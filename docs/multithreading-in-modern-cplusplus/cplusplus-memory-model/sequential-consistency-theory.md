---
layout: default
title: Sequential Consistency – Theory
parent: C++ Memory Model
grand_parent: Multithreading
nav_order: 9
---


# Sequential Consistency in the C++ Memory Model

A comprehensive technical breakdown of Sequential Consistency (`std::memory_order_seq_cst`) based on Rainer Grimm's insights into the foundational mechanics of C++ multithreading.

---

## Table of Contents

1. TOC
{:toc}

---

## Overview & Core Foundations

In C++11, the C++ language formally introduced a standardized memory model. At the foundation of this memory model sit **atomic operations**, which prevent data races when multiple threads access shared memory. 

By default, all atomic operations in C++ utilize **Sequential Consistency** (`std::memory_order_seq_cst`). First formally defined by Leslie Lamport in 1979, sequential consistency establishes the strongest correctness guarantees available in the C++ memory model.

<div class="code-example" markdown="1">
### The Sequential Consistency Guarantees
1. **Source Code Execution Order (Intra-Thread)**: Program statements executed by a single thread strictly follow program (source code) order. No instruction can cross an atomic boundary via compiler or CPU reordering.
2. **Global Total Order (Inter-Thread)**: All operations on all threads follow a single, globally agreed-upon time clock. Every thread observes the execution sequence of other threads in the exact order in which they executed.
</div>

<span class="label label-blue">Modern C++</span>
<span class="label label-green">Concurrency</span>
<span class="label label-purple">Memory Model</span>

---

## Formal Execution Rules

Sequential consistency relies on formal relationships established by the C++ specification to guarantee program-wide visibility:
```
+--------------------------+          +---------------------------+
| Sequenced-Before Rule    |  ----->  | Synchronizes-With Rule    |
| (Intra-Thread Precedence)|          | (Inter-Thread Handshake)  |
+--------------------------+          +---------------------------+
|
v
+---------------------------+
| Happens-Before Relation   |
| (Guaranteed Visibility)   |
+---------------------------+
```

| Relationship | Execution Scope | Description |
| :--- | :--- | :--- |
| **Sequenced-Before** | Single-Thread | Statement $A$ comes before Statement $B$ in local execution order. |
| **Synchronizes-With** | Multi-Thread | An atomic write in Thread 1 is observed by an atomic read in Thread 2 on the same variable. |
| **Happens-Before** | Program-Wide | Combines *sequenced-before* and *synchronizes-with* to establish total memory visibility order. |

---

## Technical Case Study: Producer-Consumer Pattern

The following example demonstrates deterministic synchronization between a producer thread and a consumer thread using `std::memory_order_seq_cst`.

{% highlight cpp %}
#include <atomic>
#include <iostream>
#include <string>
#include <thread>

std::string work;
std::atomic<bool> ready{false};

void producer() {
    // 1. Non-atomic modification
    work = "done"; 
    
    // 2. Atomic store (std::memory_order_seq_cst by default)
    ready.store(true); 
}

void consumer() {
    // 3. Atomic load polling (std::memory_order_seq_cst by default)
    while (!ready.load()) {
        std::this_thread::yield();
    }
    
    // 4. Guaranteed to observe work = "done" without a data race
    std::cout << work << std::endl; 
}

int main() {
    std::thread t1(producer);
    std::thread t2(consumer);
    
    t1.join();
    t2.join();
    
    return 0;
}
{% endhighlight %}

### Execution Order Breakdown

1. `work = "done"` is **sequenced-before** `ready.store(true)`.
2. `ready.store(true)` **synchronizes-with** `ready.load()` in the consumer `while`-loop.
3. The consumer `while`-loop is **sequenced-before** `std::cout << work`.
4. Transitively, `work = "done"` **happens-before** `std::cout << work`, ensuring zero data races on the non-atomic string `work`.

<details>
<summary>Deep-Dive: Hardware & Compiler Overhead</summary>
<p>
While sequential consistency offers intuitive reasoning, its key trade-off is <strong>performance and hardware overhead</strong>. 
<br><br>
To maintain a single global total order across core boundaries:
<ul>
  <li><strong>x86 / x64:</strong> Standard loads and stores already enforce strict ordering, but sequential stores require expensive <code>LOCK XCHG</code> or <code>MFENCE</code> instructions to prevent store-load reordering.</li>
  <li><strong>ARMv8 / Weak Architectures:</strong> Emits pipeline-blocking instructions (such as <code>LDAR</code> and <code>STLR</code>) which force CPU store buffers to flush completely before proceeding.</li>
</ul>
Modern optimization strategies often relax this model to <em>Acquire-Release</em> or <em>Relaxed</em> semantics when peak throughput is required and global ordering is unnecessary.
</p>
</details>

---

## Comparison of C++ Memory Models

Sequential consistency sits at the top of a spectrum of C++ synchronization strength:

```
[ Strongest / Easiest ]                                        [ Weakest / Complex ]
Sequential Consistency  ----->  Acquire-Release Semantics  ----->  Relaxed Semantics
```

| Feature | Sequential Consistency (`seq_cst`) | Acquire-Release (`acquire`/`release`) | Relaxed (`relaxed`) |
| :--- | :--- | :--- | :--- |
| **Global Order** | Yes (Single program clock) | No (Pairwise threads only) | No global order |
| **Reordering Barriers** | Full two-way barrier | One-way barrier | No ordering barriers |
| **Data Race Prevention** | Yes | Yes | Yes (On the target variable only) |
| **Intuitive Reasoning** | High | Medium | Low (Requires formal verification) |