---
layout: default
title: Synchronization and Ordering Constraints
parent: C++ Memory Model
grand_parent: Multithreading
nav_order: 12
---


# Acquire-Release Semantics in C++

Optimizing lock-free thread synchronization through targeted, one-way memory barriers without the overhead of global sequential consistency.

---

## Table of Contents

1. TOC
{:toc}

---

## Overview

<span class="label label-blue">Modern C++</span> <span class="label label-green">Concurrency</span> <span class="label label-purple">Performance</span>

Acquire-Release semantics introduce a key optimization over sequential consistency (`std::memory_order_seq_cst`). While sequential consistency forces a single global timeline across all execution cores, Acquire-Release semantics synchronize memory pairwise exclusively between specific threads operating on the same atomic variable.

---

## Core Concept: Pairwise Synchronization

Synchronization occurs exclusively between a **Release Store** in a writing thread and an **Acquire Load** in a reading thread.

### One-Way Memory Barriers

Acquire-Release semantics act as directional barriers for memory instructions, constraining compiler and CPU reordering without requiring global bus locks:

* **Release Operation (`std::memory_order_release`):** Applied to write/store operations. No memory reads or writes written before the release store in code can be reordered after it. It "publishes" all prior memory modifications.
* **Acquire Operation (`std::memory_order_acquire`):** Applied to read/load operations. No memory reads or writes written after the acquire load in code can be reordered before it. It "consumes" memory changes published by the release store.
* **Acquire-Release Operation (`std::memory_order_acq_rel`):** Applied to Read-Modify-Write (RMW) operations (such as `fetch_add` or CAS). It acts simultaneously as both an acquire barrier and a release barrier.

---

## Producer-Consumer Example

Rewriting the classic Producer-Consumer pattern using Acquire-Release replaces heavy sequential consistency barriers with targeted pairwise synchronization:

{% highlight cpp %}
#include <atomic>
#include <iostream>
#include <string>
#include <thread>

std::string work;
std::atomic<bool> ready{false};

void producer() {
    work = "done"; // Non-atomic payload write
    
    // Release store: guarantees work = "done" cannot drift down past this line
    ready.store(true, std::memory_order_release); 
}

void consumer() {
    // Acquire load: guarantees reading work cannot drift up before this line
    while (!ready.load(std::memory_order_acquire)) {} 
    
    // Safe to access non-atomic payload!
    std::cout << work << std::endl; 
}

int main() {
    std::thread t1(producer);
    std::thread t2(consumer);
    t1.join();
    t2.join();
}
{% endhighlight %}

<details>
<summary>Execution Mechanics & Memory Boundary</summary>
<p>
The release store on <code>ready</code> forces the payload store <code>work = "done"</code> to commit before <code>ready</code> becomes <code>true</code>. The acquire load ensures the non-atomic read of <code>work</code> cannot execute until <code>ready.load()</code> returns <code>true</code>. This guarantees a safe transfer of non-atomic state without data races.
</p>
</details>

---

## Key Takeaways & Comparison

| Property | Sequential Consistency (`seq_cst`) | Acquire-Release (`acquire` / `release`) |
| :--- | :--- | :--- |
| **Global Order** | **Yes** — all threads see an identical operation order across all variables. | **No** — memory ordering is synchronized strictly pairwise between matching threads on a single atomic variable. |
| **Barrier Type** | Two-way full memory fence (prevents reordering in both directions across the barrier). | One-way directional barrier (Release blocks downward movement; Acquire blocks upward movement). |
| **Hardware Cost** | **Higher** (forces CPU cache/bus flush instructions such as `MFENCE` on x86). | **Lower** (maps to lighter hardware instructions like `LDA` / `STL` on ARM64). |