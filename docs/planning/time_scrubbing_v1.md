# Time Scrubbing & Replay Implementation Plan

## 1. Current State Assessment

- **Existing Variables**: `_replay_live_time` and `_replay_playhead` exist in `CreateSetupExtension` but are currently unused validation markers.
- **Data Flow**: The extension consumes ZMQ messages in real-time (`_zmq_listener_loop`) and updates the scene immediately (`_update_prim`).
- **Missing Components**:
  - No History Buffer: Past states are discarded immediately after rendering.
  - No Timeline Integration: The Omni Timeline is not driven by incoming data, nor does it drive the simulation.
  - No Interpolation: The system relies on high-frequency ZMQ updates for smoothness.

## 2. Web Research: Omniverse Timeline Integration

Based on research into the `omni.timeline` extension API (Kit 104+):

- **Interface**: `omni.timeline.get_timeline_interface()` provides control.
- **Key Methods**:
  - `set_start_time(t)` / `set_end_time(t)`: Adjusts the slider bounds.
  - `set_current_time(t)`: Moves the playhead programmatically.
  - `get_current_time()`: Reads the playhead position (for scrubbing).
- **Events**: `get_timeline_event_stream()` allows subscribing to `PLAY`, `PAUSE`, and time change events to detect manual user scrubbing.

## 3. Implementation Plan

### Phase 1: Data History Infrastructure

**Objective**: Persist state over time to allow lookup.

1. **History Structure**:
    - Add `self._entity_history: Dict[int, List[Dict]]` to `CreateSetupExtension`.
    - Store tuples of `(timestamp, physics_state, rotation_data)` for each EID.
    - **Optimization**: Use `bisect` for O(log n) lookups during playback. Limit buffer size (e.g., last 10 minutes or 1GB limit) to prevent memory leaks.

2. **Recording Loop**:
    - Modify `_zmq_listener_loop`:
        - On valid packet receipt, append data to `_entity_history[eid]`.
        - Call `self._timeline_iface.set_end_time(latest_ts)` to expand the seek bar.

### Phase 2: Timeline Integration & Replay Logic

**Objective**: Connect the UI slider to the data.

1. **Live vs. Replay Mode**:
    - Refactor `_update_prim` to respect the "Live Sync" checkbox.
    - **Live Mode** (Current behavior):
        - Force Timeline Time -> `latest_timestamp`.
        - Render `_latest_physics_data`.
        - *Auto-Exit*: If user manually drags the slider (detected via `TimelineEventType.CURRENT_TIME_CHANGED` or explicit drift), uncheck "Live Sync".
    - **Replay Mode**:
        - Read `t = timeline.get_current_time()`.
        - **Query**: Find the two history frames surrounding `t` (Frame A and Frame B).
        - **Interpolate**:
            - **Position**: Linear Interpolation (Lerp) of `px, py, depth`.
            - **Rotation**: Spherical Linear Interpolation (Slerp) of Quaternions (using `pxr.Gf.Slerp`).
        - **Update**: Inject interpolated state into `self._entities_state`.

2. **Visual Feedback**:
    - ensure trails (if active) match the replay state (tricky, might reset trails on scrub or just let them be). *Decision: For V1, simple trails might look weird during scrubbing. We'll leave them as-is for now.*

### Phase 3: Code Structure

- **New Methods**:
  - `_record_history(eid, timestamp, data)`
  - `_get_interpolated_state(eid, query_time) -> dict`
  - `_on_timeline_event(event)`

## 4. Testing Plan

### Test Case A: Live Sync Continuity

1. Start Simulation.
2. Ensure "Live Sync" is CHECKED.
3. Observe the Timeline slider automatically moving forward as data arrives.
4. Verify simulated animals are moving smoothly.

### Test Case B: Manual Scrubbing

1. Uncheck "Live Sync" (or just grab the slider).
2. Drag the slider BACKWARDS 10 seconds.
3. **Expected Result**:
    - "Live Sync" unchecks automatically.
    - Animals "rewind" to their previous positions smoothly.
    - The view updates interactively while dragging.

### Test Case C: Replay Playback

1. Drag slider back.
2. Press "Play" on the Omniverse Timeline (Spacebar).
3. **Expected Result**: The simulation plays forward from that point at 1x speed (or whatever speed is set in Omniverse), deriving motion from the history buffer.

### Test Case D: Return to Live

1. Check "Live Sync".
2. **Expected Result**: Timeline jumps to the end; animals snap to current live position.
