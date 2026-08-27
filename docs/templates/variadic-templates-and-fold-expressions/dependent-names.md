---
layout: default
title: Dependent Names
parent: Variadic Templates and Fold Expressions
grand_parent: Templates
nav_order: 7
---


# Dependent Types and Template Disambiguation

Understand how the C++ compiler distinguishes between types, static variables, and template methods when parsing generic code.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">Templates</span>
<span class="label label-purple">C++20</span>
<span class="label label-yellow">Compiler Parsing</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Introduction

Based on Rainer Grimm's discussion on dependent types, a foundational rule of C++ template compilation focuses on how the compiler analyzes generic code[cite: 1]. When writing code inside a template that depends on a template parameter `T`, the compiler cannot look inside `T` during the first parsing phase because `T` has not been instantiated yet[cite: 1]. 

This creates parsing ambiguities where the compiler must make default assumptions[cite: 1]. If those default assumptions are incorrect, compilation fails[cite: 1]. To resolve these ambiguities, C++ provides two mandatory disambiguating keywords: `typename` and `template`[cite: 1].

---

## 1. The `typename` Keyword for Dependent Nested Types

A dependent type is a type that depends directly on a template parameter `T` (such as `T::iterator` or `T::value_type`)[cite: 1].

### The Ambiguity

Consider this simple line inside a template[cite: 1]:

{% highlight cpp %}
template <typename T>
void process(T container) {
    T::const_iterator* ptr; // Is this a pointer declaration or a multiplication?
}
{% endhighlight %}

Before `T` is instantiated, the compiler faces a parsing dilemma[cite: 1]:

* **Option A (Type):** Is `const_iterator` a nested type inside `T`? (Declaring a pointer `ptr` of type `T::const_iterator`)[cite: 1].
* **Option B (Variable):** Is `const_iterator` a static member variable inside `T`? (Multiplying `T::const_iterator` by a variable named `ptr`)[cite: 1].

> **The C++ Standard Rule:** By default, the compiler assumes any dependent name (`T::something`) is a **variable or member**, NOT a type[cite: 1].

### The Solution

To explicitly inform the compiler that the dependent name is a type rather than a variable, you must prepend the `typename` keyword[cite: 1]:

{% highlight cpp %}
template <typename T>
void process(T container) {
    typename T::const_iterator* ptr; // Disambiguated! 'ptr' is a pointer to a type.
}
{% endhighlight %}

---

## 2. The `template` Disambiguator for Dependent Template Methods

A similar syntax ambiguity occurs when invoking a member template function on a dependent object or pointer[cite: 1].

### The Ambiguity

{% highlight cpp %}
template <typename T>
void execute(T obj) {
    obj.get_value<int>(); // ERROR! Compiler parses '<' as 'less-than' operator!
}
{% endhighlight %}

Because `obj` depends on `T`, the compiler does not know that `get_value` is a template method[cite: 1]. Consequently, it parses the expression as[cite: 1]:

`(obj.get_value) < int` ... followed by a missing `>` operator[cite: 1].

### The Solution

To tell the compiler "the member `get_value` is a template function, so `<` begins its template argument list," insert the `template` keyword directly after the member access operator (`.`, `->`, or `::`)[cite: 1]:

{% highlight cpp %}
template <typename T>
void execute(T obj) {
    obj.template get_value<int>(); // Disambiguated! Correctly parsed as a template call.
}
{% endhighlight %}

<details>
<summary><strong>Deep Dive: Modern C++ Evolution (C++20 Improvement)</strong></summary>

<p>In C++20, the language standard became significantly smarter regarding template parsing[cite: 1]. Following standard proposal <strong>P0634</strong>, the <code>typename</code> keyword became optional in contexts where only a type name makes grammatical sense[cite: 1].</p>

<p>These contexts include function return types, <code>using</code> alias declarations, and <code>type_traits</code> specifiers[cite: 1]:</p>

{% highlight cpp %}
template <typename T>
struct MyContainer {
    using iterator = T::iterator; // Valid in C++20! ('typename' inferred automatically)
};
{% endhighlight %}

</details>

---

## Summary Cheat Sheet

The table below summarizes common syntax parsing ambiguities, their causes, and their disambiguation solutions[cite: 1]:

| Code Syntax | Problem | Solution | Meaning |
| :--- | :--- | :--- | :--- |
| `T::Nested` | Assumed to be a static variable[cite: 1] | `typename T::Nested` | Tells compiler `Nested` is a type[cite: 1] |
| `obj.method<Type>()` | `<` parsed as less-than operator[cite: 1] | `obj.template method<Type>()` | Tells compiler `method` is a template function[cite: 1] |
| `ptr->method<Type>()` | `<` parsed as less-than operator[cite: 1] | `ptr->template method<Type>()` | Tells compiler `method` is a template function via pointer[cite: 1] |
