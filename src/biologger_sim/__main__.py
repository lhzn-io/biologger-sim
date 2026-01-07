# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import argparse
import logging
import time
from pathlib import Path
from typing import Any, cast

import pandas as pd

from .config import load_config
from .core.run_manager import RunManager
from .core.telemetry import TelemetryManager
from .core.types import ProcessingMode
from .io.data_loader import load_and_filter_data
from .io.stream import SensorStream
from .io.zmq_publisher import ZMQPublisher
from .processors.lab import PostFactoProcessor


def setup_logging(log_file: Path | None, debug_level: int = 0) -> None:
    """Configures logging to file and console."""
    # Create formatters and handlers
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers = []

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    # Set level based on debug_level
    if debug_level > 0:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)


def run_lab_mode(pipeline_config: Any, config_path: Path, debug_level: int = 0) -> None:
    """Executes the pipeline in Lab Mode (Post-Facto Analysis)."""
    # Setup Run Manager
    # Use config filename stem as context for run directory
    run_context = config_path.stem
    run_manager = RunManager(context=run_context)
    run_dir = run_manager.setup()

    # Setup logging
    setup_logging(run_dir / "messages.log", debug_level)
    logger = logging.getLogger(__name__)

    logger.info("Initializing Lab Mode Pipeline...")
    logger.info(f"Run directory created: {run_dir}")
    run_manager.save_config(pipeline_config)

    # Load Data
    sim_config = pipeline_config.simulation
    logger.info(f"Loading data from: {sim_config.input_file}")

    try:
        input_path = Path(sim_config.input_file)
        # Infer metadata path: assume it's in the parent of the parent directory (datasets root)
        # e.g. datasets/Swordfish-RED.../RED...csv -> datasets/biologger_meta.csv
        meta_path = input_path.parent.parent / "biologger_meta.csv"

        # Infer Tag ID from filename: RED001_20220812_19A0564 -> RED001_20220812
        filename_stem = input_path.stem
        parts = filename_stem.split("_")
        tag_id = f"{parts[0]}_{parts[1]}" if len(parts) >= 2 else filename_stem

        if meta_path.exists():
            logger.info(f"Using metadata from {meta_path} for tag {tag_id}")
            df = load_and_filter_data(input_path, meta_path, tag_id)
        else:
            logger.warning(
                f"Metadata not found at {meta_path}. Loading CSV directly (skipping comments)."
            )
            df = pd.read_csv(input_path, comment=";", engine="python")

        logger.info(f"Loaded {len(df)} records.")
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return

    # Initialize ZMQ Publisher if configured
    zmq_publisher = None
    telemetry = None
    last_telemetry_time = time.time()

    if hasattr(sim_config, "zmq") and sim_config.zmq:
        try:
            zmq_publisher = ZMQPublisher(sim_config, debug_level=debug_level)
            telemetry = TelemetryManager()
            logger.info(f"ZMQ Publisher initialized on port {sim_config.zmq.port}")
        except Exception as e:
            logger.error(f"Failed to initialize ZMQ Publisher: {e}")

    # Initialize Processor
    processor = PostFactoProcessor(
        filt_len=48,  # TODO: Make configurable
        freq=sim_config.rate_hz,
        debug_level=debug_level,
        r_exact_mode=True,  # Default for Lab Mode
        compute_attachment_angles=True,
        compute_mag_offsets=True,
        zmq_publisher=zmq_publisher,
    )

    # Pass 1: Calibration
    logger.info("Running Pass 1: Calibration...")
    records = df.to_dict("records")
    for record in records:
        processor.process(cast(dict[str, Any], record))

    processor.calibrate_from_batch_data()
    logger.info("Calibration complete.")

    # Pass 2: Processing
    logger.info("Running Pass 2: Processing...")
    processor.reset()

    # Calculate delay for real-time playback if ZMQ is enabled
    playback_delay = 0.0
    if zmq_publisher and sim_config.rate_hz > 0:
        playback_delay = 1.0 / sim_config.rate_hz
        logger.info(f"Real-time playback enabled: {playback_delay * 1000:.1f}ms per record")

    results = []
    try:
        for i, record in enumerate(records):
            start_time = time.time()
            res = processor.process(cast(dict[str, Any], record))
            if res:
                results.append(res)

            if i % 100 == 0:
                print(f"Processed {i}/{len(records)} records...", end="\r")

            # Update telemetry if streaming
            if telemetry and zmq_publisher:
                processing_time = time.time() - start_time
                telemetry.update(processing_time)

                if time.time() - last_telemetry_time >= 1.0:
                    metrics = telemetry.get_metrics()
                    zmq_publisher.publish("sim/telemetry", metrics)
                    logger.debug(f"Telemetry: {metrics}")
                    last_telemetry_time = time.time()

            # Throttle playback if needed
            if playback_delay > 0:
                elapsed = time.time() - start_time
                if elapsed < playback_delay:
                    time.sleep(playback_delay - elapsed)
    except KeyboardInterrupt:
        logger.info("\nSimulation interrupted by user. Saving partial results...")

    # Save Results
    if results:
        result_df = pd.DataFrame(results)
        output_path = run_manager.get_output_path("output_data.csv")
        result_df.to_csv(output_path, index=False)
        logger.info(f"Results saved to: {output_path}")
    else:
        logger.warning("No results to save.")


def run_simulation_mode(pipeline_config: Any, debug_level: int = 0) -> None:
    """Executes the pipeline in Simulation Mode (Real-Time Streaming)."""
    # Setup logging (console only)
    setup_logging(None, debug_level)
    logger = logging.getLogger(__name__)

    sim_config = pipeline_config.simulation

    logger.info(f"Starting simulation in {pipeline_config.mode.value} mode")
    logger.info(f"Depth Mode: {pipeline_config.depth.mode.value}")
    logger.info(f"Input file: {sim_config.input_file}")
    logger.info(f"Streaming at {sim_config.rate_hz} Hz on port {sim_config.zmq.port}")

    stream = SensorStream(sim_config)
    publisher = ZMQPublisher(sim_config)
    telemetry = TelemetryManager()

    # If rate_hz is 0 or negative, we run as fast as possible (uncorked)
    delay = 0.0
    if sim_config.rate_hz > 0:
        delay = 1.0 / sim_config.rate_hz

    last_telemetry_time = time.time()

    try:
        for record in stream.stream():
            start_time = time.time()

            # Publish raw sensor data
            publisher.publish("sensor/raw", record)

            # Update telemetry
            processing_time = time.time() - start_time
            telemetry.update(processing_time)

            # Publish telemetry every 1 second
            if time.time() - last_telemetry_time >= 1.0:
                metrics = telemetry.get_metrics()
                publisher.publish("sim/telemetry", metrics)
                logger.debug(f"Telemetry: {metrics}")
                last_telemetry_time = time.time()

            # Calculate sleep time to maintain rate
            if delay > 0:
                elapsed = time.time() - start_time
                sleep_time = max(0.0, delay - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nStopping simulation...")
    finally:
        publisher.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Biologger Simulation Runner")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run the pipeline")
    run_parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the YAML configuration file",
    )
    run_parser.add_argument(
        "--debug-level",
        type=int,
        default=0,
        help="Debug level (0=INFO, 1=DEBUG, 2=VERBOSE)",
    )
    run_parser.add_argument(
        "--set",
        action="append",
        help="Override config values (key=value), e.g. --set simulation.rate_hz=100",
    )

    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert CSV to Feather")
    convert_parser.add_argument("input", type=Path, help="Input CSV file")
    convert_parser.add_argument("--output", type=Path, help="Output Feather file")

    # Backward compatibility: if --config is passed without a subcommand, assume 'run'
    import sys

    if len(sys.argv) > 1 and sys.argv[1].startswith("--config"):
        args = parser.parse_args(["run", *sys.argv[1:]])
    else:
        args = parser.parse_args()

    if args.command == "convert":
        from .io.converter import convert_csv_to_feather

        print(f"Converting {args.input} to Feather...")
        try:
            out_path = convert_csv_to_feather(args.input, args.output)
            print(f"Conversion complete: {out_path}")
        except Exception as e:
            print(f"Error converting file: {e}")
            return

    elif args.command == "run":
        try:
            pipeline_config = load_config(args.config, overrides=args.set)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return

        if pipeline_config.mode == ProcessingMode.LAB:
            run_lab_mode(pipeline_config, args.config, args.debug_level)
        else:
            run_simulation_mode(pipeline_config, args.debug_level)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
