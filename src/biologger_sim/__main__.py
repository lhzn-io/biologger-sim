import argparse
import time
from pathlib import Path

from .config import load_config
from .io.stream import SensorStream
from .io.zmq_publisher import ZMQPublisher


def main() -> None:
    parser = argparse.ArgumentParser(description="Biologger Simulation Runner")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the YAML configuration file",
    )

    args = parser.parse_args()

    try:
        pipeline_config = load_config(args.config)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return

    sim_config = pipeline_config.simulation

    print(f"Starting simulation in {pipeline_config.mode.value} mode")
    print(f"Depth Mode: {pipeline_config.depth.mode.value}")
    print(f"Input file: {sim_config.input_file}")
    print(f"Streaming at {sim_config.rate_hz} Hz on port {sim_config.zmq.port}")

    stream = SensorStream(sim_config)
    publisher = ZMQPublisher(sim_config)

    delay = 1.0 / sim_config.rate_hz

    try:
        for record in stream.stream():
            start_time = time.time()

            # Publish raw sensor data
            publisher.publish("sensor/raw", record)

            # Calculate sleep time to maintain rate
            elapsed = time.time() - start_time
            sleep_time = max(0, delay - elapsed)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nStopping simulation...")
    finally:
        publisher.close()


if __name__ == "__main__":
    main()
