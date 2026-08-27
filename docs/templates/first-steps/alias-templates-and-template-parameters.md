---
layout: default
title: Alias Templates and Template Parameters
parent: First Steps
grand_parent: Templates
nav_order: 6
---

# Alias Templates & Template Parameters
<span class="label label-blue">Modern C++</span> <span class="label label-green">C++11 / 14 / 17</span> <span class="label label-purple">Type Safety</span>

Modern C++ offers powerful mechanisms for defining highly readable, type-safe generic code. **Alias templates** provide a seamless way to name families of types, while the rich variety of **template parameters** (types, non-types, and template-template parameters) allows developers to shift logic to compile-time, boosting both performance and safety. {: .fs-5 .fw-300 }

## Table of Contents
1. TOC
{:toc}

---

## 1. Alias Templates: Intuitive Type Naming

Introduced in C++11, alias templates use the `using` keyword to give a convenient name to a family of types. Unlike traditional `typedef`s, alias templates can be partially bound, making them an incredible tool for expressing architectural intent directly in code.

### Partially Bound Templates
Consider a generic `Matrix` class with three dimensions of customization: the underlying type, the number of lines, and the number of columns. 

{% highlight cpp %}
template <typename T, int Line, int Col>
class Matrix {
    // ... matrix implementation ...
};
{% endhighlight %}

If we want to represent special cases—like a `Square` (lines equal columns) or a `Vector` (a single column)—we can use alias templates to partially bind the original parameters.

{% highlight cpp %}
// (1) A Square matrix reduces parametrization to Type and Size
template <typename T, int Size>
using Square = Matrix<T, Size, Size>; 

// (2) A Vector restricts the column count to 1
template <typename T, int Line>
using Vector = Matrix<T, Line, 1>; 
{% endhighlight %}

This drastically improves readability. Using `Square<int, 4>` is much safer and clearer than manually typing `Matrix<int, 4, 4>` every time.

### The C++14 Type-Traits Helpers
Alias templates revolutionized the `<type_traits>` library. Pre-C++14, removing a reference required verbose `typename` and `::type` extraction:

{% highlight cpp %}
static_cast<typename std::remove_reference<T>::type&&>(arg); // C++11
{% endhighlight %}

C++14 introduced the `_t` suffix using alias templates, heavily reducing visual clutter:

{% highlight cpp %}
template< class T >
using remove_reference_t = typename std::remove_reference<T>::type;

static_cast<std::remove_reference_t<T>&&>(arg); // C++14: Clean and concise
{% endhighlight %}

---

## 2. The Three Flavors of Template Parameters

Templates are not restricted to just generic "Types". They can accept three distinct categories of parameters, allowing for robust compile-time polymorphism.

### Type Parameters
The most ubiquitous template parameter, representing a type (e.g., `int`, `std::string`, or custom classes).

{% highlight cpp %}
std::vector<int> myVec;
std::map<std::string, double> myMap;
std::lock_guard<std::mutex> myLockGuard;
{% endhighlight %}

### Non-Type Parameters (Compile-Time Values)
Non-types are values evaluated at compile-time. They enforce memory bounds and configuration at compile time, eliminating runtime overhead. Supported non-types include:
*   Integral values (e.g., sizes, dimensions)
*   Pointers and Lvalue references
*   `nullptr`
*   Enumerators
*   **Floating-point values (Since C++20)**

A classic example is `std::array`, where the size is hardcoded into the type signature itself for optimal performance and bounds-safety:

{% highlight cpp %}
std::array<int, 5> myArray{1, 2, 3, 4, 5}; // '5' is a non-type parameter
{% endhighlight %}

### Template Template Parameters
Sometimes, you need to pass a template *as* a parameter to another template. For example, if you want a custom `Matrix` to use an underlying standard container (like `std::vector`), but you want the user to specify *which* container template to use:

{% highlight cpp %}
// (1) Pre-C++17 Syntax (using 'class')
template <typename T, template <typename, typename> class Cont>
class Matrix { /* ... */ };
{% endhighlight %}

Notice the nested `template <typename, typename> class Cont`. It specifies that `Cont` must be a template that takes two parameters (e.g., the element type and its allocator, which fits `std::vector`).

<details>
<summary>Modernizing with C++17</summary>
Before C++17, you were forced to use the <code>class</code> keyword for template template parameters. Since C++17, you can use the more semantically accurate <code>typename</code> keyword:

{% highlight cpp %}
// (2) C++17 Syntax (using 'typename')
template <typename T, template <typename, typename> typename Cont>
class Matrix { /* ... */ };
{% endhighlight %}
</details>

---

## 3. Architectural Perspective: Why This Matters

*   **Zero-Cost Abstractions:** Non-type parameters (like array sizes or dimensional constraints) are baked directly into the binary layout. The compiler can aggressively optimize these values, leading to higher execution speeds.
*   **Self-Documenting Code:** Alias templates map dense, multi-parameter generic code into domain-specific terms (e.g., `Square` instead of `Matrix<T, N, N>`).
*   **Compile-Time Safety:** By demanding template-template parameters or non-type parameters, you explicitly constrain what developers can pass into your libraries. If a developer tries to pass a dynamically-sized `std::forward_list` into a template requiring a compile-time size, the compilation simply fails—preventing subtle runtime crashes.