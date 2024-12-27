rm -rf /garage_back_end/projects/simulator/build/
mkdir -p /garage_back_end/projects/simulator/build/
cmake -B /garage_back_end/projects/simulator/build/ -S /garage_back_end/projects/simulator/
make -C /garage_back_end/projects/simulator/build
