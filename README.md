## Brief
Repo containing the code of the inverted-pendulum simulator.
The goal of this project is to develop a complete application for simulating and controlling an inverted-pendulum.

## Overview
The project consists of three containers.
### Container 1: front_end_container
1. Written in `JS` and uses `React`
2. Responsible for the user interface and for starting the simulation
### Container 2: back_end_container
1. Written in `Python` and uses `Django`
2. Receives the request from the front end and forwards it to the `projects_container`
### Container 3: projects_container
1. Written mostly in `C++` with a `Python` wrapper.
2. Contains also a server which receives the forwarded request from the back_end_container. The server is written with `Pistacheio` https://pistacheio.github.io/pistache/
3. When a request is received, the `spawn_simulation.py` script is launched which access the simulator through the `pybind11` layer.

## How to use
- Clone this repo
- Run `git submodule update --init --recursive`
- You need to have `docker` and `docker compose` installed 
- Build the docker images
    - `cd docker_scripts`
    - `bash build_image_all.sh`
- Start the containers
    - (from inside `docker_scripts`)
    - `bash containers_start.sh`
    - *also runs `xhost local:root`*
- Access the front end of the garage
    - Open a browser and head to [local](http://localhost:3000/)


## Next steps
- Use `Eigen` instead of custom types for the simulation
- Implement MPC controller
- Use the `python`-`C++` communication provided by `Pybind11` for developing learning based controllers.
