FROM ubuntu:24.04

# Install packages
RUN apt-get update && \
    apt-get install -y \
            software-properties-common \
            git \
            build-essential \
            gdb \
            python3 \
            pip \
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
            python3-dev \
            python3-numpy \
            python3-matplotlib \
            python3-pandas \
            python3-tk \
            cmake && \
    rm -rf /var/lib/apt/lists/*

# Install Pistache
RUN add-apt-repository ppa:pistache+team/unstable 
RUN apt update
RUN apt install -y libpistache-dev
RUN apt install -y pkg-config
RUN apt install -y curl

# Mount src code
WORKDIR /projects/
COPY . .

# Build simulator
RUN bash /projects/simulator/installation_scripts/build_simulator.sh

# Make bindings
WORKDIR /projects/simulator
RUN python3 -m venv /.venv_simulator  && \
    python3 src/binder/setup.py bdist_wheel && \
    /.venv_simulator/bin/pip install dist/binder-0.0.1-cp312-cp312-linux_x86_64.whl
ENV PYTHON_VENV=/.venv_simulator/bin/python3
ENV PIP_VENV=/.venv_simulator/bin/pip
RUN $PIP_VENV install matplotlib