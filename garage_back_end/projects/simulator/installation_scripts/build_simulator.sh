rm -rf /garage_back_end/projects/simulator/build/
mkdir -p /garage_back_end/projects/simulator/build/
cmake -B /garage_back_end/projects/simulator/build/ -S /garage_back_end/projects/simulator/
make -C /garage_back_end/projects/simulator/build
cd /garage_back_end/projects/simulator
${PYTHON_VENV} src/binder/setup.py bdist_wheel
${PIP_VENV} install dist/binder-0.0.1-cp312-cp312-linux_x86_64.whl --force-reinstall