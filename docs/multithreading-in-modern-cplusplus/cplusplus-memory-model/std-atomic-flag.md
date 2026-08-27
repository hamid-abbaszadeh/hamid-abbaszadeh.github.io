---
layout: default
title: "std::atomic_flag"
parent: C++ Memory Model
grand_parent: Multithreading
nav_order: 3
---


# Understanding std::atomic_flag and C++ Memory Ordering Models

A foundational guide on `std::atomic_flag`, lock-free programming primitives, spinlock implementations, and memory ordering semantics in modern C++.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++11</span>
<span class="label label-yellow">Lock-Free</span>
<span class="label label-red">High Performance</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Core Concepts & Properties

### What is `std::atomic_flag`?

`std::atomic_flag` is an atomic boolean-like type featuring an extremely simple, minimalist interface[cite: 1]. 

* It must be initialized using the macro `ATOMIC_FLAG_INIT` (which sets it to `false`).
* It supports only two primary operations:
  * `test_and_set()`: Atomically sets the flag to `true` and returns its previous value.
  * `clear()`: Sets the flag back to `false`.

### The Only Guaranteed Lock-Free Atomic

Unlike other atomic types (`std::atomic<T>`), which may fall back to using internal hidden mutexes on certain hardware architectures (queryable via `.is_lock_free()`), `std::atomic_flag` is guaranteed to be lock-free on all platforms. 

Because of this property, it serves as the foundational building block for higher-level synchronization abstractions in C++.

---

## Practical Application: Implementing a Spinlock

`std::atomic_flag` can be used to implement a spinlock—a synchronization mechanism similar to a mutex, but with a different waiting strategy.

{% highlight cpp %}
#include <atomic>
#include <thread>

class Spinlock {
    std::atomic_flag flag;
public:
    Spinlock() : flag(ATOMIC_FLAG_INIT) {}
    
    void lock() {
        // Active waiting (busy-looping) until test_and_set returns false
        while (flag.test_and_set());
    }
    
    void unlock() {
        flag.clear();
    }
};
{% endhighlight %}

<details>
<summary><b>How it works</b></summary>
<p>
1. When a thread calls <code>lock()</code>, it invokes <code>test_and_set()</code>.<br>
2. If the flag was <code>false</code>, the thread successfully captures the lock (setting it to <code>true</code>) and the loop terminates.<br>
3. If the flag was already <code>true</code>, <code>test_and_set()</code> returns <code>true</code>, and the thread gets caught in the <code>while</code> loop, eagerly checking again.
</p>
</details>

---

## Spinlock vs. Mutex (Active vs. Passive Waiting)

Spinlocks and traditional mutexes treat CPU execution differently during contention:

### Spinlocks (Active Waiting)
* Threads waiting for a lock continuously poll the CPU (busy-waiting).
* They avoid the expensive OS context-switching overhead associated with putting a thread to sleep and waking it up.
* **Downside:** They fully utilize the CPU core (driving usage to 100% on that core) while waiting, making them ideal only for very short critical sections where locks are held for minimal durations.

### Mutexes (Passive Waiting)
* Operating system mutexes put waiting threads to sleep, yielding the CPU core so other processes can use it without spiking CPU utilization.

---

## Memory Ordering Models

By default, all atomic operations in C++ enforce sequential consistency (`std::memory_order_seq_cst`). This is the safest and most intuitive memory order: it guarantees that all threads see a single, globally agreed-upon chronological order of operations.

However, enforcing sequential consistency requires hardware-level memory barriers and synchronization instructions that can slow down performance. To optimize high-performance multithreaded code, C++ provides weaker memory orders.

The six memory order tags in C++ map to three distinct synchronization models:
1. Sequential Consistency (`std::memory_order_seq_cst`)
2. Acquire-Release Semantics (`std::memory_order_acquire`, `std::memory_order_release`, `std::memory_order_acq_rel`)
3. Relaxed Ordering (`std::memory_order_relaxed`)

---

### 1. Relaxed Ordering (`std::memory_order_relaxed`)

Relaxed operations provide no synchronization or ordering constraints relative to other memory accesses. They guarantee only that the modification of the atomic variable itself is atomic.

* **What it allows:** The compiler and CPU are free to reorder read and write instructions around the atomic operation however they see fit, as long as the modification to that single variable appears atomic to other threads.
* **Use case:** Counters or statistics where you only care that the final value is accurate, but the exact interleaving order relative to other variables doesn't matter.

{% highlight cpp %}
// Thread 1 increments a counter with no ordering guarantees
counter.fetch_add(1, std::memory_order_relaxed);
{% endhighlight %}

---

### 2. Acquire-Release Semantics (`acquire` and `release`)

This model creates a synchronization relationship between two different threads operating on the same atomic variable. It is commonly used for mutexes, locks, and producer-consumer flags.

* **Release (`std::memory_order_release`):** Applied to a store (write) operation. It guarantees that no memory reads or writes that happen before the release store can be reordered after it. Any memory changes made by this thread are "published" to other threads.
* **Acquire (`std::memory_order_acquire`):** Applied to a load (read) operation. It guarantees that no memory reads or writes that happen after the acquire load can be reordered before it. It "synchronizes-with" a corresponding release store, ensuring that all memory changes made prior to the release become visible to this thread.

#### Example: Signaling Work Completion

{% highlight cpp %}
#include <atomic>
#include <thread>
#include <cassert>

std::atomic<bool> ready{false};
int shared_data = 0;

// Producer Thread
void producer() {
    shared_data = 42; // Non-atomic write
    // Release ensures shared_data = 42 happens BEFORE ready becomes true
    ready.store(true, std::memory_order_release); 
}

// Consumer Thread
void consumer() {
    // Acquire ensures we wait until ready is true, and establishes a sync edge
    while (!ready.load(std::memory_order_acquire));
    
    // Guaranteed to see 42 because of acquire-release synchronization!
    assert(shared_data == 42); 
}
{% endhighlight %}

<details>
<summary><b>Why not use std::memory_order_relaxed here?</b></summary>
<p>
If you used <code>std::memory_order_relaxed</code> in the signaling pattern above, the CPU or compiler could theoretically reorder <code>shared_data = 42</code> after the <code>ready</code> store, causing the consumer to see <code>ready == true</code> while <code>shared_data</code> is still <code>0</code>.
</p>
</details>

---

### 3. Consume Ordering (`std::memory_order_consume`)

> **Note:** This is a specialized, highly optimized variant of acquire semantics designed to handle data dependencies (e.g., loading a pointer and immediately dereferencing it). In practice, it is rarely used because most compilers currently promote `memory_order_consume` to `memory_order_acquire` for safety.

---

## Summary Table of Memory Orders

| Memory Order Tag | Applies To | Synchronization Effect | Performance Cost |
| :--- | :--- | :--- | :--- |
| `memory_order_seq_cst` | Loads, Stores, RMW | Global total order; strict synchronization. | Highest (Default) |
| `memory_order_release` | Stores | Prevents prior memory accesses from moving down past it. | Moderate |
| `memory_order_acquire` | Loads | Prevents subsequent memory accesses from moving up before it. | Moderate |
| `memory_order_acq_rel` | Read-Modify-Write | Combines both acquire and release semantics. | Moderate |
| `memory_order_relaxed` | Loads, Stores, RMW | Atomicity only; zero ordering constraints. | Lowest |