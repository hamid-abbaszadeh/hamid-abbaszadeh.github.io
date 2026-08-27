---
layout: default
title: "The Special Case std::memory_order_consume"
parent: C++ Memory Model
grand_parent: Multithreading
nav_order: 14
---

# std::memory_order_consume Demystified

Understanding data dependency chains, targeted ordering efficiency, and compiler implementation realities.

---

## Table of Contents

1. TOC
{:toc}

---

## Overview

<span class="label label-blue">Modern C++</span> <span class="label label-green">Concurrency</span> <span class="label label-yellow">Performance Pitfalls</span>

The core idea behind `std::memory_order_consume` is targeted efficiency: instead of freezing all memory operations across an entire thread, it limits memory constraints strictly to operations carrying a direct data dependency on the loaded atomic variable. Think of it as a specialized, lighter alternative to `std::memory_order_acquire`.

---

## Real-World Analogy: Package & Assembly Instructions

Consider a delivery process involving two different receiver strategies:

* **The Shipper (Producer):** Assembles a furniture kit (the primary payload data), writes unrelated updates in a company newsletter (independent data), and sends a tracking number pointing to the furniture kit using `std::memory_order_release`.
* **The Receiver with `acquire` (Heavy Overhead):** Waits for the tracking number to arrive. Refuses to read anything—including the company newsletter or standard mail—until the furniture kit arrives safely. Every operation halts until delivery verification completes.
* **The Receiver with `consume` (Targeted Dependency):** Waits for the tracking number to arrive. Only delays assembling the furniture because assembly directly depends on receiving the tracking number. Reads the company newsletter or checks standard mail concurrently without waiting, as those operations bear no dependency on the furniture delivery.

---

## How It Works in C++ Code

The following example demonstrates loading a custom object through an atomic pointer:

{% highlight cpp %}
#include <atomic>
#include <string>
#include <iostream>

struct Furniture {
    std::string name;
};

std::atomic<Furniture*> ptr{nullptr};
int companyNews = 0;

void producer() {
    Furniture* f = new Furniture{"Desk"};
    companyNews = 100;
    
    // Release store: publishes 'f' and 'companyNews'
    ptr.store(f, std::memory_order_release);
}

void consumer() {
    Furniture* f;
    
    // Consume load: ONLY protects operations that depend directly on 'f'
    while (!(f = ptr.load(std::memory_order_consume)));
    
    // SAFE: f->name depends directly on the loaded pointer 'f'
    std::cout << f->name << std::endl; 
    
    // NOT GUARANTEED SAFE: companyNews does NOT depend on 'f'!
    // The CPU/compiler might read companyNews BEFORE ptr is loaded.
    std::cout << companyNews << std::endl; 
}
{% endhighlight %}

<details>
<summary>Execution Breakdown & Memory Ordering Analysis</summary>
<p>
Accessing <code>f->name</code> is thread-safe under consume ordering because dereferencing <code>f</code> creates an explicit data dependency on the atomic load operation. Conversely, accessing <code>companyNews</code> carries zero data dependency on <code>f</code>, introducing a potential data race if executed concurrently with the producer's non-atomic write.
</p>
</details>

---

## The Golden Rule: Data Dependency

`std::memory_order_consume` enforces ordering exclusively along a mathematical data dependency chain:

$$\text{Load Pointer } f \longrightarrow \text{Dereference } f \rightarrow \text{name} \quad (\text{Protected})$$

* **Protected Operations:** Operations that explicitly compute values using the loaded variable (e.g., `f->name` or `array[f->index]`) maintain guaranteed ordering.
* **Unprotected Operations:** Independent memory accesses (e.g., `companyNews`) receive zero ordering guarantees under consume semantics.

---

## Performance Pitfall: Practical Realities

<span class="label label-red">Compiler Warning</span> <span class="label label-purple">Architecture Impact</span>

While `std::memory_order_consume` sounds ideal for fine-grained performance tuning on weakly-ordered architectures (such as ARM or PowerPC), practical implementation obstacles limit its adoption:

### 1. Compiler Promotion to Acquire
Tracking data dependencies reliably through aggressive compiler optimization passes is extremely difficult. To eliminate subtle codegen bugs, major compilers (GCC, Clang, MSVC) automatically promote `std::memory_order_consume` to `std::memory_order_acquire` internally.

### 2. Architecture Neutrality on x86
On strongly-ordered x86/x64 processors, consume and acquire generate identical assembly operations (`MOV`), rendering the theoretical performance optimization moot at the hardware level.

### 3. Deprecation and Guidance
The ISO C++ Standards Committee discourages reliance on `std::memory_order_consume` pending a revised dependency-tracking specification. 

> **Recommendation:** Prefer `std::memory_order_acquire` for atomic read operations. It provides reliable synchronization guarantees, eliminates hidden data-race risks on independent payloads, and yields equivalent runtime performance across modern compiler toolchains.