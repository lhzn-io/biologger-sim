import time

import numpy as np
from scipy.signal import lfilter, lfilter_zi


def test_lfilter_single() -> None:
    b = np.array([0.1, 0.2, 0.1])
    a = np.array([1.0, -0.5, 0.1])
    zi = lfilter_zi(b, a) * 0.0

    start = time.time()
    for _ in range(100000):
        _, zi = lfilter(b, a, [1.0], zi=zi)
    end = time.time()
    print(f"lfilter (single sample): {100000 / (end - start):.0f} sps")


def test_manual_filt() -> None:
    b = [0.1, 0.2, 0.1]
    a = [1.0, -0.5, 0.1]
    # Direct Form II Transposed (what lfilter uses)
    s1, s2 = 0.0, 0.0

    start = time.time()
    for _ in range(100000):
        x = 1.0
        y = b[0] * x + s1
        s1 = b[1] * x - a[1] * y + s2
        s2 = b[2] * x - a[2] * y
    end = time.time()
    print(f"Manual filter: {100000 / (end - start):.0f} sps")


if __name__ == "__main__":
    test_lfilter_single()
    test_manual_filt()
