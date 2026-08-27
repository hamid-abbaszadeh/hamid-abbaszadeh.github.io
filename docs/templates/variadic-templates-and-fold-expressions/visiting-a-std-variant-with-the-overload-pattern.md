---
layout: default
title: "Visiting a std::variant with the Overload Pattern"
parent: Variadic Templates and Fold Expressions
grand_parent: Templates
nav_order: 5
---

# Visiting a std::variant with the Overload Pattern

Process type-safe unions cleanly in modern C++ without clunky type-checking logic or rigid `if-else` / `std::holds_alternative` chains.
{: .fs-5 .fw-300 }

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++17</span>
<span class="label label-purple">C++20</span>
<span class="label label-yellow">Pattern Matching</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Introduction

Modern C++ applications frequently rely on `std::variant` to represent values that can hold one of several distinct types safely at runtime. However, processing these type-safe unions traditionally required cumbersome boilerplate or chained `std::holds_alternative` checks. 

The **Overload Pattern** resolves this by pairing `std::visit` with a compact variadic helper construct. This pattern brings clean, compile-time pattern matching directly into modern C++ workflows.

---

## The Problem: Handling a `std::variant`

A `std::variant` holds one of several distinct types at any given time [cite: 1]. To process its value safely at runtime, C++ provides `std::visit` [cite: 1].

`std::visit` requires a Callable Object (like a struct with overloaded `operator()`) that can handle every possible type inside the variant [cite: 1]. Writing a separate visitor struct for every variant operation gets verbose fast [cite: 1]:

### The Traditional (Verbose) Way

{% highlight cpp %}
struct MyVisitor {
    void operator()(int i) const { std::cout << "int: " << i << '
'; }
    void operator()(const std::string& s) const { std::cout << "str: " << s << '
'; }
};

std::variant<int, std::string> v = "Hello";
std::visit(MyVisitor{}, v); // Verbose!
{% endhighlight %}

---

## The Solution: The Overload Pattern

The Overload Pattern allows you to construct a single visitor object on the fly using inline lambdas [cite: 1]. It takes only 2 lines of template code to build [cite: 1]:

{% highlight cpp %}
template <typename... Ts>
struct overload : Ts... {
    using Ts::operator()...; // C++17 pack expansion of using-declarations
};

// C++17 Class Template Argument Deduction (CTAD) guide
template <typename... Ts>
overload(Ts...) -> overload<Ts...>;
{% endhighlight %}

> **C++ Standard Note:** In C++20, the explicit Class Template Argument Deduction (CTAD) guide is no longer needed—the struct template alone handles deduction automatically [cite: 1].

---

## How the Magic Works Under the Hood

The pattern relies on three modern C++ template mechanisms [cite: 1]:

1. **Variadic Multiple Inheritance (`struct overload : Ts...`):**  
   When you pass multiple lambdas into `overload{ [](...){}, [](...){} }`, the compiler generates a struct that directly inherits from every unique lambda type [cite: 1].

2. **Variadic `using` Declarations (`using Ts::operator()...`):**  
   Each lambda has its own distinct `operator()` [cite: 1]. By default, C++ hides inherited member functions with the same name [cite: 1]. Unpacking `using Ts::operator()...` pulls every inherited `operator()` into a single, unified overload set [cite: 1].

3. **Compile-Time Dispatch (`std::visit`):**  
   When `std::visit` executes, it passes the variant's active value into the `overload` object [cite: 1]. The compiler matches the active type to the correct lambda using standard C++ overload resolution [cite: 1].

---

## Complete Example in Action

{% highlight cpp %}
#include <iostream>
#include <variant>
#include <string>

// 1. The Overload Pattern boilerplate
template <typename... Ts>
struct overload : Ts... { using Ts::operator()...; };

int main() {
    using VarType = std::variant<int, double, std::string>;
    VarType v1 = 42;
    VarType v2 = "Modern C++";

    // 2. Inline, type-safe pattern matching
    auto visitor = overload{
        [](int i) { std::cout << "Got an int: " << i << '
'; },
        [](double d) { std::cout << "Got a double: " << d << '
'; },
        [](const std::string& s) { std::cout << "Got a string: " << s << '
'; }
    };

    std::visit(visitor, v1); // Output: Got an int: 42
    std::visit(visitor, v2); // Output: Got a string: Modern C++
}
{% endhighlight %}

<details>
<summary><strong>Deep Dive: Key Advantages</strong></summary>

<ul>
  <li><strong>Type Safety:</strong> If you forget to handle one of the types stored in the <code>std::variant</code>, the code will not compile [cite: 1].</li>
  <li><strong>Zero Overhead:</strong> Lambdas and inline visitors are completely inlined by modern compilers; there is zero virtual function table overhead [cite: 1].</li>
  <li><strong>Functional Pattern Matching:</strong> Gives C++ an expressive pattern-matching syntax similar to Rust (<code>match</code>) or Haskell [cite: 1].</li>
</ul>

</details>

---

## Summary Overview

| Component | Mechanism | Role in Pattern |
| :--- | :--- | :--- |
| `struct overload : Ts...` | Variadic Inheritance | Derives from all input lambda closure types [cite: 1] |
| `using Ts::operator()...` | Pack Expansion | Exposes all inherited `operator()`s in one overload set [cite: 1] |
| `overload(Ts...) -> overload<Ts...>` | CTAD Guide (C++17) | Enables type deduction without explicit template params [cite: 1] |
| `std::visit` | Variant Visitor | Performs compile-time dispatch to the matching lambda [cite: 1] |