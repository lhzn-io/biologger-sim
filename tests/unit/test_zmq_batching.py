# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""ZMQPublisher batches state samples into "<topic>/batch" messages."""

from types import SimpleNamespace
from typing import Any

import msgpack
import pytest

from biologger_sim.io import zmq_publisher as zp


class FakeSocket:
    def __init__(self) -> None:
        self.sent: list[list[bytes]] = []
        self.options: dict[int, int] = {}

    def send_multipart(self, frames: list[bytes]) -> None:
        self.sent.append(frames)

    def setsockopt(self, option: int, value: int) -> None:
        self.options[option] = value

    def close(self) -> None:
        pass


def make_publisher() -> tuple[zp.ZMQPublisher, FakeSocket]:
    pub = object.__new__(zp.ZMQPublisher)
    socket = FakeSocket()
    pub.config = SimpleNamespace(zmq=SimpleNamespace(topic="sim/state"))  # type: ignore[assignment]
    pub.debug_level = 0
    pub.socket = socket  # type: ignore[assignment]
    pub.context = SimpleNamespace(term=lambda: None)  # type: ignore[assignment]
    pub._id_to_species = {}
    pub._batch = []
    pub._batch_started = 0.0
    return pub, socket


def state(ts: float) -> dict[str, Any]:
    return {"timestamp": ts, "Depth": 10.0, "pseudo_x": 1.0, "pseudo_y": 2.0}


def unpack(frames: list[bytes]) -> list[dict[str, Any]]:
    assert frames[0] == b"sim/state/batch"
    batch: list[dict[str, Any]] = msgpack.unpackb(frames[1], raw=False)["batch"]
    return batch


def test_samples_wait_for_the_interval_then_go_together(monkeypatch: pytest.MonkeyPatch) -> None:
    now = [100.0]
    monkeypatch.setattr(zp.time, "monotonic", lambda: now[0])
    pub, socket = make_publisher()
    pub.publish_state(0, "sim", None, state(1.0))
    now[0] += zp.BATCH_INTERVAL_S / 2
    pub.publish_state(0, "sim", None, state(2.0))
    assert socket.sent == []
    now[0] += zp.BATCH_INTERVAL_S
    pub.publish_state(0, "sim", None, state(3.0))
    assert [s["ts"] for s in unpack(socket.sent[0])] == [1.0, 2.0, 3.0]


def test_a_full_batch_is_sent_at_once(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(zp.time, "monotonic", lambda: 0.0)
    pub, socket = make_publisher()
    for i in range(zp.BATCH_MAX):
        pub.publish_state(0, "sim", None, state(float(i)))
    assert len(socket.sent) == 1
    assert len(unpack(socket.sent[0])) == zp.BATCH_MAX


def test_close_sends_the_last_partial_batch() -> None:
    pub, socket = make_publisher()
    pub.publish_state(0, "sim", None, state(1.0))
    pub.close()
    assert [s["ts"] for s in unpack(socket.sent[0])] == [1.0]
    assert pub._batch == []
