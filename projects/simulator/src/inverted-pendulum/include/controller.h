#pragma once
#include "types.h"

namespace controller
{
    class PID
    {
    public:
        PID(const float &Kp, const float &Kd, const float &Ki, const float &sampling_f);
        float compute_input(const float &measurement);
        void set_setpoint(const float &setpoint);
        float get_sampling_period_microsec() { return 1/sampling_f_s_ * 1e6; };

    private:
        void update_error(const float &measurement);
        void clear_error();
        float Kp_, Kd_, Ki_, p_error_, d_error_, i_error_, sampling_f_s_, setpoint_;
    };

} // namespace controller
