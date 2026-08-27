---
layout: default
title: constexpr Enhancements and consteval in C++20
parent: Techniques
grand_parent: Templates
nav_order: 12
---


# `constexpr` Enhancements and `consteval` in C++20

Explore C++20 compile-time metaprogramming enhancements, including transient dynamic memory allocations, `constexpr` containers, and `consteval` immediate functions.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++20</span>
<span class="label label-purple">Metaprogramming</span>

---

## Table of Contents

1. TOC
{:toc}

---

## `constexpr` Containers & Dynamic Allocation

Prior to C++20, dynamic memory allocation using `new` and `delete` was strictly forbidden inside compile-time evaluation[cite: 1]. C++20 introduced support for **Transient Allocation**, allowing standard library containers such as `std::vector` and `std::string`, along with over 100 STL algorithms, to be declared as `constexpr`[cite: 1].

### Mechanics of Transient Allocation

Memory can be allocated dynamically during compile-time evaluation provided it is deallocated before the compile-time evaluation finishes[cite: 1]. The compiler enforces strict validation during this process: if memory is leaked or improperly freed (e.g., calling `delete` instead of `delete[]`), compilation halts with an explicit error[cite: 1].

{% highlight cpp %}
#include <iostream>
#include <vector>
#include <algorithm>

// Valid compile-time dynamic allocation and sorting[cite: 1]:
constexpr int maxElement() {
    std::vector<int> myVec = {1, 2, 4, 3}; // Memory allocated at compile time[cite: 1]
    std::sort(myVec.begin(), myVec.end()); // Algorithms are constexpr[cite: 1]
    return myVec.back();                   // Memory cleaned up automatically before returning[cite: 1]
}

int main() {
    constexpr int maxValue = maxElement(); // Evaluated at compile time[cite: 1]
    std::cout << "Max value: " << maxValue << "\n";
    return 0;
}
{% endhighlight %}

---

## `consteval` (Immediate Functions)

While a `constexpr` function can execute at compile time or runtime depending on how it is invoked, a `consteval` function **must** execute at compile time[cite: 1]. 

Functions declared with `consteval` are known as **Immediate Functions**[cite: 1]. Every call to an immediate function produces a compile-time constant[cite: 1]. Attempting to pass non-constant expressions or runtime arguments to a `consteval` function results in a compile error[cite: 1].

{% highlight cpp %}
#include <iostream>

consteval int sqr(int n) { 
    return n * n; 
}

int main() {
    constexpr int a = sqr(10); // OK: evaluated at compile time[cite: 1]
    int b = sqr(10);           // OK: evaluated at compile time, initialized into 'b' at runtime[cite: 1]
    
    int x = 10;
    // int c = sqr(x);         // ERROR: 'x' is not a constant expression![cite: 1]

    std::cout << "a: " << a << ", b: " << b << "\n";
    return 0;
}
{% endhighlight %}

---

## Practical Use Case: Pre-computing Non-Const Local Variables

`consteval` guarantees that expensive computation logic occurs exclusively at compile time, while allowing the computed result to initialize standard runtime mutable variables[cite: 1]:

{% highlight cpp %}
#include <iostream>

consteval auto doubleMe(auto val) {
    return 2 * val;
}

int main() {
    auto res = doubleMe(1010); // Guaranteed compile-time calculation (2020)[cite: 1]
    ++res;                     // Modified at runtime (2021)[cite: 1]

    std::cout << "Result: " << res << "\n";
    return 0;
}
{% endhighlight %}

---

## Summary: `constexpr` vs. `consteval`

The table below outlines the core differences between `constexpr` and `consteval` functions[cite: 1]:

| Characteristic | `constexpr` | `consteval` (C++20) |
| :--- | :--- | :--- |
| **Execution Window** | Compile time or runtime[cite: 1] | Compile time only[cite: 1] |
| **Function Type** | Potential constant expression[cite: 1] | Immediate function[cite: 1] |
| **Invalid Call Behavior** | Runs at runtime if arguments aren't constants[cite: 1] | Fails compilation immediately[cite: 1] |
| **Callable By** | `constexpr` or standard runtime functions[cite: 1] | Can only be called in constant contexts[cite: 1] |
| **Calling Other Functions** | Can call `constexpr` or `consteval` functions[cite: 1] | Can call `constexpr` or `consteval` functions[cite: 1] |

<details>
<summary>Click to view custom compile-time string processing example</summary>

{% highlight cpp %}
#include <iostream>
#include <string_view>
#include <algorithm>

// Consteval function enforcing compile-time string validation
consteval bool is_upper(std::string_view sv) {
    return std::all_of(sv.begin(), sv.end(), [](char c) {
        return c >= 'A' && c <= 'Z';
    });
}

int main() {
    static_assert(is_upper("HELLO")); // Valid compile-time check
    
    std::cout << "String verification passed.\n";
    return 0;
}
{% endhighlight %}
</details>