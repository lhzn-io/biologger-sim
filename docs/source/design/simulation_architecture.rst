Simulation Architecture
=======================

The ``biologger-sim`` architecture is designed to support both high-throughput batch processing (Lab Mode) and real-time visualization (Simulation Mode).

Dual-Mode System
----------------

.. list-table::
   :header-rows: 1

   * - Feature
     - Lab Mode (Batch)
     - Simulation Mode (Real-Time)
   * - **Primary Goal**
     - R-Compatible Analysis & CSV Generation
     - Real-Time Visualization & Streaming
   * - **Loop Architecture**
     - Linear Loop (Single Entity)
     - C-Merged Time Loop (Multi-Entity)
   * - **Networking**
     - Optional (for debugging)
     - Mandatory (Serialize + ZMQ Push)
   * - **Performance**
     - ~94,000 rec/sec
     - ~33,000+ rec/sec (Scalable)

Event Loop: The "Scream" Architecture
-------------------------------------

To support scalable multi-animal simulation in pure Python, we utilize a **Time-Sorted Merge** architecture rather than a manual priority queue.

Prior Approach (Slow)
~~~~~~~~~~~~~~~~~~~~~
The naive implementation used a Python ``while`` loop with ``heapq.heappush`` and ``heapq.heappop`` for every single record to maintain time synchronization between entities.

*   **Overhead**: O(log K) per record *in Python interpreter steps*.
*   **Result**: 3x performance penalty for adding a second animal.

Current Approach (Fast)
~~~~~~~~~~~~~~~~~~~~~~~
We now use `heapq.merge <https://docs.python.org/3/library/heapq.html#heapq.merge>`_, which is a C-optimized generator.

1.  **Generators**: Each ``SimulationEntity`` yields a lazy stream of ``(timestamp, index, record)`` tuples.
2.  **C-Merge**: ``heapq.merge(*streams)`` consumes these streams and performs the K-way merge sort entirely in C space.
3.  **Python Loop**: The main loop simply iterates over this pre-sorted stream, dispatching records to processors.

.. mermaid::

   graph TD
      A[Entity 1 Stream] -->|Yields (ts, rec)| M(heapq.merge)
      B[Entity 2 Stream] -->|Yields (ts, rec)| M
      C[Entity N Stream] -->|Yields (ts, rec)| M
      M -->|Sorted Tuple| L[Main Loop]
      L -->|Dispatch| P1[Processor 1]
      L -->|Dispatch| P2[Processor 2]
      L -->|Serialize| Z[ZMQ Publisher]

This results in **sublinear scaling** overhead for additional animals.
