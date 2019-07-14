/*
********************************************************************************
* Filename      : PID Controller
* Author        : Susung Park
* Description   : Generic PID controller
* Version       : On development...
********************************************************************************
*/

#ifndef PID_CONTROLLER_H_
#define PID_CONTROLLER_H_

#define MILLIS 1000
#define MICROS 1000000

template <typename T_src, typename T_out>
class PIDController
{
public:
    PIDController();
    PIDController(T_src, T_src, T_src);
    PIDController(PIDController&);

public:
    T_out ExecFreePID(T_src&);
    T_out ExecClippedPID(T_src&, T_out, T_out);

private: // PID gains
    T_src kp_;
    T_src ki_;
    T_src kd_;

private: // PID computations
    T_src err_gross_;
    T_src err_integral_;
    T_src err_derivative_;

private: // State variables
    T_src target_val_curr_;       // Current encoder value
    T_src target_val_prev_;       // Previous encoder value
    T_src target_val_diff_;       // Target value difference between current and previous timestamp
    int timestamp_curr_;        // Current timestamp
    int timestamp_prev_;        // Previous timestamp
    int timestamp_diff_;        // Time step between current and previous timestamp
};

template <typename T_src, typename T_out>
PIDController<T_src, T_out>::PIDController()
  : err_gross_(0), err_integral_(0), err_derivative_(0),
    target_val_curr_(0), target_val_prev_(0),
    timestamp_curr_(0), timestamp_prev_(0), timestamp_diff_(0)
{
    
}

template <typename T_src, typename T_out>
PIDController<T_src, T_out>::PIDController(T_src kp, T_src ki, T_src kd)
  : kp_(kp), ki_(ki), kd_(kd),
    err_integral_(0), err_derivative_(0),
    target_val_curr_(0), target_val_prev_(0),
    timestamp_curr_(0), timestamp_prev_(0), timestamp_diff_(0)
{
    
}

template <typename T_src, typename T_out>
PIDController<T_src, T_out>::PIDController(PIDController<T_src, T_out>&)
{
    
}

template <typename T_src, typename T_out>
T_out PIDController<T_src, T_out>::ExecFreePID(T_src &target_val)
{
    // Calculate time difference.
    timestamp_curr_ = micros();
    timestamp_diff_ = timestamp_curr_ - timestamp_prev_;

    // Copy the target value.
    target_val_curr_ = target_val;
    target_val_diff_ = target_val_curr_ - target_val_prev_;

    // Calculate each PID variable.
    err_gross_ += target_val_diff_;
    err_integral_ = err_gross_ / MICROS;
    err_derivative_ = target_val_diff_ * MICROS;

    T_out pidVal = T_out(target_val_diff_ * kp_) + T_out(err_integral_ * ki_) + T_out(err_derivative_ * kd_);
    return pidVal;
}

template <typename T_src, typename T_out>
T_out PIDController<T_src, T_out>::ExecClippedPID(T_src &target_val, T_out min_bound, T_out max_bound)
{
    T_out pidVal = ExecFreePID(target_val);
    pidVal = (pidVal > max_bound ? max_bound : (pidVal < min_bound ? min_bound : pidVal));
    return pidVal;
}

#endif
