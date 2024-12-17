FROM ubuntu:24.04

WORKDIR /garage_back_end

RUN apt-get update && \
    apt-get install -y \
        python3-pip \
        vim \
        curl \
        iputils-ping \
        python3-django-cors-headers \
        python3-django \
        python3-djangorestframework && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["bash", "/garage_back_end/installation_scripts/run_back_end.sh"]