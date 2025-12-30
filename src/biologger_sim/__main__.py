import argparse
import time
from pathlib import Path

from .core.types import ProcessingMode, SimulationConfig
from .io.stream import SensorStream
from .io.zmq_publisher import ZMQPublisher


def main() -> None:
    parser = argparse.ArgumentParser(description="Biologger Simulation Runner")
    parser.add_argument("data_file", type=Path, help="Path to the input CSV file")
    parser.add_argument("--port", type=int, default=5555, help="ZMQ port")
    parser.add_argument("--rate", type=float, default=100.0, help="Target Hz for playback")
    parser.add_argument("--loop", action="store_true", help="Loop playback")

    args = parser.parse_args()

    config = SimulationConfig(
        mode=ProcessingMode.SIMULATION, zmq_port=args.port, loop_playback=args.loop
    )

    print(f"Starting simulation with file: {args.data_file}")
    print(f"Streaming at {args.rate} Hz on port {args.port}")

    stream = SensorStream(args.data_file, config)
    publisher = ZMQPublisher(config)

    delay = 1.0 / args.rate

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
