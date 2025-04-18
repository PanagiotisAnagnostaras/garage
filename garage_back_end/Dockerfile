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

# Build simulator and bindings
RUN bash /garage_back_end/projects/simulator/installation_scripts/build_simulator.sh

# Include modules
RUN export PYTHONPATH=$PYTHONPATH:/garage_back_end/projects/ppo/