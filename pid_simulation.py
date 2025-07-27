import pandas as pd

def run_pid_simulation(Kp=1.0, Ki=0.1, Kd=0.05):
    setpoint = 60.0  # km/h
    speed = 0.0
    dt = 1  # time step in seconds
    integral = 0.0
    prev_error = 0.0
    time_series = []
    speed_series = []

    for t in range(0, 31):
        error = setpoint - speed
        integral += error * dt
        derivative = (error - prev_error) / dt
        output = Kp * error + Ki * integral + Kd * derivative
        speed += output * dt
        prev_error = error

        time_series.append(t)
        speed_series.append(speed)

    # Behavior classification
    if max(speed_series) > 1.5 * setpoint:
        behavior = "Unstable (Overshooting)"
    elif abs(speed_series[-1] - setpoint) < 2:
        behavior = "Well Tuned"
    elif speed_series[-1] < setpoint * 0.9:
        behavior = "Underpowered (Not reaching target)"
    else:
        behavior = "Slow Response or Untuned"

    df = pd.DataFrame({"Time(s)": time_series, "Speed(kmph)": speed_series})
    df.to_csv("data.csv", index=False)
    return {"time": time_series, "speed": speed_series, "status": behavior}
