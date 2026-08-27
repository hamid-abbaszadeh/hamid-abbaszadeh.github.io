---
layout: default
title: Transitivity
parent: C++ Memory Model
grand_parent: Multithreading
nav_order: 13
---

# Transitivity in Acquire-Release Semantics

Building multi-threaded relay chains of data visibility across threads without expensive global synchronization barriers.

---

## Table of Contents

1. TOC
{:toc}

---

## Overview

<span class="label label-blue">Modern C++</span> <span class="label label-green">Concurrency</span> <span class="label label-purple">Performance</span>

The core idea of transitivity in acquire-release semantics is straightforward: you can create a data "relay race" across multiple execution threads[cite: 3]. If Thread 1 passes the baton to Thread 2, and Thread 2 passes the baton to Thread 3, Thread 3 is guaranteed to see everything Thread 1 produced—even though Thread 1 and Thread 3 never communicated directly[cite: 3].

---

## The Real-World Analogy

Imagine three factory workers operating on an assembly line[cite: 3]:

* **Worker 1 (Producer):** Writes a secret message on a piece of paper, puts it inside Box A, and flips a physical switch (**Flag 1**) to "READY"[cite: 3].
* **Worker 2 (Relay):** Waits for **Flag 1** to show "READY"[cite: 3]. Once triggered, Worker 2 flips a second switch (**Flag 2**) to "READY"[cite: 3].
* **Worker 3 (Consumer):** Waits for **Flag 2** to show "READY"[cite: 3]. Once triggered, Worker 3 opens Box A and reads the secret message[cite: 3].

Worker 3 reads the message safely because the signal propagated down the assembly line step-by-step, preserving payload visibility across every node[cite: 3].

---

## Lock-Free Implementation

The code below demonstrates how to construct this transitive synchronization chain using atomic flags[cite: 3]:

{% highlight cpp %}
#include <atomic>
#include <thread>
#include <iostream>

int secretData = 0;              // Plain non-atomic data payload
std::atomic<int> flag1{0};       // First synchronization switch
std::atomic<int> flag2{0};       // Second synchronization switch

void thread1() {
    secretData = 42;                             // 1. Prepare data
    flag1.store(1, std::memory_order_release);   // 2. Pass baton to Thread 2
}

void thread2() {
    while (flag1.load(std::memory_order_acquire) != 1); // 3. Catch baton from Thread 1
    flag2.store(1, std::memory_order_release);          // 4. Pass baton to Thread 3
}

void thread3() {
    while (flag2.load(std::memory_order_acquire) != 1); // 5. Catch baton from Thread 2
    
    // GUARANTEED SAFE: secretData will always be 42!
    std::cout << secretData << std::endl;               
}

int main() {
    std::thread t1(thread1);
    std::thread t2(thread2);
    std::thread t3(thread3);

    t1.join();
    t2.join();
    t3.join();
}
{% endhighlight %}

<details>
<summary>Execution Mechanics & Output</summary>
<p>
<strong>Console Output:</strong>
</p>
<pre>42</pre>
<p>
Even though <code>secretData</code> is a plain non-atomic integer, the transitive synchronization chain prevents data races completely[cite: 3]. Thread 3 never reads <code>secretData</code> before Thread 1 finishes writing it[cite: 3].
</p>
</details>

---

## Why It Works: The Golden Rules

To ensure the relay works reliably without data races, two memory-ordering rules govern the operations[cite: 3]:

### Release = "Publish & Freeze"
When a thread writes using `std::memory_order_release`, it instructs the compiler and CPU: *"Finish writing all preceding memory modifications BEFORE setting this atomic flag."*[cite: 3]

### Acquire = "Wait & Synchronize"
When a thread reads using `std::memory_order_acquire`, it instructs the compiler and CPU: *"Do not execute any subsequent memory reads UNTIL this atomic flag reads the expected value."*[cite: 3]

Because Thread 2 receives `flag1` with an **acquire** load and publishes `flag2` with a **release** store, it links both operations into a continuous, unbroken chain[cite: 3]:

$$\text{Thread 1 prepares data} \longrightarrow \text{Thread 2 gets notified} \longrightarrow \text{Thread 3 gets notified and reads data safely}$$

---

## Performance Trap: Broken Handoffs

<span class="label label-yellow">Performance Pitfall</span> <span class="label label-red">Data Race Risk</span>

The transitive relay chain functions only when **every single handoff** uses Acquire-Release ordering[cite: 3]. 

If Thread 2 evaluates either step using `std::memory_order_relaxed`, the synchronization link snaps[cite: 3]! The CPU or compiler remains free to reorder instructions across the boundary, leading to potential data races where Thread 3 accesses `secretData` prior to Thread 1 completing the write operation[cite: 3].