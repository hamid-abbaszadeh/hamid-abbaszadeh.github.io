---
layout: default
title: "std::atomic (Specializations)"
parent: C++ Memory Model
grand_parent: Multithreading
nav_order: 5
---



# Advanced C++ Atomic Specializations: Integrals, Pointers, and User-Defined Types

An in-depth architectural guide covering the full spectrum of `std::atomic` template specializations beyond boolean and flag primitives—focusing on integral types, pointer arithmetic, custom types, and smart pointers.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++11</span>
<span class="label label-purple">C++20</span>
<span class="label label-yellow">Thread Safety</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Introduction

Modern C++ provides specialized templates for `std::atomic` beyond simple flags and boolean states. These specializations allow developers to execute atomic operations on integral types, manipulate memory addresses via pointer atomics, and safely wrap custom structures. Understanding these specializations—along with their interface nuances and hardware limitations—is essential for building safe, high-performance concurrent systems.

---

## 1. Integral Atomics (`std::atomic<Integral>`)

C++ provides atomic specializations for standard integer types (such as `int`, `char`, `long`, `uint64_t`, and `size_t`).

### Supported Composite Assignments
Integral atomics support composite arithmetic and bitwise assignment operators directly:
* **Arithmetic:** `+=`, `-=`
* **Bitwise:** `&=`, `|=`, `^=`

### Assignment Operators vs. Fetch Variations
A critical distinction exists between compound assignment operators and explicit `fetch_*` member functions regarding their return values:
* `atomicVar += 5` executes the addition and returns the **new value** (after modification).
* `atomicVar.fetch_add(5)` executes the addition and returns the **old value** (prior to modification).

### Custom Operations via Compare-and-Swap (CAS)
C++ does not provide native atomic operations for multiplication (`*`), division (`/`), or bit-shifting. To implement missing mathematical operations safely, use a Compare-and-Swap loop with `compare_exchange_weak`:

{% highlight cpp %}
#include <atomic>
#include <iostream>

template <typename T>
void fetch_mult(std::atomic<T>& shared, T mult) {
    T oldValue = shared.load(std::memory_order_relaxed);
    // Re-evaluate in a loop until the atomic swap succeeds
    while (!shared.compare_exchange_weak(oldValue, oldValue * mult,
                                         std::memory_order_release,
                                         std::memory_order_relaxed)) {
        // 'oldValue' is automatically updated with the latest value of 'shared' on failure
    }
}

int main() {
    std::atomic<int> value{10};
    fetch_mult(value, 3);
    std::cout << "Multiplied atomic result: " << value.load() << "\n"; // Outputs 30
    return 0;
}
{% endhighlight %}

<details>
<summary><b>Deep Dive: Why compare_exchange_weak in a loop?</b></summary>
<p>
<code>compare_exchange_weak</code> can fail spuriously on certain hardware architectures (such as ARM LL/SC instruction sequences), even if the underlying value hasn't changed. When placed inside a tight retry loop, <code>compare_exchange_weak</code> yields better performance than <code>compare_exchange_strong</code> because it avoids generating additional conditional branch checks in machine code.
</p>
</details>

---

## 2. Pointer Atomics (`std::atomic<T*>`)

`std::atomic<T*>` enables atomic access to memory addresses and native pointer arithmetic without requiring global locks.

### Pointer Operations & Scaling
* Supports increment and decrement operators: `++`, `--`
* Supports atomic fetch modifications: `fetch_add(n)`, `fetch_sub(n)`

Just like standard C++ raw pointer arithmetic, adding or subtracting an integer scale factor automatically adjusts the target byte offset based on `sizeof(T)`.

{% highlight cpp %}
#include <iostream>
#include <atomic>

struct QuadWord {
    uint64_t data[2]; // 16 bytes
};

int main() {
    QuadWord buffer[5];
    std::atomic<QuadWord*> ptr{buffer};

    // Advances the pointer by 2 * sizeof(QuadWord) bytes (32 bytes)
    QuadWord* old_ptr = ptr.fetch_add(2, std::memory_order_relaxed);

    std::cout << "Original address: " << old_ptr << "\n";
    std::cout << "Updated address:  " << ptr.load() << "\n";
    return 0;
}
{% endhighlight %}

---

## 3. Rules for User-Defined Types (`std::atomic<UserType>`)

You can wrap a custom `struct` or `class` inside `std::atomic<T>`, but the compiler enforces strict design restrictions on `T` to guarantee hardware atomicity:

1. **Trivially Copyable:** The type must have trivial copy/move constructors and assignment operators. It must be safe to copy via `std::memcpy`.
2. **No Virtual Members:** It cannot contain virtual functions (`vptr`) or virtual base classes.
3. **Bitwise Comparable:** Its memory representation must permit byte-for-byte memory comparisons (`std::memcmp`).

### Lock-Free vs. Mutex Fallback
If a user-defined type is too large to fit inside native hardware atomic registers (typically larger than 64 or 128 bits depending on the architecture), the compiler silently injects internal `std::mutex` locks under the hood. Always check hardware execution support using `.is_lock_free()`:

{% highlight cpp %}
#include <iostream>
#include <atomic>

struct Point2D {
    float x;
    float y;
}; // Fits in 64 bits -> Lock-free on modern x86/ARM

struct Matrix4x4 {
    float data[16];
}; // 64 bytes -> Exceeds hardware register limits

int main() {
    std::atomic<Point2D> opt_point;
    std::atomic<Matrix4x4> opt_matrix;

    std::cout << "Point2D is lock-free:  " << (opt_point.is_lock_free() ? "Yes" : "No") << "\n";
    std::cout << "Matrix4x4 is lock-free: " << (opt_matrix.is_lock_free() ? "Yes" : "No") << "\n";

    return 0;
}
{% endhighlight %}

---

## 4. C-Compatible Free Functions & Smart Pointers

### C-Style Free Functions
For compatibility with C APIs or legacy codebases, all `std::atomic` member operations can be invoked via free functions:
* `std::atomic_load(&var)`
* `std::atomic_store(&var, new_val)`
* `std::atomic_fetch_add(&var, 1)`

### Atomic Smart Pointers
While `std::shared_ptr` itself is not thread-safe for concurrent writes, C++ provides mechanisms to safely swap smart pointers across threads:

* **Pre-C++20:** Non-member atomic functions were provided for `std::shared_ptr` (e.g., `std::atomic_load(&ptr)`, `std::atomic_store(&ptr, new_ptr)`).
* **C++20 and Later:** C++20 introduced dedicated atomic smart pointer specializations: `std::atomic<std::shared_ptr<T>>` and `std::atomic<std::weak_ptr<T>>`. These allow atomic reference-count mutations and instance replacements without data races on control blocks.

{% highlight cpp %}
#include <iostream>
#include <memory>
#include <atomic>

struct Config {
    int timeout_ms = 5000;
};

int main() {
    // C++20 explicit atomic shared pointer
    std::atomic<std::shared_ptr<Config>> global_config{
        std::make_shared<Config>()
    };

    // Atomically swap with a new configuration instance
    auto new_config = std::make_shared<Config>();
    new_config->timeout_ms = 10000;

    global_config.store(new_config, std::memory_order_release);

    // Read current config safely
    std::shared_ptr<Config> current = global_config.load(std::memory_order_acquire);
    std::cout << "Active Timeout: " << current->timeout_ms << "ms\n";

    return 0;
}
{% endhighlight %}

---

## Summary Comparison Matrix

| Specialization | Key Operations | Hardware Lock-Free Status | Primary Use Cases |
| :--- | :--- | :--- | :--- |
| **`std::atomic<Integral>`** | `+=`, `-=`, `&=`, `|=`, `^=`, `fetch_*` | Lock-free on native integer sizes | Thread-safe counters, statistics, state bitmasks |
| **`std::atomic<T*>`** | `++`, `--`, `fetch_add`, `fetch_sub` | Lock-free on pointer-sized types | Lock-free data structures, ring buffers, dynamic node pointers |
| **`std::atomic<UserType>`** | `load()`, `store()`, `exchange()`, CAS | Lock-free only if trivially copyable and fits in hardware registers | Small custom POD types, coordinates, state structures |
| **`std::atomic<std::shared_ptr<T>>`** | `load()`, `store()`, `exchange()` | Usually lock-based internal control block mechanics | Dynamic configuration swapping, concurrent data structures (C++20) |