---
layout: default
title: Sequential Consistency – Practice
parent: C++ Memory Model
grand_parent: Multithreading
nav_order: 10
---



# Sequential Consistency in C++ Memory Model

Understanding `std::memory_order_seq_cst` through a practical lock-free Producer-Consumer pattern and formal synchronization analysis.

---

## Table of Contents

1. TOC
{:toc}

---

## Overview

<span class="label label-blue">Modern C++</span> <span class="label label-green">Concurrency</span> <span class="label label-yellow">Lock-Free</span>

In C++ multithreading, sequential consistency (`std::memory_order_seq_cst`) is the default memory ordering for atomic operations. It provides an intuitive mental model: operations appear to execute in a strict single-thread-like sequential order, shared consistently across all threads.

### Trade-offs: Intuition vs. Hardware Cost

* **Advantage:** Sequential consistency matches our intuitive understanding of program execution. Every thread observes operations in source-code order, as if all threads execute on a single global clock.
* **Disadvantage:** Achieving this global order requires the CPU and compiler to introduce heavyweight synchronization memory barriers, which inhibits certain reordering optimizations and incurs performance overhead.

---

## Practical Example: Lock-Free Producer-Consumer

Below is a classic Producer-Consumer implementation using atomic flags for signaling instead of `std::mutex` or `std::condition_variable`.

{% highlight cpp %}
#include <atomic>
#include <iostream>
#include <string>
#include <thread>

std::string work;
std::atomic<bool> ready{false};

void consumer() {
    // Consumer polls ready flag
    while (!ready.load()) {} 
    
    // Guaranteed to see "done" because of sequential consistency
    std::cout << work << std::endl; 
}

void producer() {
    work = "done";       // Non-atomic assignment
    ready.store(true);   // Atomic store (seq_cst by default)
}

int main() {
    std::thread t1(consumer);
    std::thread t2(producer);
    
    t1.join();
    t2.join();
}
{% endhighlight %}

<details>
<summary>Execution Output & Explanation</summary>
<p>
<strong>Output:</strong>
</p>
<pre>done</pre>
<p>
Even though <code>work</code> is a non-atomic variable, the program is completely free of data races. The atomic operations on <code>ready</code> establish a strict boundary ensuring <code>work</code> is fully written before it is read.
</p>
</details>

---

## Formal Proof of Correctness

To prove why this pattern is deterministic and free of data races, we analyze the execution order using formal relations within the C++ Memory Model.

### 1. Intra-Thread Sequencing (Sequenced-Before)

Within a single thread, evaluation steps follow program order:

* In `producer()`: `work = "done"` is sequenced-before `ready.store(true)`.
* In `consumer()`: `while (!ready.load())` is sequenced-before `std::cout << work`.

$$\text{work = "done"} \xrightarrow{\text{happens-before}} \text{ready.store(true)}$$

$$\text{while (!ready.load())} \xrightarrow{\text{happens-before}} \text{std::cout << work}$$

### 2. Inter-Thread Synchronization (Synchronizes-With)

Under sequential consistency, an atomic store synchronizes with an atomic load that reads the written value across threads:

$$\text{ready.store(true)} \xrightarrow{\text{synchronizes-with}} \text{while (!ready.load())}$$

This inter-thread synchronization establishes a global *happens-before* relation between the threads.

### 3. Transitive Execution Chain

Combining intra-thread sequencing and inter-thread synchronization yields the total ordering chain across threads:

$$\text{work = "done"} \xrightarrow{\text{happens-before}} \text{ready.store(true)} \xrightarrow{\text{happens-before}} \text{while (!ready.load())} \xrightarrow{\text{happens-before}} \text{std::cout << work}$$

Because <span class="math">work = "done"</span> strictly **happens-before** <span class="math">std::cout << work</span>, the consumer thread is mathematically guaranteed to observe `"done"`.

---

## Transitioning to Acquire-Release Semantics

While `std::memory_order_seq_cst` provides strong guarantees, it forces all atomic operations globally into a single total order. 

In performance-critical code, this same Producer-Consumer guarantee can be achieved with lower overhead using **Acquire-Release Semantics**:

* `ready.store(true, std::memory_order_release);` in the producer.
* `ready.load(std::memory_order_acquire);` in the consumer.

Acquire-Release synchronizes only dependent operations between specific threads without enforcing a global clock across all threads, reducing CPU pipeline stalls.