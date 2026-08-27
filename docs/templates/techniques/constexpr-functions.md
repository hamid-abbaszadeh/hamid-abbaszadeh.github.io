---
layout: default
title: constexpr Functions in C++
parent: Techniques
grand_parent: Templates
nav_order: 11
---


# `constexpr` Functions in Modern C++

Explore how `constexpr` functions enable dual execution at compile time and runtime, simplifying compile-time evaluation compared to traditional Template Metaprogramming (TMP).

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++11 / C++14</span>
<span class="label label-purple">Metaprogramming</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Dual Execution: Compile Time vs. Runtime

Declaring a function as `constexpr` does not guarantee that it will execute at compile time[cite: 1]. Instead, it signals to the compiler that the function has the *potential* to be evaluated at compile time if provided with constant expressions[cite: 1].

A `constexpr` function is evaluated at compile time if:
* It is evaluated in an explicit compile-time context (e.g., inside `static_assert`, array bounds, or template arguments)[cite: 1].
* Its return value is directly assigned to a `constexpr` variable[cite: 1].

Otherwise, the compiler invokes the function at runtime just like a standard function[cite: 1].

{% highlight cpp %}
#include <iostream>

constexpr auto gcd(int a, int b) {
    while (b != 0) {
        auto t = b;
        b = a % b;
        a = t;
    }
    return a;
}

int main() {
    // Evaluated at COMPILE TIME (emits raw constant 11 in assembly)
    constexpr int i = gcd(11, 121);[cite: 1]

    // Evaluated at RUNTIME (generates a standard function call)
    int a = 11, b = 121;[cite: 1]
    int j = gcd(a, b);[cite: 1]

    std::cout << "Compile-time result: " << i << "\n";
    std::cout << "Runtime result: " << j << "\n";
    return 0;
}
{% endhighlight %}

---

## `constexpr` Functions vs. Template Metaprogramming (TMP)

Before `constexpr` functions were introduced, compile-time logic relied on Template Metaprogramming (TMP)[cite: 1]. While both approaches achieve compile-time calculations, `constexpr` functions allow imperative programming idioms rather than functional, recursive template expansion[cite: 1].

| Property | Template Metaprogramming (TMP) | `constexpr` Functions |
| :--- | :--- | :--- |
| **Programming Paradigm** | Pure functional (no mutable state)[cite: 1] | Standard imperative C++[cite: 1] |
| **Looping Mechanism** | Recursion[cite: 1] | Standard loops (`for`, `while`)[cite: 1] |
| **Conditional Logic** | Template partial/full specialization[cite: 1] | Standard `if` / `switch` statements[cite: 1] |
| **Value Modification** | Generates new types/constants per step[cite: 1] | Modifies local variables directly[cite: 1] |
| **Execution Time** | Strictly compile time[cite: 1] | Compile time or runtime[cite: 1] |
| **Error Handling** | Verbose template compiler errors[cite: 1] | Standard function compiler errors[cite: 1] |

---

## Compiler Checking & Visibility Rules

`constexpr` functions follow compilation rules similar to template definitions[cite: 1]:

1. **Two-Phase Syntax Checking:** The compiler validates the general function syntax during initial parsing[cite: 1]. It performs a second check upon each invocation to verify that the passed arguments are valid constant expressions[cite: 1].
2. **Definition Visibility:** Like templates, the full definition of a `constexpr` function must be visible within the translation unit where it is called[cite: 1]. Consequently, `constexpr` functions are typically placed directly in header files[cite: 1].

<details>
<summary>Click to view custom implementation example</summary>

{% highlight cpp %}
#include <iostream>
#include <array>

// Compile-time factorial function
constexpr std::size_t factorial(std::size_t n) {
    std::size_t result = 1;
    for (std::size_t i = 1; i <= n; ++i) {
        result *= i;
    }
    return result;
}

int main() {
    // Used directly as an array bound at compile time
    std::array<int, factorial(4)> my_array; // Size 24

    std::cout << "Array size: " << my_array.size() << "\n";
    return 0;
}
{% endhighlight %}
</details>