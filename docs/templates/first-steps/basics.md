---
layout: default
title: Basics
parent: First Steps
grand_parent: Templates
nav_order: 1
---

# Insights into C++ Template Instantiation
{: .no_toc }

A deep dive into how the C++ compiler processes templates behind the scenes, highlighting lazy evaluation, instantiation caching, and the power of non-type parameters.
{: .fs-6 .fw-300 }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## The Mechanics of Template Instantiation

Templates allow developers to write generic, highly reusable code. However, a template itself is not a usable class or function—it is simply a blueprint. When you use a template with specific arguments, the compiler creates a concrete class or function out of that family. This automatic generation process is called **template instantiation**.

<span class="label label-blue">Modern C++</span> <span class="label label-green">Under the Hood</span>

Understanding how the compiler generates this code is crucial for writing efficient C++ and keeping binary sizes manageable. Let's examine the core behaviors of the instantiation process.

---

## Template Memoization (Instantiation Caching)

One of the smartest aspects of the C++ compiler is how it manages identical template requests. This process is often referred to as **Template Memoization** or **Instantiation Caching**.

### Instantiating Multiple Times

What happens when you instantiate a template more than once for the exact same type and parameters? Does the compiler bloat your binary with duplicate code?

<details>
<summary><b>View Code Example: Multiple Instantiations</b></summary>

{% highlight cpp %}
template <typename T, int N>
class Array {
public:
    int getSize() const { return N; }
private:
    T elem[N];
};

int main() {
    Array<int, 5> myArr1;   // (1) Triggers initial instantiation
    Array<int, 10> myArr2;  // (2) Triggers a new, separate instantiation
    Array<int, 5> myArr3;   // (3) Caches and reuses (1)
}
{% endhighlight %}
</details>

> **How the Cache Works**
> When `myArr1` is declared, the compiler works to generate the concrete class `Array<int, 5>`. When `myArr3` is declared on line 3 with the *identical template arguments*, the compiler does not generate new code. Instead, it reuses the first instantiation already triggered by line 1. 
{: .note }

This caching mechanism ensures that compile times are minimized and duplicate binaries are avoided. However, note that `Array<int, 5>` and `Array<int, 10>` are treated as two entirely distinct types. Generating instances with different parameters guarantees different generated types.

---

## Template Instantiation is Lazy

A critical performance and design feature in C++ is that **template instantiation is lazy**. Meaning, if you don't need it, it won't be instantiated. 

When you instantiate a class template, the compiler generates the class definition, but it explicitly *omits* the instantiation of its member functions until they are actually invoked in the code.

<details open>
<summary><b>View Code Example: Proving Lazy Evaluation</b></summary>

{% highlight cpp %}
#include <cmath>
#include <string>

template <typename T>
struct Number {
    int absValue() { 
        return std::abs(val); // std::abs won't work on std::string
    }
    T val{};
};

int main() {
    Number<std::string> numb; 
    // numb.absValue(); // (1) If uncommented, this triggers a compilation error!
}
{% endhighlight %}
</details>

> **Why Lazy Instantiation Matters**
> Because the compiler is lazy, the invalid code inside `absValue()` (trying to call `std::abs` on a `std::string`) is completely ignored by the compiler as long as you never actually call `numb.absValue()`. 
{: .warning }

Only the *declaration* of the member function is made available during the class instantiation. The *definition* is deferred until the exact moment of invocation. This flexibility allows generic containers to hold types that might only support a subset of the container's methods.

---

## Non-Type Template Parameters

While developers commonly pass types to templates (using `typename T` or `class T`), C++ also fully supports **Non-Type Template Parameters**, allowing you to pass concrete values directly into the template at compile time.

In our earlier array example, the second parameter `int N` is a non-type template parameter:

{% highlight cpp %}
template <typename T, int N>
class Array { /* ... */ };
{% endhighlight %}

<span class="label label-purple">C++20 Extensions</span>

### Supported Non-Type Parameters
Traditionally, non-type parameters were restricted to:
*   Integral types (`int`, `size_t`, `char`, etc.)
*   Pointers
*   References

With the rollout of C++20, the language expanded this feature to also include **floating-point types**.

### Impact on Type Generation
When you instantiate templates with different non-type values, the compiler strictly enforces them as distinct types:

<details>
<summary><b>View Code Example: Distinct Types</b></summary>

{% highlight cpp %}
int main() {
    Array<float, 5> myArr1;
    Array<float, 10> myArr2;
    
    // myArr1 and myArr2 are completely different types!
    // Assignment like myArr1 = myArr2 is illegal.
}
{% endhighlight %}
</details>

Because `5` and `10` are different values, `Array<float, 5>` and `Array<float, 10>` generate unique compiler code. This is an incredibly powerful feature for enforcing strict compile-time safety and defining fixed-size data structures without incurring the overhead of dynamic memory allocation.