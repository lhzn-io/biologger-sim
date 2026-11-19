Simulation Architecture
=======================

``biologger-sim`` runs in two modes: high-throughput batch processing (Lab Mode) and real-time
visualization (Simulation Mode).

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

To simulate many animals at once in pure Python, the event loop uses a **Time-Sorted Merge**
instead of a manual priority queue.

Prior Approach (Slow)
~~~~~~~~~~~~~~~~~~~~~
The first implementation kept the entities in time order with a Python ``while`` loop that called
``heapq.heappush`` and ``heapq.heappop`` for every record.

*   **Overhead**: O(log K) per record *in Python interpreter steps*.

Current Approach (Fast)
~~~~~~~~~~~~~~~~~~~~~~~
The current loop uses `heapq.merge <https://docs.python.org/3/library/heapq.html#heapq.merge>`_,
a generator implemented in C.

1.  **Generators**: Each ``SimulationEntity`` yields a lazy stream of
    ``(timestamp, index, record)`` tuples.
2.  **C-Merge**: ``heapq.merge(*streams)`` consumes the streams and runs the K-way merge sort
    entirely in C.
3.  **Python Loop**: The main loop iterates over the sorted stream and dispatches each record to
    the processors.

.. code-block:: text

   Entity 1 stream --(ts, idx, rec)--+
   Entity 2 stream --(ts, idx, rec)--+--> heapq.merge --> main loop --> processor 1 .. N
   Entity N stream --(ts, idx, rec)--+                              \--> ZMQ publisher

The merge still costs O(log K) comparisons per record for K entities, but they run in C rather
than as interpreter steps.
