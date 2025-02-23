FROM ubuntu:24.04

WORKDIR /garage_back_end

RUN apt-get update && \
    apt-get install -y \
        software-properties-common \
        git \
        build-essential \
        gdb \
        python3 \
        vim \
        libasio-dev \
        libx11-dev \
        ffmpeg \
        imagemagick \
        x11-apps \
        python3.12-venv \
        xorg \
        openbox \
        python3-setuptools \
        libx11-6 \
        ca-certificates \
        curl \
        iputils-ping \
        cmake \
        python3-dev \
        python3-tk \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy source code
COPY . .

# Make virtual environment
RUN python3 -m venv /.venv_simulator
ENV PYTHON_VENV=/.venv_simulator/bin/python3
ENV PIP_VENV=/.venv_simulator/bin/pip
RUN $PIP_VENV install -r requirements.txt

# Build simulator
RUN bash /garage_back_end/projects/simulator/installation_scripts/build_simulator.sh

# Make bindings
WORKDIR /garage_back_end/projects/simulator
RUN ${PYTHON_VENV} src/binder/setup.py bdist_wheel
RUN ${PIP_VENV} install dist/binder-0.0.1-cp312-cp312-linux_x86_64.whl --force-reinstall