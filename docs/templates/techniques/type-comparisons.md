---
layout: default
title: Type Comparisons in C++ <type_traits>
parent: Techniques
grand_parent: Templates
nav_order: 7
---


# Type Comparisons in the C++ `<type_traits>` Library

Learn how to evaluate relationships between two types at compile time with zero runtime overhead using `std::is_same`, `std::is_base_of`, and `std::is_convertible`.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++11 / C++17 / C++20</span>
<span class="label label-purple">Metaprogramming</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Introduction to Compile-Time Type Comparisons

Evaluating relationships between types during compilation is a cornerstone of modern template metaprogramming[cite: 1]. Type comparisons allow developers to constrain template arguments, optimize algorithms based on inheritance, and enforce interface requirements—all with zero runtime performance cost[cite: 1].

---

## The Three Primary C++11 Type Comparisons

C++11 introduced three fundamental metafunctions to analyze how two types interact[cite: 1]:

1. **`std::is_same<T, U>`** — Checks if type `T` and type `U` are exact identical types[cite: 1].
2. **`std::is_base_of<Base, Derived>`** — Checks if `Base` is a base class of `Derived`, or if both are the exact same class type[cite: 1].
3. **`std::is_convertible<From, To>`** — Checks if an expression of type `From` can be implicitly converted to type `To`[cite: 1].

*(Note: Modern standard additions like C++20's `is_pointer_interconvertible_with_class` build upon these foundation concepts[cite: 1]).*

---

## Deep Dive: How `std::is_same` Works

`std::is_same` is the simplest comparison trait to implement. It relies on basic template partial specialization:

{% highlight cpp %}
namespace rgr {
    // 1. Base template defaults to false_type
    template<class T, class U> 
    struct is_same : false_type {};

    // 2. Partial specialization for identical types evaluates to true_type
    template<class T> 
    struct is_same<T, T> : true_type {};
}
{% endhighlight %}

### Critical Detail: Qualified vs. Unqualified Types

`std::is_same` performs an strict check. It treats `const` and `volatile` cv-qualifiers as fundamental components of the type:

* `std::is_same<int, const int>::value` $\rightarrow$ `false`
* `std::is_same<int, volatile int>::value` $\rightarrow$ `false`
* `std::is_same<int, int>::value` $\rightarrow$ `true`

If your requirement is to compare types while ignoring `const` and `volatile` qualifiers, strip them first using `std::remove_cv`:

{% highlight cpp %}
template<typename T, typename U>
struct isSameIgnoringConstVolatile : rgr::integral_constant<
    bool, 
    rgr::is_same<typename std::remove_cv<T>::type, 
                 typename std::remove_cv<U>::type>::value
> {};
{% endhighlight %}

---

## Standard Implementations: `is_base_of` & `is_convertible`

More complex traits like `std::is_base_of` and `std::is_convertible` rely on **SFINAE** (Substitution Failure Is Not An Error) and overload resolution rules.

### 1. Structure of `std::is_base_of`

`std::is_base_of` verifies inheritance hierarchy through SFINAE overload resolution. It tests whether a pointer of type `Derived*` can be static-casted or implicitly converted to `Base*` via internal helper overload signatures (`test_pre_is_base_of`).

### 2. Structure of `std::is_convertible`

`std::is_convertible` leverages `std::declval` inside a `decltype` expression. It tests whether the construct `To t = std::declval<From>()` forms a valid expression without instantiating actual runtime objects.

<details>
<summary>Click to view template specialization demonstration</summary>

{% highlight cpp %}
#include <iostream>
#include <type_traits>

class Base {};
class Derived : public Base {};
class Unrelated {};

int main() {
    std::cout << std::boolalpha;
    
    // is_same checks
    std::cout << "is_same<int, int>: " 
              << std::is_same_v<int, int> << "\n"; // true
    std::cout << "is_same<int, const int>: " 
              << std::is_same_v<int, const int> << "\n"; // false

    // is_base_of checks
    std::cout << "is_base_of<Base, Derived>: " 
              << std::is_base_of_v<Base, Derived> << "\n"; // true
    std::cout << "is_base_of<Derived, Base>: " 
              << std::is_base_of_v<Derived, Base> << "\n"; // false

    // is_convertible checks
    std::cout << "is_convertible<Derived*, Base*>: " 
              << std::is_convertible_v<Derived*, Base*> << "\n"; // true
    std::cout << "is_convertible<Base*, Derived*>: " 
              << std::is_convertible_v<Base*, Derived*> << "\n"; // false

    return 0;
}
{% endhighlight %}
</details>

---

## Type Comparison Summary

Below is a cheat sheet summarizing the differences between the core comparison traits:

| Trait | Evaluates to `true` when: | Example (`true`) | Example (`false`) |
| :--- | :--- | :--- | :--- |
| **`is_same<T, U>`** | `T` and `U` are exact identical types. | `is_same<int, int32_t>` | `is_same<int, const int>` |
| **`is_base_of<B, D>`** | `B` is a base class of `D`, or `B` and `D` are the same class type. | `is_base_of<Base, Derived>` | `is_base_of<Derived, Base>` |
| **`is_convertible<F, T>`** | Expressions of type `F` can be implicitly converted to `T`. | `is_convertible<Derived*, Base*>` | `is_convertible<Base*, Derived*>` |