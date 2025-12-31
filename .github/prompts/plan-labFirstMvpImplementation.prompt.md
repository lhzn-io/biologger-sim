# Plan: Final Sprint Plan for biologger-sim (MVP Implementation)

**Summary**: Implement a **Lab-first → Visualization → Sim-progression architecture** with exact R column-by-column validation, Feather format optimization for 4TB SSD, complete config+provenance capture (YAML + repo hash), and optional diagnostic visualization controlled via CLI/config. All test datasets (stable_period, attachment_angle_validation, early_deployment with newly-generated R diagnostics) are ready for validation.

## Steps

1. **Create test infrastructure with slow/baseline markers** — Set up `tests/unit/` for fast component tests (~10s), `tests/integration/` for full-pipeline baseline validation, implement `@pytest.mark.slow` and `@pytest.mark.requires_baseline` markers to separate fast/slow suites, create fixtures loading test datasets from [biologger-pseudotrack/data/test/](biologger-pseudotrack/data/test/) (stable_period, attachment_angle_validation, early_deployment), implement relative floating-point comparison for orientation angles (±0.1% tolerance, ±0.01° for pitch/roll).

2. **Port postfacto Lab pipeline with validation** — Implement `src/biologger_sim/processors/lab.py` and utilities (rotation.py, filtering.py, magnetometer.py, kalman.py, dead_reckoning.py) from [biologger-pseudotrack/postfacto](biologger-pseudotrack/biologger_pseudotrack/postfacto/), generate exact 34-column diagnostic output matching R baseline schema, add integration test comparing Lab outputs to stable_period R baseline within tolerance (primary validation).

3. **Add Feather format with config+provenance metadata** — Update [stream.py](src/biologger_sim/io/stream.py) for auto-detection/loading of `.feather` files, implement metadata storage: `deployment_id`, `pipeline_version`, `processing_timestamp`, `attachment_angles`, `mag_offsets`, `source_config_yaml`, `repo_commit_hash`, `src_md5sum` (full src/ directory hash for reproducibility), auto-convert CSV→Feather on first access, configure Lab output to Feather by default (>100MB datasets), add CLI `biologger-sim convert <input.csv> [--output out.feather]`.

4. **Integrate visualization in `src/biologger_viz/`** — Create modular backends (headless default: matplotlib/plotly figures saved to `figures/`; optional ZMQ broadcaster for external Omniverse consumers), add `visualize: true/false` config option and `--visualize` CLI flag, make viz an optional extra (`pip install biologger-sim[viz]` adds pyzmq, plotly, matplotlib), design interfaces ready for future `biologger-viz` repo refactor.

5. **Implement pluggable AHRS with runtime config** — Add `ahrs_algorithm: [TILT_COMPENSATION, MADGWICK_ACCEL_MAG, MAHONY, EKF]` enum to config, create `src/biologger_sim/processors/ahrs/` module with interchangeable implementations, port streaming tilt compensation to `ahrs/tilt.py` as Phase-1 baseline, design interface supporting GPU/CUDA variants.

6. **Add telemetry, logging, and multiprocessing roadmap** — Initialize `PerformanceTelemetry` in [**main**.py](src/biologger_sim/__main__.py) (logs/‹deployment_id›_‹timestamp›_logs/ with messages and telemetry.csv), configure Lab to output mag calibration (offset, radius, hard-iron) to log and CSV, document roadmap: multiprocessing.Pool for parallel pipeline configs on CPU, CUDA kernels for GPU acceleration (Phase 2).

## Further Considerations

1. **Test Suite Organization**: Should baseline validation tests live in separate file (e.g., `tests/integration/test_lab_baseline.py`) marked with `@pytest.mark.slow` and `@pytest.mark.requires_baseline`, so developers can run `pytest tests/unit/` for fast feedback and `pytest -m slow` for full validation?

2. **Config YAML Storage Strategy**: Should the stored YAML be the exact input config file, or a "flattened" version with all defaults resolved? For reproducibility, should we also capture environment.yml hash or just src_md5sum?

3. **Visualization Output Locations**: Should diagnostic plots be saved to `figures/‹deployment_id›_‹timestamp›/` with subdirectories (timeseries/, orientation/, trajectory/), or a single flat directory structure?

4. **Multiprocessing Roadmap Detail**: Should config support a `parallel: {enabled: true, num_workers: 4, backends: [cpu, cuda]}` section, with results aggregated into single output file or separate per-config outputs?

## Implementation Roadmap

### Phase 1: Lab Mode MVP (Weeks 1-3)

- [x] Create test infrastructure with pytest markers
- [x] Port postfacto pipeline from biologger-pseudotrack
- [ ] Add Feather format with metadata storage
- [x] Integrate Lab mode validation against R baselines
- [x] Output telemetry and logging (Logging implemented, Telemetry pending)

### Phase 2: Visualization & Config (Weeks 4-5)

- [ ] Implement `src/biologger_viz/` with headless/optional backends
- [ ] Add `--visualize` CLI flag and config option
- [ ] Create diagnostic plot generation (timeseries, orientation, trajectory)
- [ ] Make visualization an optional extra dependency

### Phase 3: Sim Progression (Weeks 6-8)

- [ ] Implement pluggable AHRS configuration
- [ ] Port streaming tilt compensation (Phase-1 baseline)
- [ ] Port Madgwick accel+mag variant
- [ ] Compare Sim vs Lab divergence in real-time

### Phase 4: Advanced Features (Phase 2+)

- [ ] Document multiprocessing architecture for parallel pipeline configs
- [ ] GPU/CUDA acceleration roadmap
- [ ] Refactor visualization to separate `biologger-viz` repo
- [ ] Full Mahony + Extended Kalman implementations

## Decisions Made

1. **Test Suite**: Baseline validation tests in separate `test_lab_baseline.py` with `@pytest.mark.slow` marker, enabling fast unit testing and full validation independently.

2. **Config Storage**: Store exact input YAML + src_md5sum for full reproducibility; optionally capture environment.yml hash in metadata.

3. **Visualization Output**: `figures/‹deployment_id›_‹timestamp›/` with subdirectories (timeseries/, orientation/, trajectory/) for organized output.

4. **Multiprocessing**: Phase 2+ feature; document architecture as separate roadmap item for future parallel/CUDA acceleration.

5. **AHRS Progression**: Start with streaming tilt compensation, validate each step, progressively add Madgwick → Mahony → EKF driven by literature review and validation results.

## Success Criteria

- ✓ Lab mode outputs exactly match R baseline CSV within ±0.01° orientation tolerance
- ✓ All three test datasets pass integration validation
- ✓ Feather format outputs with complete provenance metadata
- ✓ Optional visualization working with CLI/config flags
- ✓ PerformanceTelemetry logging shows sub-millisecond per-frame processing
- ✓ AHRS configuration pluggable and testable for future variants
- ✓ Documentation includes multiprocessing roadmap for Phase 2
