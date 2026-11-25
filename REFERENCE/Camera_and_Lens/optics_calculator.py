#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NI Vision / Basler dart / C-Mount & Macro Optics Selection & Calculation Engine
Compatible with NI Vision Development Module (VDM) & IMAQdx workflows.
"""

import sys
if sys.stdout and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import os
import json
import argparse
from typing import Dict, List, Optional, Tuple, Any

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'optics_database.json')

def load_database() -> Dict[str, Any]:
    """Loads the optics database from JSON."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file not found: {DB_PATH}")
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_database(db: Dict[str, Any]) -> None:
    """Saves the optics database to JSON."""
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def get_camera(db: Dict[str, Any], model_name: str) -> Optional[Dict[str, Any]]:
    """Retrieves camera specs by model name (case-insensitive)."""
    model_lower = model_name.strip().lower()
    for cam in db['cameras']:
        if cam['model'].lower() == model_lower:
            return cam
    return None

def add_camera_model(
    model: str,
    shutter: str,
    pixels_h: int,
    pixels_v: int,
    pixel_size_um: float
) -> Dict[str, Any]:
    """
    Dynamically adds a new camera model to the database and re-computes
    compatibility matrices for all fixed and macro lenses.
    """
    db = load_database()
    
    # Check if already exists
    existing = get_camera(db, model)
    if existing:
        print(f"[Warning] Camera '{model}' already exists. Updating parameters.")
        db['cameras'] = [c for c in db['cameras'] if c['model'].lower() != model.lower()]

    sensor_h = round(pixels_h * pixel_size_um / 1000.0, 4)
    sensor_v = round(pixels_v * pixel_size_um / 1000.0, 4)
    sensor_diag = round((sensor_h**2 + sensor_v**2)**0.5, 3)
    megapixels = round((pixels_h * pixels_v) / 1e6, 2)

    new_cam = {
        'model': model.strip(),
        'shutter': shutter.strip().capitalize(),
        'pixels_h': int(pixels_h),
        'pixels_v': int(pixels_v),
        'pixel_size_um': float(pixel_size_um),
        'sensor_h_mm': sensor_h,
        'sensor_v_mm': sensor_v,
        'sensor_diag_mm': sensor_diag,
        'aspect_ratio': f"{pixels_h}:{pixels_v}",
        'megapixels': megapixels
    }
    db['cameras'].append(new_cam)

    # Update fix lenses precomputed entries
    for lens in db['fix_lenses']:
        for entry in lens['entries']:
            mag = entry['mag_factor']
            fov_h = round(sensor_h * mag, 2)
            fov_v = round(sensor_v * mag, 2)
            res_mm_px = round(pixel_size_um * mag / 1000.0, 4)
            px_per_mm = round(1.0 / res_mm_px, 2) if res_mm_px > 0 else 0
            entry['camera_combinations'][new_cam['model']] = {
                'fov_h_mm': fov_h,
                'fov_v_mm': fov_v,
                'mm_per_pixel': res_mm_px,
                'pixels_per_mm': px_per_mm
            }

    # Update macro lenses precomputed entries
    for entry in db['macro_lenses']['entries']:
        mag = entry['magnification']
        fov_h = round(sensor_h / mag, 3)
        fov_v = round(sensor_v / mag, 3)
        res_mm_px = round((pixel_size_um / mag) / 1000.0, 5)
        px_per_mm = round(1.0 / res_mm_px, 2) if res_mm_px > 0 else 0
        entry['camera_combinations'][new_cam['model']] = {
            'fov_h_mm': fov_h,
            'fov_v_mm': fov_v,
            'mm_per_pixel': res_mm_px,
            'pixels_per_mm': px_per_mm
        }

    save_database(db)
    return new_cam

def calculate_fix_lens(
    cam: Dict[str, Any],
    lens: Dict[str, Any],
    wd_mm: float
) -> Dict[str, Any]:
    """
    Calculates optical field and resolution for a camera paired with a fixed lens at a given WD.
    Uses table lookup or piecewise linear interpolation for arbitrary WDs.
    """
    entries = lens['entries']
    wds = [e['wd_mm'] for e in entries]

    if wd_mm <= wds[0]:
        # Clamp or extrapolate below min WD
        ratio = wd_mm / wds[0] if wds[0] > 0 else 1.0
        mag = entries[0]['mag_factor'] * ratio
    elif wd_mm >= wds[-1]:
        # Linear extrapolation above max WD using last segment
        slope = (entries[-1]['mag_factor'] - entries[-2]['mag_factor']) / (wds[-1] - wds[-2])
        mag = entries[-1]['mag_factor'] + slope * (wd_mm - wds[-1])
    else:
        # Interpolate between closest bracket
        for i in range(len(wds) - 1):
            if wds[i] <= wd_mm <= wds[i+1]:
                t = (wd_mm - wds[i]) / (wds[i+1] - wds[i])
                mag = entries[i]['mag_factor'] + t * (entries[i+1]['mag_factor'] - entries[i]['mag_factor'])
                break

    fov_h = round(cam['sensor_h_mm'] * mag, 2)
    fov_v = round(cam['sensor_v_mm'] * mag, 2)
    mm_per_pixel = round(cam['pixel_size_um'] * mag / 1000.0, 4)
    pixels_per_mm = round(1.0 / mm_per_pixel, 2) if mm_per_pixel > 0 else 0.0

    return {
        'camera': cam['model'],
        'lens': lens['name'],
        'lens_type': 'Fixed Focal Length',
        'focal_length_mm': lens['focal_length_mm'],
        'wd_mm': wd_mm,
        'magnification_factor': round(mag, 4),
        'fov_h_mm': fov_h,
        'fov_v_mm': fov_v,
        'mm_per_pixel': mm_per_pixel,
        'pixels_per_mm': pixels_per_mm
    }

def calculate_macro_lens(
    cam: Dict[str, Any],
    magnification: float
) -> Dict[str, Any]:
    """
    Calculates optical field and resolution for a camera paired with a macro/telecentric lens.
    """
    fov_h = round(cam['sensor_h_mm'] / magnification, 3)
    fov_v = round(cam['sensor_v_mm'] / magnification, 3)
    mm_per_pixel = round((cam['pixel_size_um'] / magnification) / 1000.0, 5)
    pixels_per_mm = round(1.0 / mm_per_pixel, 2) if mm_per_pixel > 0 else 0.0

    return {
        'camera': cam['model'],
        'lens': f"{magnification}X",
        'lens_type': 'Macro / Telecentric',
        'magnification': magnification,
        'fov_h_mm': fov_h,
        'fov_v_mm': fov_v,
        'mm_per_pixel': mm_per_pixel,
        'pixels_per_mm': pixels_per_mm
    }

def recommend_optics(
    target_fov_w: float,
    target_fov_h: float,
    wd_limit: Optional[float] = None,
    max_resolution_mm: Optional[float] = None,
    shutter_preference: Optional[str] = None,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Reverse selection algorithm:
    Given target FOV (w x h), working distance limit, resolution constraint, and shutter preference,
    evaluates all camera and lens permutations and ranks them by suitability score.
    """
    db = load_database()
    candidates = []

    for cam in db['cameras']:
        # Filter shutter if required
        if shutter_preference:
            if cam['shutter'].lower() != shutter_preference.strip().lower():
                continue

        # 1. Test Fixed Lenses
        for lens in db['fix_lenses']:
            # Search available WDs
            for entry in lens['entries']:
                wd = entry['wd_mm']
                if wd_limit is not None and wd > wd_limit * 1.15:
                    continue  # Exceeds WD constraint
                
                # Check precalculated combo
                combo = entry['camera_combinations'].get(cam['model'])
                if not combo:
                    combo_calc = calculate_fix_lens(cam, lens, wd)
                    fov_h = combo_calc['fov_h_mm']
                    fov_v = combo_calc['fov_v_mm']
                    res = combo_calc['mm_per_pixel']
                    px_mm = combo_calc['pixels_per_mm']
                else:
                    fov_h = combo['fov_h_mm']
                    fov_v = combo['fov_v_mm']
                    res = combo['mm_per_pixel']
                    px_mm = combo['pixels_per_mm']

                # Must cover the target FOV (considering orientation swap)
                covers_direct = (fov_h >= target_fov_w * 0.98) and (fov_v >= target_fov_h * 0.98)
                covers_rotated = (fov_h >= target_fov_h * 0.98) and (fov_v >= target_fov_w * 0.98)

                if not (covers_direct or covers_rotated):
                    continue

                # Check resolution constraint
                if max_resolution_mm is not None and res > max_resolution_mm:
                    continue

                # Compute Score:
                # 1. FOV overhead (prefer tighter fit to maximize pixel usage on target)
                area_ratio = (fov_h * fov_v) / (target_fov_w * target_fov_h)
                # Ideal area_ratio is 1.15 ~ 1.35 (15%~35% safety margin)
                fov_penalty = abs(area_ratio - 1.25)

                # 2. WD score
                wd_penalty = 0.0
                if wd_limit is not None:
                    wd_penalty = abs(wd - wd_limit) / max(wd_limit, 100.0)

                # 3. Resolution score: finer is better
                res_score = res * 10.0

                total_score = fov_penalty * 2.0 + wd_penalty * 1.5 + res_score

                candidates.append({
                    'score': round(total_score, 4),
                    'camera': cam['model'],
                    'shutter': cam['shutter'],
                    'pixels': f"{cam['pixels_h']}x{cam['pixels_v']}",
                    'lens': lens['name'],
                    'lens_type': 'Fixed Lens',
                    'wd_mm': wd,
                    'fov_h_mm': fov_h,
                    'fov_v_mm': fov_v,
                    'fov_area_margin_pct': round((area_ratio - 1.0) * 100, 1),
                    'mm_per_pixel': res,
                    'pixels_per_mm': px_mm
                })

        # 2. Test Macro Lenses (when FOV is small, typically < 80mm)
        if max(target_fov_w, target_fov_h) <= 80:
            for entry in db['macro_lenses']['entries']:
                mag = entry['magnification']
                combo = entry['camera_combinations'].get(cam['model'])
                if combo:
                    fov_h = combo['fov_h_mm']
                    fov_v = combo['fov_v_mm']
                    res = combo['mm_per_pixel']
                    px_mm = combo['pixels_per_mm']
                else:
                    fov_h = round(cam['sensor_h_mm'] / mag, 3)
                    fov_v = round(cam['sensor_v_mm'] / mag, 3)
                    res = round((cam['pixel_size_um'] / mag) / 1000.0, 5)
                    px_mm = round(1.0 / res, 2)

                covers_direct = (fov_h >= target_fov_w * 0.98) and (fov_v >= target_fov_h * 0.98)
                covers_rotated = (fov_h >= target_fov_h * 0.98) and (fov_v >= target_fov_w * 0.98)

                if not (covers_direct or covers_rotated):
                    continue

                if max_resolution_mm is not None and res > max_resolution_mm:
                    continue

                area_ratio = (fov_h * fov_v) / (target_fov_w * target_fov_h)
                fov_penalty = abs(area_ratio - 1.2)
                total_score = fov_penalty * 2.0 + res * 10.0

                candidates.append({
                    'score': round(total_score, 4),
                    'camera': cam['model'],
                    'shutter': cam['shutter'],
                    'pixels': f"{cam['pixels_h']}x{cam['pixels_v']}",
                    'lens': entry['magnification_label'],
                    'lens_type': 'Macro / Telecentric',
                    'wd_mm': 'Fixed by Lens Model',
                    'fov_h_mm': fov_h,
                    'fov_v_mm': fov_v,
                    'fov_area_margin_pct': round((area_ratio - 1.0) * 100, 1),
                    'mm_per_pixel': res,
                    'pixels_per_mm': px_mm
                })

    # Sort candidates by ascending score (lower is better)
    candidates.sort(key=lambda x: x['score'])
    return candidates[:top_k]

def main():
    parser = argparse.ArgumentParser(description="NI Vision / Basler dart Optics Selection Engine")
    subparsers = parser.add_subparsers(dest="subcommand", help="Sub-commands")

    # List cameras
    subparsers.add_parser("list-cameras", help="List all available cameras")
    subparsers.add_parser("list-lenses", help="List all available lenses")

    # Forward Calculation
    calc_parser = subparsers.add_parser("calc", help="Forward optical field calculation")
    calc_parser.add_argument("--camera", required=True, help="Camera model name (e.g. daA3840-45u)")
    calc_parser.add_argument("--lens", help="Fixed lens focal length (e.g. 8mm, 16mm, 25mm)")
    calc_parser.add_argument("--wd", type=float, help="Working distance in mm")
    calc_parser.add_argument("--macro", type=float, help="Macro magnification (e.g. 0.5 for 0.5X)")

    # Recommend / Reverse Selection
    rec_parser = subparsers.add_parser("recommend", help="Recommend optimal camera and lens setups")
    rec_parser.add_argument("--fov-w", type=float, required=True, help="Target FOV width in mm")
    rec_parser.add_argument("--fov-h", type=float, required=True, help="Target FOV height in mm")
    rec_parser.add_argument("--wd", type=float, help="Working distance target/limit in mm")
    rec_parser.add_argument("--max-res", type=float, help="Maximum allowable mm/pixel (precision)")
    rec_parser.add_argument("--shutter", choices=["Global", "Rolling"], help="Filter shutter type")
    rec_parser.add_argument("--top", type=int, default=5, help="Number of top candidates to display")

    # Add Camera
    add_parser = subparsers.add_parser("add-camera", help="Add a new camera model to the database")
    add_parser.add_argument("--model", required=True, help="Camera model identifier")
    add_parser.add_argument("--shutter", required=True, choices=["Global", "Rolling"], help="Shutter mechanism")
    add_parser.add_argument("--pixels-h", type=int, required=True, help="Horizontal pixel resolution")
    add_parser.add_argument("--pixels-v", type=int, required=True, help="Vertical pixel resolution")
    add_parser.add_argument("--pixel-size", type=float, required=True, help="Pixel size in micrometers (um)")

    args = parser.parse_args()
    db = load_database()

    if args.subcommand == "list-cameras":
        print(f"\n{'='*78}")
        print(f"{'Model':<15} | {'Shutter':<8} | {'Resolution':<12} | {'Pixel':<7} | {'Sensor (WxH)':<16} | {'MP':<5}")
        print(f"{'-'*78}")
        for c in db['cameras']:
            print(f"{c['model']:<15} | {c['shutter']:<8} | {c['pixels_h']}x{c['pixels_v']:<7} | {c['pixel_size_um']}um{'':<3} | {c['sensor_h_mm']}x{c['sensor_v_mm']} mm{'':<5} | {c['megapixels']}MP")
        print(f"{'='*78}\n")

    elif args.subcommand == "list-lenses":
        print("\n--- FIXED FOCAL LENGTH LENSES ---")
        for l in db['fix_lenses']:
            print(f"Lens: {l['name']:<6} | Nominal Focal Length: {l['focal_length_mm']:<3} mm | Working Distance: {l['min_wd_mm']} ~ {l['max_wd_mm']} mm (step {l['wd_step_mm']}mm)")
        print("\n--- MACRO / TELECENTRIC LENSES ---")
        mags = [e['magnification_label'] for e in db['macro_lenses']['entries']]
        print("Magnifications:", ", ".join(mags), "\n")

    elif args.subcommand == "calc":
        cam = get_camera(db, args.camera)
        if not cam:
            print(f"[Error] Camera '{args.camera}' not found in database.")
            sys.exit(1)

        if args.lens:
            lens_match = None
            for l in db['fix_lenses']:
                if l['name'].lower() == args.lens.lower() or l['name'].replace('mm','').strip() == args.lens.replace('mm','').strip():
                    lens_match = l
                    break
            if not lens_match:
                print(f"[Error] Lens '{args.lens}' not recognized.")
                sys.exit(1)
            wd = args.wd if args.wd is not None else 200.0
            res = calculate_fix_lens(cam, lens_match, wd)
            print("\n" + "="*50)
            print(f" Camera:         {res['camera']} ({cam['shutter']} Shutter, {cam['pixels_h']}x{cam['pixels_v']})")
            print(f" Lens:           {res['lens']} Fixed Lens")
            print(f" Working Dist:   {res['wd_mm']} mm")
            print(f" FOV (H x V):    {res['fov_h_mm']} mm x {res['fov_v_mm']} mm")
            print(f" Resolution:     {res['mm_per_pixel']} mm/pixel ({res['mm_per_pixel']*1000:.1f} µm/pixel)")
            print(f" Pixel Density:  {res['pixels_per_mm']} pixels/mm")
            print("="*50 + "\n")

        elif args.macro is not None:
            res = calculate_macro_lens(cam, args.macro)
            print("\n" + "="*50)
            print(f" Camera:         {res['camera']} ({cam['shutter']} Shutter, {cam['pixels_h']}x{cam['pixels_v']})")
            print(f" Lens:           {res['lens']} Macro / Telecentric")
            print(f" FOV (H x V):    {res['fov_h_mm']} mm x {res['fov_v_mm']} mm")
            print(f" Resolution:     {res['mm_per_pixel']} mm/pixel ({res['mm_per_pixel']*1000:.1f} µm/pixel)")
            print(f" Pixel Density:  {res['pixels_per_mm']} pixels/mm")
            print("="*50 + "\n")
        else:
            print("[Error] Please specify either --lens with --wd, or --macro <magnification>.")

    elif args.subcommand == "recommend":
        recs = recommend_optics(
            target_fov_w=args.fov_w,
            target_fov_h=args.fov_h,
            wd_limit=args.wd,
            max_resolution_mm=args.max_res,
            shutter_preference=args.shutter,
            top_k=args.top
        )
        print(f"\nTarget Request: FOV = {args.fov_w} x {args.fov_h} mm | WD limit = {args.wd} mm | Shutter = {args.shutter or 'Any'}")
        print(f"{'='*90}")
        print(f"{'Rank':<5} | {'Camera':<14} | {'Lens':<8} | {'WD (mm)':<10} | {'Actual FOV':<16} | {'Margin':<8} | {'Resolution':<12}")
        print(f"{'-'*90}")
        for idx, r in enumerate(recs, 1):
            wd_str = f"{r['wd_mm']}" if isinstance(r['wd_mm'], (int, float)) else str(r['wd_mm'])
            fov_str = f"{r['fov_h_mm']}x{r['fov_v_mm']} mm"
            res_str = f"{r['mm_per_pixel']} mm/px"
            margin_str = f"+{r['fov_area_margin_pct']}%"
            print(f"#{idx:<4} | {r['camera']:<14} | {r['lens']:<8} | {wd_str:<10} | {fov_str:<16} | {margin_str:<8} | {res_str:<12}")
        print(f"{'='*90}\n")

    elif args.subcommand == "add-camera":
        new_cam = add_camera_model(
            model=args.model,
            shutter=args.shutter,
            pixels_h=args.pixels_h,
            pixels_v=args.pixels_v,
            pixel_size_um=args.pixel_size
        )
        print(f"\n[Success] Camera '{new_cam['model']}' successfully registered and propagated to database!")
        print(f"Specs: {new_cam['pixels_h']}x{new_cam['pixels_v']} ({new_cam['megapixels']} MP), Shutter: {new_cam['shutter']}, Sensor: {new_cam['sensor_h_mm']} x {new_cam['sensor_v_mm']} mm\n")

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
