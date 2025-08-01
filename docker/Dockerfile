FROM python:3.11-slim

# 1. System libs for VTK and graphics
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    gfortran \
    pkg-config \
    libblas-dev \
    liblapack-dev \
    coinor-libipopt-dev \
    coinor-libipopt1v5 \
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

# 3. MATLAB Engine environment (requires MATLAB installation)
ENV MATLAB_ROOT=/usr/local/MATLAB
ENV LD_LIBRARY_PATH=$MATLAB_ROOT/bin/glnxa64:$LD_LIBRARY_PATH
ENV PYTHONPATH=$MATLAB_ROOT/extern/engines/python:$PYTHONPATH

# 4. Non-root user (optional)
RUN useradd -ms /bin/bash vscode
USER vscode
WORKDIR /workspace
