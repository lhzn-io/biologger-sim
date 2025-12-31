# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import argparse
import logging
import time
from pathlib import Path
from typing import Any, cast

import pandas as pd

from .config import load_config
from .core.run_manager import RunManager
from .core.types import ProcessingMode
from .io.data_loader import load_and_filter_data
from .io.stream import SensorStream
from .io.zmq_publisher import ZMQPublisher
from .processors.lab import PostFactoProcessor


def setup_logging(log_file: Path) -> None:
    """Configures logging to file and console."""
    # Create formatters and handlers
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    # Remove existing handlers to avoid duplication
    root_logger.handlers = []
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)


def run_lab_mode(pipeline_config: Any, config_path: Path) -> None:
    """Executes the pipeline in Lab Mode (Post-Facto Analysis)."""
    # Setup Run Manager
    # Use config filename stem as context for run directory
    run_context = config_path.stem
    run_manager = RunManager(context=run_context)
    run_dir = run_manager.setup()

    # Setup logging
    setup_logging(run_dir / "messages.log")
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

    # Initialize Processor
    processor = PostFactoProcessor(
        filt_len=48,  # TODO: Make configurable
        freq=sim_config.rate_hz,
        r_exact_mode=True,  # Default for Lab Mode
        compute_attachment_angles=True,
        compute_mag_offsets=True,
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
    results = []
    for record in records:
        res = processor.process(cast(dict[str, Any], record))
        results.append(res)

    # Save Results
    result_df = pd.DataFrame(results)
    output_path = run_manager.get_output_path("output_data.csv")
    result_df.to_csv(output_path, index=False)
    logger.info(f"Results saved to: {output_path}")


def run_simulation_mode(pipeline_config: Any) -> None:
    """Executes the pipeline in Simulation Mode (Real-Time Streaming)."""
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
            pipeline_config = load_config(args.config)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return

        if pipeline_config.mode == ProcessingMode.LAB:
            run_lab_mode(pipeline_config, args.config)
        else:
            run_simulation_mode(pipeline_config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
