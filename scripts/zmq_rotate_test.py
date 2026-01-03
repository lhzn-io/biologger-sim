import time

import numpy as np
import zmq
from scipy.spatial.transform import Rotation as R  # noqa: N817


def main() -> None:
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    print("ZMQ Publisher started on tcp://*:5555")
    print("Sending tumbling quaternion for /World/Shark...")

    # Initial rotation
    current_r = R.from_euler("z", 0, degrees=True)

    # Initial angular velocity vector (direction = axis, magnitude = speed in rad/step)
    # Throttled to ~1000Hz
    ang_vel = np.array([0.0025, 0.005, 0.001])

    try:
        while True:
            # 1. Apply incremental rotation
            # Create rotation from current angular velocity vector
            delta_r = R.from_rotvec(ang_vel)
            current_r = delta_r * current_r

            quat = current_r.as_quat()  # returns [x, y, z, w] in scipy

            # Omniverse Gf.Quatf takes (w, x, y, z)
            # So we need to reorder from [x, y, z, w] to [w, x, y, z]
            w_first_quat = [float(quat[3]), float(quat[0]), float(quat[1]), float(quat[2])]

            # Simulate Dynamic Acceleration (Body Frame)
            # Shark swimming is primarily lateral (Y-axis) oscillation
            # We'll generate a sine wave based on time to simulate tail beats
            t = time.time()
            freq = 2.0  # 2 Hz tail beat
            amp = 0.5  # 0.5g amplitude

            # Body-frame dynamic accel: [Surge (X), Sway (Y), Heave (Z)]
            # Simulating a sway (tail beat)
            accel_dyn = [
                np.random.normal(0, 0.05),  # X: minimal surge noise
                np.sin(t * freq * 2 * np.pi) * amp,  # Y: strong lateral oscillation
                np.random.normal(0, 0.05),  # Z: minimal heave noise
            ]

            vedba = np.sqrt(accel_dyn[0] ** 2 + accel_dyn[1] ** 2 + accel_dyn[2] ** 2)

            message = {
                "transform": {"quat": w_first_quat},
                "physics": {"accel_dynamic": [float(x) for x in accel_dyn], "vedba": float(vedba)},
            }

            socket.send_json(message)

            # 2. Evolve angular velocity (Autocorrelated Random Walk)
            # Add small random noise to the angular velocity vector
            # This smoothly changes the axis and speed of rotation
            noise = np.random.normal(0, 0.000025, 3)
            ang_vel += noise

            # Soft speed limit (damping) to prevent it from spinning too fast
            speed = np.linalg.norm(ang_vel)
            if speed > 0.015:
                ang_vel *= 0.99  # Dampen if too fast

            # Throttled to ~1000Hz to save CPU
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("Stopping publisher...")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
