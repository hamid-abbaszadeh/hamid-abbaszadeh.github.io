---
layout: default
title: Template Specialization (Primary, Partial, and Full)
parent: First Steps
grand_parent: Templates
nav_order: 9
---


# Primary, Partial, and Full Specialization
<span class="label label-blue">Modern C++</span> <span class="label label-purple">Template Metaprogramming</span> <span class="label label-green">Code Optimization</span>

Templates allow us to write generic code, but sometimes generic isn't good enough. You might need a highly optimized implementation for a specific data type or custom behavior for pointers. C++ solves this through **Template Specialization**, allowing you to define custom rules for specific types while falling back to the generic template for everything else. {: .fs-5 .fw-300 }

## Table of Contents
1. TOC
{:toc}

---

## 1. The Primary Template (The Fallback)

The primary template is your baseline. It defines the generic behavior that will be used if no specific specialization matches the provided type. The compiler always looks at the primary template first to understand the blueprint of the class or function.

{% highlight cpp %}
#include <iostream>
#include <string>

// The Primary Template
template <typename T>
struct TypeAnalyzer {
    static void print() {
        std::cout << "This is a standard generic type.\n";
    }
};
{% endhighlight %}

---

## 2. Full (Explicit) Specialization

Full specialization occurs when you provide a custom implementation for an *exact, specific type* (like `int`, `double`, or a custom `User` class). In this case, all template parameters are bound to specific types. 

The syntax requires an empty `template <>` prefix to tell the compiler: "I am providing an explicitly customized version of an existing template."

{% highlight cpp %}
// Full Specialization for 'int'
template <>
struct TypeAnalyzer<int> {
    static void print() {
        std::cout << "This is specifically an integer! Fast math applied.\n";
    }
};

// Full Specialization for 'std::string'
template <>
struct TypeAnalyzer<std::string> {
    static void print() {
        std::cout << "This is a string. Handling text data.\n";
    }
};
{% endhighlight %}

---

## 3. Partial Specialization

Partial specialization is where template metaprogramming shines. Instead of specializing for one exact type, you specialize for a *family* of types (like all pointers, all references, or all `std::vector<T>`).

Unlike full specialization, partial specialization still leaves some template parameters generic.

{% highlight cpp %}
// Partial Specialization for ANY pointer type (T*)
template <typename T>
struct TypeAnalyzer<T*> {
    static void print() {
        std::cout << "This is a pointer to some type. Memory address incoming.\n";
    }
};

// Partial Specialization for ANY std::vector
#include <vector>
template <typename T>
struct TypeAnalyzer<std::vector<T>> {
    static void print() {
        std::cout << "This is a dynamic array (std::vector).\n";
    }
};
{% endhighlight %}

<details>
<summary>Deep Dive: Class vs. Function Templates</summary>
While <strong>Class Templates</strong> can be both fully and partially specialized, <strong>Function Templates</strong> can ONLY be fully specialized. You cannot partially specialize a function template. If you need partial specialization-like behavior for a function, you must either overload the function or wrap it inside a partially specialized class/struct template.
</details>

---

## 4. Why This Matters: Practical Examples

Template specialization is not just an academic exercise. It is heavily used in the C++ Standard Library and high-performance applications to optimize code or change semantics.

### Example A: Customizing Formatter Semantics
Imagine a logging system that safely prints values, but you want to mask sensitive data like passwords.

{% highlight cpp %}
template <typename T>
struct Logger {
    static void log(const T& data) {
        std::cout << "Log: " << data << "\n";
    }
};

struct Password { std::string value; };

// Full Specialization to prevent logging raw passwords
template <>
struct Logger<Password> {
    static void log(const Password& data) {
        std::cout << "Log: ******** (Redacted)\n";
    }
};
{% endhighlight %}

### Example B: Memory Optimization (The `std::vector<bool>` case)
The C++ Standard Library uses partial specialization to optimize `std::vector` specifically for booleans. A standard `std::vector<T>` allocates a full byte (or more) per element. However, `std::vector<bool>` is specialized to pack 8 booleans into a single byte, drastically reducing memory usage.

{% highlight cpp %}
// Conceptual view of how the Standard Library optimizes vector<bool>

// Primary Template: Normal allocation
template <typename T>
class my_vector {
    T* data; 
};

// Full Specialization: Bit-packing optimization for bools
template <>
class my_vector<bool> {
    unsigned int* bit_array; // Stores bits instead of full bytes
};
{% endhighlight %}

### Putting It All Together

{% highlight cpp %}
int main() {
    TypeAnalyzer<double>::print();          // Uses Primary
    TypeAnalyzer<int>::print();             // Uses Full Specialization
    TypeAnalyzer<int*>::print();            // Uses Partial Specialization (T*)
    TypeAnalyzer<std::vector<float>>::print(); // Uses Partial Specialization (vector)
    
    return 0;
}
{% endhighlight %}
