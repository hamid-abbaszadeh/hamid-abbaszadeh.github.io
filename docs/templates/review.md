---
layout: default
title: Review
parent: Templates
nav_order: 5
---

# Overview of Generic Code
{: .no_toc }

When writing modern C++, it is important **not to confuse metaprogramming with basic template usage**. While both help us write flexible code, they solve problems at different scales.
{: .fs-5 .fw-300 }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## The 3 Ways to Write Generic Code

When you need a function to handle different data types, you generally have three approaches:

| Approach | How It Works | Best Used For |
| :--- | :--- | :--- |
| <span class="label label-red">Overloading</span> | Writing a separate function for every single type. | Small, specific cases where logic differs wildly per type. |
| <span class="label label-yellow">Specialization</span> | Creating a general template, but overriding it for a specific type. | Handling "exceptions to the rule" in your templates. |
| <span class="label label-green">Metaprogramming</span> | Writing logic that evaluates types at compile-time and adapts automatically. | Large-scale generic code based on type traits or concepts. |

---

## The Power of Metaprogramming

Basic templates prevent you from rewriting the exact same code for different types. **Metaprogramming** takes this a step further.

> **The Golden Rule**
> 
> Metaprogramming reduces your workload from writing **one function per type** to writing **one function per category of types**.
{: .text-purple-100 }

### A Real-World Example

Imagine you want to print different kinds of data. You might have:

1. <strong class="text-blue-100">50 Custom Classes</strong> (House, Person, Car, Dog...) that all have a `.toString()` method.
2. <strong class="text-blue-100">10 Container Types</strong> (`std::vector`, `std::set`, `std::list`, `std::map`...).
3. <strong class="text-blue-100">10 Primitive Types</strong> (`int`, `float`, `double`...).

<details open>
  <summary>How do we solve this efficiently?</summary>

  <p>If you use pure <strong>Overloading</strong> <span class="label label-red">Bad Idea</span>, you would have to write 70 different functions!</p>

  <p>By using <strong>Metaprogramming</strong> <span class="label label-green">Modern C++</span> (like <code>if constexpr</code> and type traits), you can group these into categories. You reduce your workload from 70 separate functions down to just <strong>3 template functions</strong>:</p>
  <ul>
    <li>One for classes with a <code>.toString()</code> method.</li>
    <li>One for iterable containers.</li>
    <li>One for basic primitives.</li>
  </ul>
</details>

---

[Explore Templates]({% link docs/templates/templates.md %}){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[Back to Multithreading]({% link docs/multithreading-in-modern-cplusplus/multithreading-in-modern-cplusplus.md %}){: .btn .fs-5 .mb-4 .mb-md-0 }