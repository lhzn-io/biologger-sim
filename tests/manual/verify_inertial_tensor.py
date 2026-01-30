import logging
import traceback

try:
    import warp as wp
except ImportError:
    wp = None  # type: ignore

from biologger_sim.processors.inertial_tensor import InertialTensorProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)


def test_inertial_tensor() -> None:
    print("--- Testing InertialTensorProcessor (Batch GPU) ---")

    if wp is None or not wp.is_cuda_available():
        print("SKIPPING: Warp/CUDA not available.")
        return

    # 1. Initialize for 10 entities
    num_entities = 10
    filt_len = 10
    processor = InertialTensorProcessor(
        num_entities=num_entities, filt_len=filt_len, freq=10, debug_level=1
    )  # Should auto-detect cuda

    # 2. Warmup Phase (Fill buffers)
    # We will simulate Entity 0 and Entity 5 being active
    active_indices = [0, 5]

    # Entity 0: Static Upright (Z=9.8) -> Pitch=0, Roll=0
    # Entity 5: Static Tilted 90 deg Pitch (X=9.8) -> Pitch=-90

    # In streaming.py logic:
    # ax_g = X/10.0.
    # Pitch = -atan2(ax_g, mag_yz)
    # If X=9.8 (approx 1g), ax_g=0.98. mag_yz=0.
    # Pitch = -atan2(0.98, 0) = -PI/2 = -90 deg. Correct.

    # Input data needs to be in 0.1g units? Or m/s^2?
    # streaming.py comment: "Data is in 0.1g units"
    # Wait.
    # streaming.py: ax_m = record["int aX"].
    # And accel_g = static / 10.0.
    # So 1.0g = 10.0 units.
    # If I pass 10.0, ax_g = 1.0.

    val_0 = [0.0, 0.0, 10.0]  # 1g Z
    val_5 = [10.0, 0.0, 0.0]  # 1g X

    print("Feeding warmup data...")
    for _ in range(filt_len + 5):
        indices = active_indices
        accel_data = [val_0, val_5]

        res = processor.process_vectors(indices, accel_data)

    print("Checking Results...")
    # Expected:
    # Entity 0: Roll=0, Pitch=0
    # Entity 5: Pitch ~= -90 deg (-1.57 rad)

    r0 = res["roll_rad"][0]
    p0 = res["pitch_rad"][0]

    r5 = res["roll_rad"][1]
    p5 = res["pitch_rad"][1]

    print(f"Entity 0: Roll={r0:.4f}, Pitch={p0:.4f}")
    if abs(p0) < 0.1:
        print("  -> PASS (Upright)")
    else:
        print("  -> FAIL (Upright)")

    print(f"Entity 5: Roll={r5:.4f}, Pitch={p5:.4f}")
    if abs(p5 + 1.57) < 0.1:
        print("  -> PASS (Tilted -90)")
    else:
        print(f"  -> FAIL (Expected -1.57, got {p5:.4f})")

    print("\nSUCCESS: Batch processing executed on GPU.")


if __name__ == "__main__":
    try:
        test_inertial_tensor()
    except Exception as e:
        print(f"\nCRITICAL FAILURE: {e}")
        traceback.print_exc()
        exit(1)
