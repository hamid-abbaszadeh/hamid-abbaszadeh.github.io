---
layout: default
title: constexpr if
parent: Techniques
grand_parent: Templates
nav_order: 13
---


# Compile-Time Branching with `if constexpr` in C++17

Discover how C++17's `if constexpr` simplifies template metaprogramming by enabling compile-time conditional compilation, replacing complex template specialization with clean imperative code.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++17 / C++20</span>
<span class="label label-purple">Metaprogramming</span>

---

## Table of Contents

1. TOC
{:toc}

---

## What is `if constexpr`?

Introduced in C++17, `if constexpr` (often called *constexpr if*) evaluates a condition at compile time[cite: 1]. Based on the boolean result[cite: 1]:
* The **true branch** is compiled directly into the binary[cite: 1].
* The **discarded branch** is ignored completely and not compiled[cite: 1].

This mechanism allows template functions to return different types or execute completely different code blocks depending on type traits or compile-time constants without generating compilation errors in the unchosen branch[cite: 1].

{% highlight cpp %}
#include <iostream>
#include <type_traits>

template <typename T>
auto getValue(T t) {
    if constexpr (std::is_pointer_v<T>)
        return *t; // Compiled ONLY when T is a pointer (e.g., int*)[cite: 1]
    else
        return t;  // Compiled ONLY when T is a value type (e.g., int)[cite: 1]
}

int main() {
    int val = 42;
    int* ptr = &val;

    std::cout << "Value: " << getValue(val) << "\n"; // Evaluates else branch[cite: 1]
    std::cout << "Pointer: " << getValue(ptr) << "\n"; // Evaluates true branch[cite: 1]
    return 0;
}
{% endhighlight %}

In contrast, a standard runtime `if` statement requires both branches to be valid and compileable for any given type `T`[cite: 1]. Attempting `*t` when `T` is `int` inside a standard runtime `if` causes a compilation error[cite: 1].

---

## Simplifying Template Metaprogramming (TMP)

Historically (C++98/C++11), compile-time branching and recursion required class templates with explicit and partial specializations[cite: 1]. `if constexpr` eliminates this boilerplate, allowing compile-time logic to be written using familiar imperative control flow[cite: 1].

### Example 1: Factorial Calculation

#### Traditional TMP (Multiple Class Templates)
Historically, recursion required a primary template and a base-case specialization[cite: 1]:

{% highlight cpp %}
// Primary template
template <int N>
struct Factorial {
    static int const value = N * Factorial<N-1>::value;[cite: 1]
};

// Termination base-case specialization
template <>
struct Factorial<1> {
    static int const value = 1;[cite: 1]
};
{% endhighlight %}

#### Modern C++17 `if constexpr` (Single Function)
With C++17, the entire recursive sequence fits inside a single function body[cite: 1]:

{% highlight cpp %}
template <int N>
constexpr int factorial() {
    if constexpr (N >= 2)
        return N * factorial<N-1>();[cite: 1]
    else
        return N;[cite: 1]
}
{% endhighlight %}

### Example 2: Fibonacci Sequence

* **Traditional TMP:** Requires 3 `struct` templates (1 primary template + 2 explicit specializations for $N=1$ and $N=0$)[cite: 1].
* **C++17 `if constexpr`:** Requires a single function containing a standard `if constexpr (N >= 2)` branch[cite: 1].

---

## Integration with C++20 Concepts

The condition supplied to `if constexpr` must evaluate to a compile-time boolean predicate[cite: 1]. While C++17 relies on type traits (e.g., `std::is_integral_v<T>`), C++20 concepts can be passed directly to constrain inline compile-time branches[cite: 1]:

{% highlight cpp %}
#include <iostream>
#include <concepts>

template <typename T>
auto get_value(T t) {
    if constexpr (std::integral<T>)
        return t;[cite: 1]
    else
        return *t;[cite: 1]
}

int main() {
    int number = 100;
    int* ptr = &number;

    std::cout << get_value(number) << "\n"; // Integral branch
    std::cout << get_value(ptr) << "\n";    // Non-integral (pointer) branch
    return 0;
}
{% endhighlight %}

---

## Summary of Differences

| Feature | Standard `if` | `if constexpr` (C++17) |
| :--- | :--- | :--- |
| **Evaluation Time** | Runtime[cite: 1] | Compile time[cite: 1] |
| **Discarded Branch** | Executed or skipped at runtime; must compile[cite: 1] | Not compiled into the binary[cite: 1] |
| **Condition Type** | Any boolean expression[cite: 1] | Compile-time constant expression / predicate[cite: 1] |
| **Primary Purpose** | Flow control based on runtime state[cite: 1] | Branching on types, traits, or compile-time values[cite: 1] |

<details>
<summary>Click to view custom compile-time Fibonacci implementation</summary>

{% highlight cpp %}
#include <iostream>

template <int N>
constexpr int fibonacci() {
    if constexpr (N >= 2)
        return fibonacci<N-1>() + fibonacci<N-2>();
    else
        return N;
}

int main() {
    constexpr int fib10 = fibonacci<10>();
    std::cout << "Fibonacci(10) = " << fib10 << "\n"; // Output: 55
    return 0;
}
{% endhighlight %}
</details>