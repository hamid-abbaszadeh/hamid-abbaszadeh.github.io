---
layout: default
title: "<span style='color: #4ade80;'>Synchronization and Ordering Constraints</span>"
parent: C++ Memory Model
grand_parent: Multithreading
nav_order: 6
---

# Synchronization and Ordering Constraints

A comprehensive deep-dive into the theoretical backbone of the C++ memory model, memory ordering flags, and hardware-software execution guarantees.

---

## Table of Contents

1. TOC
{:toc}

---

## Overview & Core Foundations

When writing concurrent code with atomics in modern C++, standard atomic operations handle two separate and distinct responsibilities:

<div class="code-example" markdown="1">
1. **Atomicity (Data Race Prevention)**: Ensures that a memory location is read or written cleanly without intermediate states being observed by competing threads.
2. **Synchronization & Ordering Constraints**: Defines when changes to adjacent memory (both atomic and non-atomic variables) become visible across thread boundaries, constraining compiler and hardware instruction reordering.
</div>

<span class="label label-blue">Modern C++</span>
<span class="label label-green">Concurrency</span>
<span class="label label-purple">Memory Model</span>

---

## The Three Memory Ordering Categories

C++ categorizes its six memory ordering flags (`std::memory_order`) into three distinct models based on their synchronization strength:

```
[ Strongest / Easiest ]                                        [ Weakest / Complex ]
Sequential Consistency  ----->  Acquire-Release Semantics  ----->  Relaxed Semantics
```

| Memory Model | Permitted Flags | Primary Characteristics | Hardware Overhead |
| :--- | :--- | :--- | :--- |
| **Sequential Consistency** | `memory_order_seq_cst` | Global single total order; strict two-way barrier | High (Full Memory Fences) |
| **Acquire-Release** | `acquire`, `release`, `acq_rel`, `consume` | Pairwise thread synchronization; one-way barriers | Medium (Targeted Fences / Load-Store Rules) |
| **Relaxed** | `memory_order_relaxed` | Atomicity only; zero cross-thread ordering guarantees | Minimal (Native Atomic Ops) |

---

### 1. Sequential Consistency (`memory_order_seq_cst`)

Sequential consistency is the **implicit default** for all standard C++ atomic reads, writes, and read-modify-writes.

- **Global Order**: Imposes a single, globally agreed-upon total order of all `seq_cst` operations across all executing threads.
- **Ordering Guarantee**: No memory read or write instruction can be reordered across a `seq_cst` operation in either direction (acts as a full two-way memory barrier).
- **Trade-off**: Provides maximum correctness and ease of reasoning, but introduces significant hardware overhead on weakly ordered architectures (e.g., ARM, POWER) due to required CPU cache/bus synchronization instructions.

{% highlight cpp %}
#include <atomic>
#include <thread>
#include <cassert>

std::atomic<bool> x{false};
std::atomic<bool> y{false};
std::atomic<int> z{0};

void write_x() {
    x.store(true, std::memory_order_seq_cst);
}

void write_y() {
    y.store(true, std::memory_order_seq_cst);
}

void read_x_then_y() {
    while (!x.load(std::memory_order_seq_cst));
    if (y.load(std::memory_order_seq_cst)) {
        ++z;
    }
}

void read_y_then_x() {
    while (!y.load(std::memory_order_seq_cst));
    if (x.load(std::memory_order_seq_cst)) {
        ++z;
    }
}

int main() {
    std::thread a(write_x);
    std::thread b(write_y);
    std::thread c(read_x_then_y);
    std::thread d(read_y_then_x);

    a.join(); b.join(); c.join(); d.join();

    // z can NEVER be 0 due to total sequential consistency ordering
    assert(z.load() != 0);
}
{% endhighlight %}

<details>
<summary>Deep-Dive: Hardware Implications of Sequential Consistency</summary>
<p>
On strongly ordered architectures like x86/x64, standard loads and stores already exhibit acquire-release semantics for free. However, <code>memory_order_seq_cst</code> stores still require a full bus lock instruction (e.g., <code>LOCK XCHG</code> or <code>MFENCE</code>) to prevent store-load reordering across cores. On weakly ordered architectures like ARMv8, <code>seq_cst</code> operations emit sequential consistency instructions (such as <code>LDAR</code> and <code>STLR</code>) which stall pipeline execution until store buffers flush.
</p>
</details>

---

### 2. Acquire-Release Semantics

Acquire-Release establishes pairwise synchronization between threads without imposing a single global execution order across unrelated threads.

- **Read / Load**: Uses `std::memory_order_acquire` (or `memory_order_consume`).
- **Write / Store**: Uses `std::memory_order_release`.
- **Read-Modify-Write**: Uses `std::memory_order_acq_rel`.

#### One-Way Barrier Guarantees

- **Acquire Barrier**: No memory read or write operations following an Acquire load in program order can be reordered *before* it.
- **Release Barrier**: No memory read or write operations preceding a Release store in program order can be reordered *after* it.

{% highlight cpp %}
#include <atomic>
#include <thread>
#include <string>
#include <cassert>

std::atomic<bool> ready{false};
std::string data; // Non-atomic payload

void producer() {
    data = "Payload initialized";                          // 1. Non-atomic store
    ready.store(true, std::memory_order_release);        // 2. Release store (Barrier)
}

void consumer() {
    while (!ready.load(std::memory_order_acquire));      // 3. Acquire load (Barrier)
    assert(data == "Payload initialized");               // 4. Guaranteed to observe store #1
}
{% endhighlight %}

---

### 3. Relaxed Semantics (`memory_order_relaxed`)

Relaxed operations guarantee **atomicity only**. They prevent data races on the target variable itself but impose no synchronization or ordering constraints relative to surrounding memory access instructions.

- **Compiler & CPU Freedom**: High-level compilers and hardware cores are allowed to reorder surrounding non-atomic and atomic reads and writes freely around the relaxed operation.
- **Typical Use Cases**: Atomic counters (e.g., reference counting increment), statistics collection, or flags where thread coordination is handled elsewhere.

{% highlight cpp %}
#include <atomic>
#include <thread>

std::atomic<int> counter{0};

void increment_stats() {
    // Atomically increments counter without forcing cache flushes or memory fences
    counter.fetch_add(1, std::memory_order_relaxed);
}
{% endhighlight %}

---

## Key Theoretical Relationships

Multithreaded formal verification in C++ relies on three core theoretical relations:

### 1. Sequenced-Before (Intra-Thread)
An asymmetric, transitive relation between evaluation statements within the single execution context of a single thread. If Statement $A$ is placed before Statement $B$ in source execution order, $A$ is **sequenced-before** $B$.

### 2. Synchronizes-With (Inter-Thread)
An inter-thread relationship established when an atomic release operation in Thread $A$ writes a value that is subsequently read by an atomic acquire operation in Thread $B$ on the same atomic variable.

### 3. Happens-Before (Program-Wide Execution Order)
The foundational relation determining overall memory visibility and operational precedence across threads:

$$	ext{If } A 	ext{ is sequenced-before } B, 	ext{ then } A 	ext{ happens-before } B.$$

$$	ext{If } A 	ext{ synchronizes-with } B, 	ext{ then } A 	ext{ happens-before } B.$$

$$	ext{If } A 	ext{ happens-before } B 	ext{ and } B 	ext{ happens-before } C, 	ext{ then } A 	ext{ happens-before } C.$$

<div class="code-example" markdown="1">
> **Visibility Rule:** If Operation $A$ *happens-before* Operation $B$, then all memory side-effects made by $A$ are guaranteed to be fully visible to $B$.
</div>

---

## Operations Mapping Matrix

The following matrix defines the allowable memory ordering parameters across fundamental atomic operations and their canonical usage scenarios:

| Operations Type | Permitted Memory Orders | Typical Use Case |
| :--- | :--- | :--- |
| **Read (Load)** | `relaxed`, `consume`, `acquire`, `seq_cst` | Reading status flags, acquiring locks, reading shared state |
| **Write (Store)** | `relaxed`, `release`, `seq_cst` | Setting completion flags, releasing locks, publishing data |
| **Read-Modify-Write** | `relaxed`, `consume`, `acquire`, `release`, `acq_rel`, `seq_cst` | Fetch-and-add counters, CAS (Compare-And-Swap) loops |

---

## Practical Example: Lock-Free Stack Spinlock Pattern

<details>
<summary>View Complete Lock-Free Reference Implementation</summary>

{% highlight cpp %}
#include <atomic>
#include <thread>

class Spinlock {
private:
    std::atomic<bool> flag{false};

public:
    void lock() {
        // Acquire barrier ensures subsequent critical section reads/writes don't hoist above
        while (flag.exchange(true, std::memory_order_acquire)) {
            #if defined(__x86_64__) || defined(_M_X64)
            __builtin_ia32_pause();
            #endif
        }
    }

    void unlock() {
        // Release barrier ensures prior critical section reads/writes finish before releasing flag
        flag.store(false, std::memory_order_release);
    }
};
{% endhighlight %}

</details>