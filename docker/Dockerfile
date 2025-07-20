FROM python:3.11-slim

# 1. System libs for VTK and graphics
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libgl1 \
    libglu1-mesa \
    libvtk9-dev \
    libxrender1 \
    libxext6 \
    libsm6 \
    && rm -rf /var/lib/apt/lists/*


# 2. Python deps
COPY docker/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 3. Non-root user (optional)
RUN useradd -ms /bin/bash vscode
USER vscode
WORKDIR /workspace
