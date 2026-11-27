FROM python:3.12-slim

# 安裝系統相依套件與繁體中文字體（供 PIL 繪製 AOI 標註中文標籤不變方塊字）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces 規範：使用非 root 使用者 (UID 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR $HOME/app

COPY --chown=user:user requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=user:user app.py mcp_server.py agy_reviewer.py manage_project.py patrol_notifier.py notify_director.py AI_REVIEWER_SOP.md ./
COPY --chown=user:user static_assets ./static_assets

EXPOSE 7860
CMD ["python", "app.py"]
