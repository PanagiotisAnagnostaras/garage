apt-get update &&
apt-get install -y \
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
        auth \
        xorg \
        openbox \
        python3-setuptools \
        libx11-6 \
        ca-certificates \
        python3-dev \
        cmake &&
rm -rf /var/lib/apt/lists/*

apt-get update &&
    apt-get install -y \
        python3-numpy \
        python3-matplotlib \
        python3-pandas \
        python3-tk \
