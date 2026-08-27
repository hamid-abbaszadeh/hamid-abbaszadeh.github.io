---
layout: default
title: "Memory Barriers and Memory Ordering Models in C++"
parent: "Multithreading"
nav_order: 1
---

# Memory Barriers and Memory Ordering Models in C++

Explore the hardware-level mechanics of CPU caches, instruction reordering, and memory barriers, and master the 6 C++ `std::memory_order` options to write safe, high-performance concurrent code.
<span class="label label-blue">Modern C++</span><span class="label label-green">C++11 / C++17 / C++20</span><span class="label label-purple">Multithreading</span><span class="label label-red">Performance</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Core Concept: Caches, Instruction Reordering, and Hardware Reality

In modern multi-core architectures, threads do not read from or write directly to main system RAM on every instruction. Each CPU core possesses its own private high-speed L1 and L2 caches, along with store buffers (write buffers).

![Memory Diagram]({{ site.baseurl }}/assets/images/cpu-diagram.png)
```
+------------------------------------+       +------------------------------------+
|               CORE 0               |       |               CORE 1               |
|  [ Registers ]                     |       |  [ Registers ]                     |
|        |                           |       |        |                           |
|  [ Store Buffer / Execution Pipeline ]     |  [ Store Buffer / Execution Pipeline ]
|        |                           |       |        |                           |
|  [ Private L1 / L2 Cache ]         |       |  [ Private L1 / L2 Cache ]         |
+-----------------+------------------+       +-----------------+------------------+
                  |                                            |
                  +---------------------+----------------------+
                                        |
                          [ Shared L3 Cache / Main RAM ]
```

This hardware architecture introduces two critical multithreading challenges:

1. **Cache Incoherency & Stale Data:** When Thread A running on Core 0 writes a value to memory, the updated value sits inside Core 0's store buffer or private L1 cache before flushing to main memory. Thread B running on Core 1 reading that same memory address will read its own stale local cache copy, seeing an outdated reality.
2. **Instruction Reordering:** To maximize instruction-level parallelism, both the C++ compiler and the CPU execution pipeline aggressively reorder reads and writes. The compiler/CPU guarantees that code execution appears sequential **within a single thread**, but it makes zero guarantees about the visibility order of those operations across **other concurrently running threads**.

**Memory Barriers (also called Memory Fences)** are specialized CPU instructions that restrict instruction reordering and force private store buffers to flush and invalidate local caches. This ensures operations executed before the fence are made visible to all cores before any operations after the fence are executed.

---

## Types of Hardware Memory Barriers

At the processor instruction set level, memory barriers fall into three fundamental categories:

* **Store (Write) Barrier:** Guarantees that all store/write operations issued *before* the barrier are flushed from local store buffers to shared memory *before* any write operations issued *after* the barrier are allowed to execute.
* **Load (Read) Barrier:** Guarantees that all load/read operations issued *before* the barrier are fully completed *before* any load operations issued *after* the barrier are allowed to execute, invalidating local stale cache lines.
* **Full Barrier:** Acts as both a Store and a Load barrier simultaneously. It enforces that all prior memory operations (reads and writes) complete fully before any subsequent memory operations are executed.

---

## C++ Memory Ordering Models (`<atomic>`)

C++ provides 6 explicit enum options in the `<atomic>` header under `std::memory_order` to specify exact hardware fence behavior and visibility constraints:

1. `std::memory_order_relaxed`
2. `std::memory_order_release`
3. `std::memory_order_acquire`
4. `std::memory_order_acq_rel`
5. `std::memory_order_seq_cst`
6. `std::memory_order_consume` (Deprecated / discouraged in modern standard practice due to implementation challenges).

---

### 1. `std::memory_order_relaxed`

#### Core Behavior
`std::memory_order_relaxed` places zero cross-thread ordering synchronization or memory fence constraints on surrounding memory reads and writes.

#### What It Guarantees
It guarantees **atomicity** (no data races or torn reads/writes on the atomic variable itself) and **modification order consistency** (all threads see modifications to *that specific atomic variable* in the exact same order).

#### Issue It Solves
It eliminates expensive hardware memory fence overhead when you need thread-safe updates to an isolated variable (like an internal counter) without synchronizing other non-atomic payloads.

{% highlight cpp %}
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>

std::atomic<int> global_counter{0};

void increment_task() {
    for (int i = 0; i < 1000; ++i) {
        // ISSUE SOLVED: Prevents data race / torn writes during multi-threaded increment.
        // DOES NOT SOLVE: Ordering of adjacent non-atomic memory operations.
        global_counter.fetch_add(1, std::memory_order_relaxed);
    }
}

int main() {
    std::vector<std::thread> threads;
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back(increment_task);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Final counter: " << global_counter.load(std::memory_order_relaxed) << "
";
    return 0;
}
{% endhighlight %}

---

### 2. `std::memory_order_release`

#### Core Behavior
Acts as a **Store (Write) Barrier**. It must be combined with a store/write operation on an atomic variable.

#### What It Guarantees
No memory reads or writes in the current thread can be reordered by the compiler or CPU *after* this store operation. All writes committed before this release store are guaranteed to become visible to any thread performing a matching **Acquire** load on the same atomic variable.

#### Issue It Solves
Prevents publishing incomplete payload data to other threads. Without a release barrier, the payload creation writes could be reordered to occur *after* the flag store operation, causing consumer threads to process unitialized data.

{% highlight cpp %}
#include <iostream>
#include <atomic>
#include <thread>
#include <string>

std::string shared_payload;
std::atomic<bool> data_ready{false};

void producer_thread() {
    // Non-atomic memory write
    shared_payload = "Heavy initialization data payload";

    // ISSUE SOLVED: Prevents compiler/CPU from reordering 'shared_payload' write 
    // to occur AFTER 'data_ready' is published.
    data_ready.store(true, std::memory_order_release);
}

void consumer_thread() {
    // Wait for data
    while (!data_ready.load(std::memory_order_acquire)) {
        std::this_thread::yield();
    }

    // Safe to consume shared_payload here
    std::cout << "Payload: " << shared_payload << "
";
}

int main() {
    std::thread t1(producer_thread);
    std::thread t2(consumer_thread);

    t1.join();
    t2.join();
    return 0;
}
{% endhighlight %}

---

### 3. `std::memory_order_acquire`

#### Core Behavior
Acts as a **Load (Read) Barrier**. It must be applied to a load/read operation on an atomic variable.

#### What It Guarantees
No memory reads or writes in the current thread can be reordered *before* this load operation. When this load reads the value stored by a matching `std::memory_order_release` write, all memory writes committed before that release store become fully visible to the loading thread.

#### Issue It Solves
Prevents speculative execution or pre-fetching of payload reads. Without an acquire barrier, the consumer thread could speculatively read `shared_payload` from its stale L1 cache line *before* checking if `data_ready` is true.

{% highlight cpp %}
#include <iostream>
#include <atomic>
#include <thread>
#include <cassert>

int payload_data = 0;
std::atomic<bool> ready_flag{false};

void producer() {
    payload_data = 42;
    ready_flag.store(true, std::memory_order_release);
}

void consumer() {
    // ISSUE SOLVED: Prevents compiler/CPU from speculatively loading 'payload_data'
    // BEFORE reading 'ready_flag'.
    while (!ready_flag.load(std::memory_order_acquire)) {
        // Spin lock wait
    }

    // Guaranteed to read 42
    std::cout << "Data read successfully: " << payload_data << "
";
    assert(payload_data == 42);
}

int main() {
    std::thread t1(producer);
    std::thread t2(consumer);

    t1.join();
    t2.join();
    return 0;
}
{% endhighlight %}

---

### 4. `std::memory_order_acq_rel`

#### Core Behavior
Combines both **Acquire** and **Release** semantics into a single operation. It is applied exclusively to Read-Modify-Write (RMW) atomic operations such as `fetch_add`, `fetch_sub`, or `compare_exchange_strong`.

#### What It Guarantees
* **Acquire part:** Prevents surrounding reads/writes from being reordered before this RMW operation.
* **Release part:** Prevents surrounding reads/writes from being reordered after this RMW operation.
* Synchronizes memory across both prior writer threads and subsequent reader threads.

#### Issue It Solves
Solves race conditions in lock-free concurrent data structures (like reference counting, lock-free queues, or spinlocks) where a thread must simultaneously acquire a resource lock while releasing an existing pipeline stage.

{% highlight cpp %}
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>

std::atomic<int> ref_count{1};

void release_reference() {
    // ISSUE SOLVED: Synchronizes both previous modifications (Release) 
    // and subsequent destruction logic (Acquire) atomically during decrement.
    if (ref_count.fetch_sub(1, std::memory_order_acq_rel) == 1) {
        std::cout << "Last reference released. Safe to delete resource.
";
    }
}

int main() {
    ref_count.fetch_add(1, std::memory_order_relaxed); // Total 2 references

    std::thread t1(release_reference);
    std::thread t2(release_reference);

    t1.join();
    t2.join();
    return 0;
}
{% endhighlight %}

---

### 5. `std::memory_order_seq_cst`

#### Core Behavior
Enforces **Sequential Consistency**. This is the **default memory order** used by all atomic operations in C++ if no order parameter is specified.

#### What It Guarantees
It provides Acquire/Release guarantees AND enforces a **single, global, universally agreed-upon execution timeline** for all `seq_cst` operations across every CPU core in the system. All threads observe every `seq_cst` atomic modification in the exact same sequence.

#### Issue It Solves
Prevents non-intuitive execution state anomalies where two threads simultaneously write to separate atomic flags and then fail to see each other's writes due to store-buffer latency (Dekker's Algorithm / Peterson's Algorithm failures).

{% highlight cpp %}
#include <iostream>
#include <atomic>
#include <thread>
#include <cassert>

std::atomic<bool> x{false};
std::atomic<bool> y{false};
std::atomic<int> z{0};

void write_x() {
    // Default is std::memory_order_seq_cst
    x.store(true, std::memory_order_seq_cst);
}

void write_y() {
    y.store(true, std::memory_order_seq_cst);
}

void read_x_then_y() {
    while (!x.load(std::memory_order_seq_cst));
    if (y.load(std::memory_order_seq_cst)) {
        z.fetch_add(1, std::memory_order_seq_cst);
    }
}

void read_y_then_x() {
    while (!y.load(std::memory_order_seq_cst));
    if (x.load(std::memory_order_seq_cst)) {
        z.fetch_add(1, std::memory_order_seq_cst);
    }
}

int main() {
    std::thread t1(write_x);
    std::thread t2(write_y);
    std::thread t3(read_x_then_y);
    std::thread t4(read_y_then_x);

    t1.join();
    t2.join();
    t3.join();
    t4.join();

    // ISSUE SOLVED: Under relaxed/release-acquire ordering, it's possible for t3 to see x=true, y=false
    // AND t4 to see y=true, x=false simultaneously (z remaining 0).
    // Under seq_cst, a single global timeline guarantees z is NEVER 0!
    std::cout << "z value (Guaranteed > 0): " << z.load() << "
";
    assert(z.load() != 0);
    return 0;
}
{% endhighlight %}

---

### 6. `std::memory_order_consume`

#### Core Behavior
A specialized data-dependency variant of Acquire. It limits barrier synchronization exclusively to operations that have a **direct data dependency** on the loaded value (via pointers or calculations dependent on the atomic variable).

#### Status in Standard C++
> **Warning & Best Practice:** The C++ standard committee has formally discouraged the use of `std::memory_order_consume` because standard compilers find dependency tracking difficult to optimize, internally promoting `consume` operations to full `acquire` operations. Use `std::memory_order_acquire` instead.

{% highlight cpp %}
#include <iostream>
#include <atomic>
#include <thread>
#include <chrono>

struct ConfigData {
    int param1;
    int param2;
};

std::atomic<ConfigData*> global_config{nullptr};

void producer() {
    ConfigData* cfg = new ConfigData{100, 200};
    global_config.store(cfg, std::memory_order_release);
}

void consumer() {
    ConfigData* ptr = nullptr;
    // Consume targets only values carrying a direct data dependency via 'ptr'
    while (!(ptr = global_config.load(std::memory_order_consume))) {
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }

    // ISSUE SOLVED: Ensures 'ptr->param1' read is ordered relative to pointer creation
    // without enforcing a hardware-wide load barrier for unrelated variables.
    std::cout << "Param 1: " << ptr->param1 << "
";
    delete ptr;
}

int main() {
    std::thread t1(producer);
    std::thread t2(consumer);

    t1.join();
    t2.join();
    return 0;
}
{% endhighlight %}

---

## Summary of `std::memory_order` Choices

<details>
<summary>Click to view memory ordering model reference matrix</summary>

| Memory Order Enum | Barrier Type | Overhead / Cost | Key Use Case | Solved Issue |
| :--- | :--- | :--- | :--- | :--- |
| **`memory_order_relaxed`** | None | Minimal / Zero barrier overhead | Atomic counters, statistics | Prevents data races on isolated variables without restricting instruction order. |
| **`memory_order_release`** | Store Barrier | Low to Moderate | Data publishing / Producers | Prevents prior writes from being reordered after flag publishing. |
| **`memory_order_acquire`** | Load Barrier | Low to Moderate | Flag checking / Consumers | Prevents speculative reads of payload data before flag validation. |
| **`memory_order_acq_rel`** | Combined Barrier | Moderate | RMW operations (`fetch_add`, `CAS`) | Enables dual-ended synchronization in lock-free counters/queues. |
| **`memory_order_seq_cst`** | Full Global Barrier | Highest (System-wide cache sync) | Default atomic safety, complex multi-flag states | Prevents globally inconsistent execution timelines across CPU cores. |
| **`memory_order_consume`** | Data Dependent Load | Low (Promoted to Acquire in compilers) | Read-mostly data structures (e.g., RCU) | Constrains reordering strictly to dependent pointer branches. |

</details>