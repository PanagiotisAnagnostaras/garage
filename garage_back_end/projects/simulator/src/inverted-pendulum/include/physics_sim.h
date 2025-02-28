#pragma once

#include "types.h"
#include "controller.h"
#include "integrator.h"
#include <memory>
#include <map>
#include <iostream>
#include <cmath>
#include <fstream>
#include <filesystem>
#include <chrono>
#include <mutex>


namespace physics_simulator
{
    enum solver_type
    {
        EXPLICIT_EULER = 0
    };

    class PhysicSimulator
    {
    public:
        PhysicSimulator(float timestep_s = 1e-3, solver_type solver = solver_type::EXPLICIT_EULER, controller::PID pid = controller::PID(0, 0, 0, 10));
        void simulate(bool realtime);
        void run_controller();
        float getCartPos();
        float getCartVel();
        float getPendAng();
        float getPendVel();
        void setCartPos(float v);
        void setCartVel(float v);
        void setPendAng(float v);
        void setPendVel(float v);
        float getInput();
        void setHorizon(float horizon_s);
        bool isRunning();
        float getTime();
        void applyInput(float input);
        
    private:       
        static constexpr uint STATE_INDEX_CART_POS = 0;
        static constexpr uint STATE_INDEX_CART_VEL = 1;
        static constexpr uint STATE_INDEX_PEND_ANG = 2;
        static constexpr uint STATE_INDEX_PEND_VEL = 3;
        static constexpr float PI = 3.1415926;

        void initializeStates();
        void step();
        void setState(Vf state);
        void computeDynamics();
        void addNoise(Vf noise);
        void updateBuffers();
        void wrapToCircle();
        Vf getState();



        controller::PID pid_;
        Vf f_, state_;
        bool sim_is_over_;
        int number_of_steps_;
        float input_, timestep_s_, horizon_s_, mass_cart_, mass_pendulum_, length_, g_, inertia_, elapsed_sim_time_s_;
        solver_type solver_;
        std::shared_ptr<integrator::ExplicitEuler> solver_ptr_;
        std::vector<float> cart_pos_buffer_, cart_vel_buffer_, pend_ang_buffer_, pend_vel_buffer_, input_buffer_, time_buffer_;
        std::mutex input_mutex_;
    };
}