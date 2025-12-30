# Technical Specification: `omni.biologger.subscriber`

**Status**: Draft
**Created**: 2025-12-30
**Parent Doc**: [Roadmap](./roadmap.md)

This technical specification outlines the architecture for a custom **Omniverse Kit Extension** that serves as the bridge between high-frequency biologger data and 3D rigged animal assets.

The core objective is to move data from a **ZeroMQ (ZMQ)** stream into the **USD Fabric** (runtime memory) at low latency, ensuring that the 3D model, sensor telemetry, and behavioral predictions remain in lockstep for the researcher.

---

## 1. Architectural Overview

The extension operates as an asynchronous background service within **Omniverse USD Composer**. It decouples the simulation/processing logic (running on a separate machine or process) from the rendering viewport.

**Data Flow:**

1. **ZMQ Socket**: Listens for `PUB` packets containing Quaternions, Depth, and Saliency triggers.
2. **Logic Engine**: A non-blocking Python thread parses JSON/Binary packets.
3. **Fabric Writer**: Injects pose data directly into the **USD Fabric** layer for sub-millisecond updates to the Prim (3D shark/swordfish).

---

## 2. Implementation Requirements

### A. Asynchronous Subscription Thread

To prevent UI "hitching," the subscriber must run in a separate `asyncio` loop or a dedicated thread.

* **Mechanism**: `ZMQ SUB` socket.
* **Port**: Configurable (Default: `5555`).
* **Heartbeat**: Monitor for packet loss to trigger "Data Lost" HUD overlay.

### B. USD Fabric (USDRT) Integration

Using standard USD APIs for 50Hz+ movement causes significant overhead. This extension will use **Fabric** to bypass the scene graph's "dirtying" mechanism.

* **Target**: `UsdGeom.Xform` attributes of the model's `Root_Bone`.
* **Latency Goal**: Update transform data within the same frame as the `kit.update` event.

### C. Multi-Modal Clock Synchronization

The extension must handle the "Scrubbing" use case by mapping the ZMQ timestamp to the Omniverse timeline.

* **Sync Logic**: When the user scrubs the timeline, the extension sends a `SEEK_TO` command back to the processing engine (or fetches the corresponding frame from the local cache).
* **Interpolation**: If IMU data is 100Hz but rendering is 60Hz, use **NVIDIA Warp** for on-the-fly Slerp (Spherical Linear Interpolation) of quaternions to ensure visual smoothness.

---

## 3. Component Breakdown

| Module | Technical Function |
| --- | --- |
| **`subscriber.py`** | Manages the ZMQ context and listens for the data payload (JSON/Protobuf). |
| **`fabric_bridge.py`** | Uses `omni.usd.get_watcher` and `usdrt` to write pose data to the Fabric layer. |
| **`behavior_hud.py`** | An `omni.ui` overlay displaying real-time ethogram features (e.g., "VeDBA", "Saliency Score"). |
| **`video_sync.py`** | A secondary viewport window that decodes and displays the synchronized POV video frame. |

---

## 4. Proposed Payload Structure

The extension expects a ZMQ packet adhering to the following structure to ensure multi-animal scalability:

```json
{
  "animal_id": "swordfish_01",
  "timestamp": 1703894400.123,
  "transform": {
    "quat": [0.707, 0.0, 0.707, 0.0], // Orientation
    "position": [x, y, depth]         // Dead-reckoned position
  },
  "behavior": {
    "class": "FORAGING",
    "confidence": 0.89,
    "is_salient": true                // Triggers recording/highlighting
  }
}
```

---

## 5. Near-Term Project Milestone: "The Cube Mover"

To validate this spec for funding, our first technical deliverable will be a **"Hello World" Extension**:

1. A standalone Python script sends random Quaternions via ZMQ.
2. The Omniverse Extension listens to that port and moves a 3D Cube in the viewport.
3. **Success Metric**: Zero visual stutter and <10ms latency between the script and the viewport movement.
