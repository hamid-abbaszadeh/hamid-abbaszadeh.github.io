---
layout: default
title: "The Atomic Boolean"
parent: C++ Memory Model
grand_parent: Multithreading
nav_order: 4
---



# The Atomic Boolean: `std::atomic<bool>` Interface, Trade-offs, and Signaling

An architectural exploration of `std::atomic<bool>`, detailing how it expands upon low-level primitives, its API capabilities, practical signaling patterns, and key lock-free guarantees.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++11</span>
<span class="label label-purple">Lock-Free</span>
<span class="label label-yellow">Thread Safety</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Introduction

The atomic boolean (`std::atomic<bool>`) directly builds upon `std::atomic_flag` by expanding the capabilities of boolean atomics while introducing minor trade-offs regarding lock-free hardware guarantees.

While `std::atomic_flag` provides the bare-minimum, hardware-guaranteed lock-free primitive, `std::atomic<bool>` offers a much richer interface designed to act like a standard boolean variable in thread-safe contexts.

---

## Enhanced Interface (Load, Store, and Exchange)

Unlike `std::atomic_flag`, which only permits `test_and_set()` and `clear()`, `std::atomic<bool>` supports explicit read and write operations:

* **`.store(val)`:** Atomically sets the boolean to `true` or `false`.
* **`.load()`:** Atomically reads the current boolean state.
* **`.exchange(val)`:** Atomically replaces the current value with `val` and returns the old value (similar to `test_and_set()`, but allows setting to `false`).
* **`.compare_exchange_weak()` / `.compare_exchange_strong()`:** Enables Compare-and-Swap (CAS) logic on boolean values.

{% highlight cpp %}
#include <atomic>

std::atomic<bool> flag{false};

void update_state() {
    // Direct atomic store and load with explicit memory orders
    flag.store(true, std::memory_order_release);
    bool current_state = flag.load(std::memory_order_acquire);
}
{% endhighlight %}

---

## Key Distinctions: `std::atomic_flag` vs. `std::atomic<bool>`

Selecting between `std::atomic_flag` and `std::atomic<bool>` requires evaluating API requirements against hardware execution guarantees.

| Characteristic | `std::atomic_flag` | `std::atomic<bool>` |
| :--- | :--- | :--- |
| **Lock-Free Guarantee** | Always lock-free on all platforms (guaranteed by standard). | Usually lock-free, but must check `.is_lock_free()` or `is_always_lock_free`. |
| **Explicit Read/Write** | No (`load()` and `store()` prohibited). | Yes (`load()`, `store()`, `exchange()`). |
| **Setting to false** | Only via `.clear()`. | Directly via `.store(false)` or `.exchange(false)`. |
| **Initialization** | Must use `ATOMIC_FLAG_INIT` (pre-C++20). | Standard constructor syntax (`std::atomic<bool> b{false}`). |

---

## Practical Use Case: Condition Signaling & Thread Notifications

Because `std::atomic<bool>` supports explicit `load()` and `store()`, it is ideal for one-way notification flags (such as signaling a background worker thread to stop), where active polling via `test_and_set()` would be clunky.

{% highlight cpp %}
#include <atomic>
#include <thread>
#include <chrono>

std::atomic<bool> ready{false};

void work() {
    // Wait until the main thread sets ready to true
    while (!ready.load(std::memory_order_acquire)) {
        std::this_thread::yield(); // Yield CPU execution slot
    }
    // Do work once ready is true...
}

int main() {
    std::thread t(work);
    
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    ready.store(true, std::memory_order_release); // Publish ready state
    
    t.join();
    return 0;
}
{% endhighlight %}

<details>
<summary><b>Deep Dive: std::this_thread::yield() in Polling Loops</b></summary>
<p>
When waiting on a boolean signal like <code>std::atomic<bool></code>, busy-waiting in a tight <code>while</code> loop can saturate a CPU core. Invoking <code>std::this_thread::yield()</code> hints to the operating system scheduler that the current thread can relinquish its CPU time slice, allowing other threads to run and preventing temporary CPU starvation.
</p>
</details>

---

## Why Isn't `std::atomic<bool>` Guaranteed Always Lock-Free?

On modern x86 and ARM architectures, `std::atomic<bool>` is implemented using single-byte atomic hardware instructions and is lock-free.

However, the C++ standard does not mandate it to be lock-free across all esoteric hardware (such as legacy or specialized embedded architectures that cannot execute byte-addressable atomic loads/stores without locking a larger word boundary). For these platforms, `std::atomic<bool>` may silently fall back to an internal mutex.

---

## Conclusion

`std::atomic<bool>` balances high-level ergonomic syntax with high-performance lock-free execution. When building cross-platform real-time or embedded software, verify hardware capabilities using `.is_lock_free()` or default to `std::atomic_flag` if absolute lock-free guarantees are required.