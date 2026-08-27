---
layout: default
title: Template Arguments
parent: First Steps
grand_parent: Templates
nav_order: 7
---


# Template Arguments & Type Deduction
<span class="label label-blue">Modern C++</span> <span class="label label-green">C++11/17/20</span> <span class="label label-purple">Core Mechanics</span>

Understanding how the compiler deduces template arguments is crucial for writing robust, bug-free generic code. The rules for template type deduction do not only apply to function templates (C++98) but also to `auto` (C++11), class templates (C++17), and concepts (C++20). {: .fs-5 .fw-300 }

## Table of Contents
1. TOC
{:toc}

---

## 1. The Three Rules of Type Deduction

When deducing the template type, three entities come into play: `T`, `ParameterType`, and the expression passed to the function. The compiler deduces two types: the actual template parameter `T` and the fully resolved `ParameterType`. The behavior changes dramatically based on how the parameter is declared:

*   **Pass by Value:** The deduced type ignores reference qualifiers (`&`). Furthermore, if the expression is `const` or `volatile`, those qualifiers are also ignored.
*   **Pass by Reference/Pointer:** The reference or pointer is added to the deduced type. Crucially, the `constness` or `volatileness` of the original expression is respected and preserved.
*   **Pass by Universal Reference (`&&`):** When the expression is an lvalue, the resulting type becomes an lvalue reference. When it is an rvalue, it becomes an rvalue reference.

---

## 2. Why This Matters (Practical Examples)

Understanding these rules prevents dangerous bugs related to accidental copying, lost `const` safety, and unexpected array behavior. Because `auto` type deduction uses the exact same rules as template type deduction, mastering this concept is mandatory for modern C++ development.

### Code Example: Pitfalls and Solutions

{% highlight cpp %}
template <typename T> void passByValue(T param);
template <typename T> void passByRef(T& param);

int main() {
    const int myData = 42;
    int myArr[5] = {1, 2, 3, 4, 5};

    // --- 1. Losing Const Safety ---
    passByValue(myData); // T deduced as 'int'. Const is stripped!
    passByRef(myData);   // T deduced as 'const int'. Const is preserved!

    // --- 2. Unexpected Array Decay ---
    // When passed by value, implicit array-to-pointer conversion is applied.
    passByValue(myArr);  // T deduced as 'int*'. Array decays!
    
    // When passed by reference, size information is retained.
    passByRef(myArr);    // T deduced as 'int[5]'. No decay!

    // --- 3. The 'auto' Connection ---
    // Regard 'auto' as the replacement for T.
    auto val = myData;   // val is 'int' (Const stripped)
    auto& ref = myData;  // ref is 'const int&' (Const preserved)
}
{% endhighlight %}

<details>
<summary>Deep Dive: Array Decay</summary>
When you invoke a function template by value with a C-array, the C-array decays to a pointer to its first element. Decay means that an implicit conversion (like array-to-pointer or lvalue-to-rvalue) is applied. This is why calculating the size of a passed-by-value array inside a template function will yield the size of a pointer, not the original array. Passing by reference prevents this decay entirely.
</details>