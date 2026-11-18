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
     - Linear Loop (one entity after another)
     - C-Merged Time Loop (Multi-Entity)
   * - **Networking**
     - ZMQ publishing on by default (``publish_zmq``); off for ``export-track``
     - ZMQ publishing on by default (MessagePack batches on a PUB socket)

Event Loop: The "Scream" Architecture
-------------------------------------

To support scalable multi-animal simulation in pure Python, we utilize a **Time-Sorted Merge** architecture rather than a manual priority queue.

Prior Approach (Slow)
~~~~~~~~~~~~~~~~~~~~~
The naive implementation used a Python ``while`` loop with ``heapq.heappush`` and ``heapq.heappop`` for every single record to maintain time synchronization between entities.

*   **Overhead**: O(log K) per record *in Python interpreter steps*.

Current Approach (Fast)
~~~~~~~~~~~~~~~~~~~~~~~
We now use `heapq.merge <https://docs.python.org/3/library/heapq.html#heapq.merge>`_, which is a C-optimized generator.

1.  **Generators**: Each ``SimulationEntity`` yields a lazy stream of ``(timestamp, index, record)`` tuples.
2.  **C-Merge**: ``heapq.merge(*streams)`` consumes these streams and performs the K-way merge sort entirely in C space.
3.  **Python Loop**: The main loop simply iterates over this pre-sorted stream, dispatching records to processors.

.. code-block:: text

   Entity 1 stream --(ts, rec)--+
   Entity 2 stream --(ts, rec)--+--> heapq.merge --> main loop --> processor 1 .. N
   Entity N stream --(ts, rec)--+                              \--> ZMQ publisher

The merge still costs O(log K) comparisons per record for K entities, but they run in C rather
than as interpreter steps.
