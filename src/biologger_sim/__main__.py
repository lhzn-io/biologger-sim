# Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import argparse
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


def run_lab_mode(pipeline_config: Any, config_path: Path) -> None:
    """Executes the pipeline in Lab Mode (Post-Facto Analysis)."""
    print("Initializing Lab Mode Pipeline...")

    # Setup Run Manager
    # Use config filename stem as context for run directory
    run_context = config_path.stem
    run_manager = RunManager(context=run_context)
    run_dir = run_manager.setup()
    print(f"Run directory created: {run_dir}")
    run_manager.save_config(pipeline_config)

    # Load Data
    sim_config = pipeline_config.simulation
    print(f"Loading data from: {sim_config.input_file}")

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
            print(f"Using metadata from {meta_path} for tag {tag_id}")
            df = load_and_filter_data(input_path, meta_path, tag_id)
        else:
            print(f"Metadata not found at {meta_path}. Loading CSV directly (skipping comments).")
            df = pd.read_csv(input_path, comment=";", engine="python")

        print(f"Loaded {len(df)} records.")
    except Exception as e:
        print(f"Error loading data: {e}")
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
    print("Running Pass 1: Calibration...")
    records = df.to_dict("records")
    for record in records:
        processor.process(cast(dict[str, Any], record))

    processor.calibrate_from_batch_data()
    print("Calibration complete.")

    # Pass 2: Processing
    print("Running Pass 2: Processing...")
    processor.reset()
    results = []
    for record in records:
        res = processor.process(cast(dict[str, Any], record))
        results.append(res)

    # Save Results
    result_df = pd.DataFrame(results)
    output_path = run_manager.get_output_path("output_data.csv")
    result_df.to_csv(output_path, index=False)
    print(f"Results saved to: {output_path}")


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

    if pipeline_config.mode == ProcessingMode.LAB:
        run_lab_mode(pipeline_config, args.config)
    else:
        run_simulation_mode(pipeline_config)


if __name__ == "__main__":
    main()
