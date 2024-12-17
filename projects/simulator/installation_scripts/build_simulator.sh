rm -rf /projects/simulator/build/
mkdir -p /projects/simulator/build/
cmake -B /projects/simulator/build/ -S /projects/simulator/
make -C /projects/simulator/build
