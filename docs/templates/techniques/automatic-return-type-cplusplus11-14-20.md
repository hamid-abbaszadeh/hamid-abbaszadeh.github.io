---
layout: default
title: Evolution of Return-Type Deduction in C++
parent: Techniques
grand_parent: Templates
nav_order: 2
---


# Evolution of Return-Type Deduction in C++

How modern C++ standards progressively simplified return-type deduction for function templates like `sum(T t, T2 t2)`[cite: 1].

<span class="label label-blue">C++11</span>
<span class="label label-green">C++14</span>
<span class="label label-purple">C++20</span>
<span class="label label-yellow">Type Safety</span>

---

## Table of Contents

1. TOC
{:toc}

---

## The Evolution Across Standards

The challenge of determining template return types has evolved significantly from the verbose boilerplate of C++98. Modern C++ standards introduce cleaner, more expressive language features to inspect types and enforce compile-time constraints[cite: 1].

---

## C++11: Type Traits & Trailing Return Types

C++11 introduced two main approaches to determine the return type without custom template boilerplate[cite: 1]:

### 1. `std::common_type`

`std::common_type` determines the shared type to which both parameters can be implicitly converted[cite: 1].

{% highlight cpp %}
template <typename T, typename T2>
typename std::common_type<T, T2>::type sum(T t, T2 t2) {
    return t + t2;
}
{% endhighlight %}

### 2. `auto` with `decltype` (Trailing Return Type)

Inspects the actual result type of the expression `t + t2`[cite: 1].

{% highlight cpp %}
template <typename T, typename T2>
auto sum(T t, T2 t2) -> decltype(t + t2) {
    return t + t2;
}
{% endhighlight %}

{: .note }
> **Redundancy Warning:** Repeating `t + t2` in both the return type declaration and function body is redundant and error-prone[cite: 1].

---

## C++14: Direct Return Type Deduction

C++14 eliminated redundant syntax by allowing the compiler to inspect the `return` statement directly[cite: 1]:

{% highlight cpp %}
template <typename T, typename T2>
auto sum(T t, T2 t2) {
    return t + t2;
}
{% endhighlight %}

The compiler automatically deduces the return type as the exact type evaluated by `t + t2`[cite: 1].

---

## C++20: Constrained Placeholders (Concepts)

C++20 adds type safety and explicit intent through Concepts, ensuring only valid types are accepted while keeping concise syntax[cite: 1]:

{% highlight cpp %}
template <typename T>
concept Arithmetic = std::is_arithmetic<T>::value;

Arithmetic auto sum(Arithmetic auto t, Arithmetic auto t2) {
    return t + t2;
}
{% endhighlight %}

This restricts inputs to arithmetic types at compile time, providing clear compiler errors if non-arithmetic types are passed[cite: 1].

<details>
<summary>Click to view concept evaluation & compiler diagnostic benefits</summary>
<p>
Without concepts, passing incompatible types like <code>std::string</code> or a custom struct into <code>sum()</code> results in deep template instantiation errors inside the function body.
</p>
<p>
By constraining parameters with <code>Arithmetic auto</code>, the failure occurs at the call site before function template instantiation begins. This yields short, human-readable compiler errors stating that the argument fails the constraint test.
</p>
</details>

---

## Key Takeaways

### `std::common_type` vs. Expression Deduction (`decltype` / `auto`)
* `std::common_type<T, T2>` finds a shared target type for both inputs[cite: 1].
* `decltype(t + t2)` or plain C++14 `auto` evaluates the exact result type of the `+` operator[cite: 1].

### Progression of Clean Syntax
* **C++98 / C++11:** Verbose boilerplate and explicit traits classes[cite: 1].
* **C++14:** Clean, auto-deduced code[cite: 1].
* **C++20:** Type-safe, constrained templates[cite: 1].
