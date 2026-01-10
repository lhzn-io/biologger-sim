# Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

import argparse
import heapq
import logging
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, cast

import pandas as pd

from biologger_sim.io.data_loader import load_and_filter_data, load_metadata
from biologger_sim.io.stream import SensorStream

from .config import load_config
from .core.registry import EcosystemRegistry
from .core.run_manager import RunManager
from .core.telemetry import TelemetryManager
from .core.types import ProcessingMode
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


def run_lab_mode(
    pipeline_config: Any,
    config_path: Path,
    debug_level: int = 0,
    uncork: bool = False,
    playback_speed: float = 1.0,
) -> None:
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

    sim_config = pipeline_config.simulation

    # Initialize Registry
    registry = EcosystemRegistry()

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

    # Process each entity sequentially in Lab Mode
    for entity_cfg in sim_config.entities:
        logger.info(f"--- Processing Entity: {entity_cfg.sim_id} (tag: {entity_cfg.tag_id}) ---")

        try:
            # Load and filter data (Restores deployment start/end time logic)
            # R logic: uses metadata to filter by time_start_utc and time_end_utc
            meta_path = getattr(entity_cfg, "metadata_file", None)
            if not meta_path:
                meta_path = getattr(sim_config, "meta_file", None)

            df = None
            meta = {}
            if meta_path:
                try:
                    # Try resolving relative path
                    actual_meta_path = Path(meta_path)
                    if not actual_meta_path.is_absolute():
                        # Try relative to config file
                        config_rel_path = (config_path.parent / actual_meta_path).resolve()
                        if config_rel_path.exists():
                            actual_meta_path = config_rel_path
                        else:
                            # Try as-is (relative to CWD)
                            actual_meta_path = actual_meta_path.resolve()

                    df = load_and_filter_data(
                        entity_cfg.input_file, actual_meta_path, entity_cfg.tag_id
                    )
                    meta = load_metadata(actual_meta_path, entity_cfg.tag_id)
                    logger.info(
                        f"  Filtered: {len(df)} records "
                        f"({meta['time_start_utc']} to {meta['time_end_utc']})"
                    )
                except Exception as e:
                    logger.warning(f"  Filtering failed: {e}. Falling back to full dataset.")

            if df is None:
                # Use robust loader for fallback
                df = pd.read_csv(
                    entity_cfg.input_file,
                    comment=";",
                    index_col=False,
                    engine="python",
                    on_bad_lines="warn",
                )
                logger.info(f"  Loaded {len(df)} records without filtering.")

            # Initialize stream and processor for this entity
            stream = SensorStream(sim_config, file_path=entity_cfg.input_file, data=df)
            processor = PostFactoProcessor(
                freq=entity_cfg.sampling_rate_hz,
                ahrs_cfg=entity_cfg.ahrs,
                cal_cfg=entity_cfg.calibration,
                depth_cfg=entity_cfg.depth,
                debug_level=debug_level,
                zmq_publisher=zmq_publisher,
                eid=registry.register(entity_cfg.sim_id, tag_id=entity_cfg.tag_id),
                sim_id=entity_cfg.sim_id,
                r_exact_mode=True,  # Lab Mode always uses acausal filters
            )
        except Exception as e:
            logger.error(f"  Failed to initialize entity {entity_cfg.sim_id}: {e}")
            import traceback

            logger.debug(traceback.format_exc())
            continue

        # Pass 1: Calibration
        logger.info("  Running Pass 1: Calibration...")
        if stream.data is None:
            logger.error(f"  No data available for entity {entity_cfg.sim_id}")
            continue

        records = stream.data.to_dict("records")
        for record in records:
            processor.process(cast(dict[str, Any], record))

        processor.calibrate_from_batch_data()
        logger.info("  Calibration complete.")

        # Pass 2: Processing
        logger.info("  Running Pass 2: Processing...")
        processor.reset()

        # Calculate delay for real-time playback if ZMQ is enabled
        playback_delay = 0.0
        if uncork:
            logger.info("  Uncorked mode enabled: Running at maximum speed")
        elif zmq_publisher and entity_cfg.sampling_rate_hz > 0:
            base_delay = 1.0 / entity_cfg.sampling_rate_hz
            playback_delay = base_delay / max(0.1, playback_speed)
            logger.info(
                f"  Real-time playback enabled: {playback_delay * 1000:.1f}ms per record "
                f"(Rate: {entity_cfg.sampling_rate_hz}Hz, Speed: {playback_speed}x)"
            )

        entity_results = []
        try:
            for i, record in enumerate(records):
                start_time = time.time()
                res = processor.process(cast(dict[str, Any], record))
                if res:
                    entity_results.append(res)

                if i % 1000 == 0:
                    print(f"  Processed {i}/{len(records)} records...", end="\r")

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
            logger.info("\nProcessing interrupted by user. Saving partial results...")

        # Save Results for this entity
        if entity_results:
            result_df = pd.DataFrame(entity_results)
            output_path = run_manager.get_output_path(f"{entity_cfg.sim_id}_output.csv")
            result_df.to_csv(output_path, index=False)
            logger.info(f"  Results saved to: {output_path}")
        else:
            logger.warning(f"  No results to save for {entity_cfg.sim_id}.")


class SimulationEntity:
    """Helper class to manage the processing pipeline for a single entity."""

    def __init__(
        self,
        entity_cfg: Any,
        eid: int,
        sim_config: Any,
        debug_level: int = 0,
        zmq_publisher: Any | None = None,
    ) -> None:
        self.config = entity_cfg
        self.eid = eid
        self.offset = entity_cfg.start_time_offset
        self.debug_level = debug_level

        # Initialize stream and processor
        self.stream = SensorStream(sim_config, file_path=entity_cfg.input_file)
        self.processor = PostFactoProcessor(
            freq=entity_cfg.sampling_rate_hz,
            ahrs_cfg=entity_cfg.ahrs,
            cal_cfg=entity_cfg.calibration,
            depth_cfg=entity_cfg.depth,
            debug_level=debug_level,
            zmq_publisher=zmq_publisher,
            eid=eid,
            sim_id=entity_cfg.sim_id,
        )
        self.iter = self.stream.stream()
        self.next_record: dict[str, Any] | None = None
        self.next_adj_ts: float = float("inf")

    def fetch_next(self) -> float:
        """Fetches the next record and calculates its adjusted timestamp."""
        try:
            self.next_record = next(self.iter)
            ts = float(self._extract_ts(self.next_record))
            self.next_adj_ts = ts + self.offset
            return float(self.next_adj_ts)
        except StopIteration:
            self.next_record = None
            self.next_adj_ts = float("inf")
            return self.next_adj_ts

    def _extract_ts(self, record: dict[str, Any]) -> float:
        """Extracts Unix timestamp from record."""
        ts_obj = record.get("DateTimeP")
        if isinstance(ts_obj, pd.Timestamp):
            return float(ts_obj.timestamp())

        date_val = record.get("Date", record.get('"Date"'))
        if date_val is not None:
            try:
                base_date = datetime(1899, 12, 30, tzinfo=timezone.utc)
                return (base_date + timedelta(days=float(date_val))).timestamp()
            except (ValueError, TypeError):
                pass
        return 0.0


def run_simulation_mode(
    pipeline_config: Any,
    debug_level: int = 0,
    uncork: bool = False,
    playback_speed: float = 1.0,
) -> None:
    """Executes the pipeline in Simulation Mode (Real-Time Streaming for multiple entities)."""
    # Setup logging (console only)
    setup_logging(None, debug_level)
    logger = logging.getLogger(__name__)

    sim_config = pipeline_config.simulation

    logger.info(f"Starting simulation in {pipeline_config.mode.value} mode")
    logger.info(f"Streaming {len(sim_config.entities)} entities on port {sim_config.zmq.port}")

    registry = EcosystemRegistry(meta_file=sim_config.meta_file)
    publisher = ZMQPublisher(sim_config)
    telemetry = TelemetryManager()

    # Initialize and Calibrate all entities
    pipelines: list[SimulationEntity] = []
    for entity_cfg in sim_config.entities:
        logger.info(f"Initializing entity: {entity_cfg.sim_id}")
        eid = registry.register(entity_cfg.sim_id, tag_id=entity_cfg.tag_id)

        # We use the view 'sim_id' as the primary key for ZMQ baggage reduction
        pipe = SimulationEntity(entity_cfg, eid, sim_config, debug_level, zmq_publisher=publisher)

        # Pass 1: Calibration (Acausal processor needs full dataset first)
        logger.info(f"  Performing calibration pass for {entity_cfg.sim_id}...")
        if pipe.stream.data is not None:
            for record in pipe.stream.data.to_dict("records"):
                record_dict = cast(dict[str, Any], record)
                pipe.processor.process(record_dict)
            pipe.processor.calibrate_from_batch_data()
            pipe.processor.reset()
        else:
            logger.warning(f"  No data found for {entity_cfg.id}, skipping calibration.")

        pipe.fetch_next()
        pipelines.append(pipe)

    # Initialize priority queue for timestamp-synchronized streaming
    # Heap stores: (adjusted_timestamp, entity_index)
    heap: list[tuple[float, int]] = []
    for i, pipe in enumerate(pipelines):
        if pipe.next_record:
            heapq.heappush(heap, (pipe.next_adj_ts, i))

    sim_start_time: float | None = None
    wall_start_time = time.time()
    last_telemetry_time = time.time()

    logger.info("Starting simulation loop...")
    try:
        while heap:
            # Pick the record with the earliest adjusted timestamp
            adj_ts, idx = heapq.heappop(heap)
            pipe = pipelines[idx]

            # Real-time pacing
            if not uncork:
                if sim_start_time is None:
                    sim_start_time = adj_ts

                sim_elapsed = (adj_ts - sim_start_time) / playback_speed
                wall_elapsed = time.time() - wall_start_time

                sleep_time = sim_elapsed - wall_elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

            # Process record (Pass 2)
            # Safe as we verified next_record exists before pushing to heap
            res = pipe.processor.process(cast(dict[str, Any], pipe.next_record))

            # Publish result
            if res:
                publisher.publish_state(pipe.eid, pipe.config.sim_id, res)

            # Update telemetry
            telemetry.update(time.time() - wall_start_time)
            if time.time() - last_telemetry_time >= 1.0:
                metrics = telemetry.get_metrics()
                publisher.publish("sim/telemetry", metrics)
                last_telemetry_time = time.time()

            # Load next record for this entity
            next_ts = pipe.fetch_next()
            if pipe.next_record:
                heapq.heappush(heap, (next_ts, idx))

    except KeyboardInterrupt:
        logger.info("\nSimulation interrupted by user.")
    finally:
        publisher.close()
        logger.info("Simulation shut down.")


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
        help="Override config values (e.g. --set simulation.playback_speed=2.0)",
    )
    run_parser.add_argument(
        "--uncork",
        action="store_true",
        help="Run without rate limiting (max speed). Equivalent to --speed <very high>",
    )
    run_parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Playback speed multiplier (default: 1.0). e.g. 2.0 = 2x real-time.",
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
            run_lab_mode(
                pipeline_config,
                args.config,
                args.debug_level,
                args.uncork,
                args.speed,
            )
        else:
            run_simulation_mode(pipeline_config, args.debug_level, args.uncork, args.speed)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
