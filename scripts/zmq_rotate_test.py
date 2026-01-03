import argparse
import json
import time

import numpy as np
import zmq
from scipy.spatial.transform import Rotation as R  # noqa: N817


def main() -> None:
    parser = argparse.ArgumentParser(description="ZMQ Rotation Test Publisher")
    parser.add_argument(
        "--calibrate",
        "-c",
        action="store_true",
        help="Send zero rotation (0,0,0) for calibration",
    )
    args = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    topic = "biologger/telemetry"

    print("ZMQ Publisher started on tcp://*:5555")
    if args.calibrate:
        print(f"Sending CALIBRATION (0,0,0) for /World/Animal on topic '{topic}'...")
    else:
        print(f"Sending tumbling quaternion for /World/Animal on topic '{topic}'...")

    # Initial rotation
    current_r = R.from_euler("z", 0, degrees=True)

    # Initial angular velocity vector (direction = axis, magnitude = speed in rad/step)
    # Throttled to ~1000Hz
    ang_vel = np.array([0.0025, 0.005, 0.001])

    try:
        while True:
            if args.calibrate:
                # Calibration mode: Send 0,0,0
                roll, pitch, heading = 0.0, 0.0, 0.0
                accel_dyn = [0.0, 0.0, 0.0]
                vedba = 0.0
                odba = 0.0
                depth = 0.0
                velocity = 0.0
            else:
                # 1. Apply incremental rotation
                # Create rotation from current angular velocity vector
                delta_r = R.from_rotvec(ang_vel)
                current_r = delta_r * current_r

                # Convert to Euler angles (degrees) for ZMQ payload
                # Order: ZYX (Yaw, Pitch, Roll) -> [Heading, Pitch, Roll]
                # Note: scipy returns [yaw, pitch, roll] for 'zyx'
                euler = current_r.as_euler("zyx", degrees=True)
                heading, pitch, roll = euler[0], euler[1], euler[2]

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
                odba = np.sum(np.abs(accel_dyn))

                # Simulate Depth and Velocity
                depth = 10.0 + 5.0 * np.sin(t * 0.1)  # Oscillating depth
                velocity = 1.5 + 0.5 * np.sin(t * 0.5)  # Oscillating velocity

                # 2. Evolve angular velocity (Autocorrelated Random Walk)
                # Add small random noise to the angular velocity vector
                # This smoothly changes the axis and speed of rotation
                noise = np.random.normal(0, 0.000025, 3)
                ang_vel += noise

                # Soft speed limit (damping) to prevent it from spinning too fast
                speed = np.linalg.norm(ang_vel)
                if speed > 0.015:
                    ang_vel *= 0.99  # Dampen if too fast

            message = {
                "rotation": {
                    "euler_deg": [float(roll), float(pitch), float(heading)],
                    "order": "zyx",
                },
                "physics": {
                    "accel_dynamic": [float(x) for x in accel_dyn],
                    "vedba": float(vedba),
                    "odba": float(odba),
                    "depth": float(depth),
                    "velocity": float(velocity),
                },
            }

            # Send with topic prefix
            json_str = json.dumps(message)
            socket.send_string(f"{topic} {json_str}")

            # Throttled to ~1000Hz to save CPU
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("Stopping publisher...")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
