## Brief
Repo containing the code of the simulator_core simulator.
The goal of this project is to develop a complete application for simulating and controlling an simulator_core.

## Overview
The project consists of 2 containers.
### Container 1: front_end_container
1. Written in `JS` and uses `React`
2. Responsible for the user interface and for starting the simulation
### Container 2: back_end_container
1. Written in `Python` and `C++`.
2. `Python` uses `Django` for the back end server
3. The physics are written in `C++` with a `Python` wrapper. The wrapper uses `pybind11`.

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
