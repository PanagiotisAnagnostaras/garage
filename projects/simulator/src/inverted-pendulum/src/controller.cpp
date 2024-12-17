#include "controller.h"

using namespace controller;
PID::PID(const float &Kp, const float &Kd, const float &Ki, const float &sampling_f) : Kp_(Kp), Kd_(Kd), Ki_(Ki), sampling_f_s_(sampling_f)
{
}

float PID::compute_input(const float &measurement)
{
    std::cout << "controller update" << std::endl;
    update_error(measurement);
    float input = Kp_ * p_error_ + Kd_ * d_error_ + Ki_ * i_error_;
    return input;
}

void PID::set_setpoint(const float &setpoint)
{
    clear_error();
    setpoint_ = setpoint;
}

void PID::update_error(const float &measurement)
{

    d_error_ = ((measurement - setpoint_) - p_error_) * sampling_f_s_;
    p_error_ = measurement - setpoint_;
    i_error_ += (measurement - setpoint_) * (1 / sampling_f_s_);
}

void PID::clear_error()
{
    p_error_ = 0;
    d_error_ = 0;
    i_error_ = 0;
}
