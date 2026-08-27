---
layout: default
title: Determining Return Types in C++98 Function Templates
parent: Techniques
grand_parent: Templates
nav_order: 1
---



# Determining Return Types in C++98 Function Templates

A historical deep-dive into return-type deduction using template traits before `auto` and `decltype`.

<span class="label label-blue">C++98</span>
<span class="label label-purple">Template Metaprogramming</span>
<span class="label label-green">Type Safety</span>

---

## Table of Contents

1. TOC
{:toc}

---

## The Problem

When writing a function template with multiple generic parameters, such as:

{% highlight cpp %}
template <typename T, typename T2>
??? sum(T t, T2 t2) {
    return t + t2;
}
{% endhighlight %}

You cannot easily predict what type `t + t2` will yield. For example:
* `double + double` $\rightarrow$ `double`
* `double + bool` $\rightarrow$ `double`
* `bool + bool` $\rightarrow$ `int` (due to integral promotion)

In modern C++, you can simply rely on trailing return types or `auto`, but C++98 lacks these features.

---

## The C++98 Solution: Template Traits

Because C++98 has no direct mechanism to deduce the result type of an expression at compile time, you must manually define the type-deduction rules using a traits class.

### 1. Define a Primary Template

Act as an interface or default case:

{% highlight cpp %}
template <typename T, typename T2>
struct ReturnType;
{% endhighlight %}

### 2. Provide Full Template Specializations

Map pairs of types directly to their expected result type:

{% highlight cpp %}
template <>
struct ReturnType<double, double> {
    typedef double Type;
};

template <>
struct ReturnType<double, bool> {
    typedef double Type;
};

template <>
struct ReturnType<bool, bool> {
    typedef int Type;
};
{% endhighlight %}

### 3. Use the Trait in the Function Template

{% highlight cpp %}
template <typename T, typename T2>
typename ReturnType<T, T2>::Type sum(T t, T2 t2) {
    return t + t2;
}
{% endhighlight %}

{: .note }
> **Note on `typename`:** The `typename` keyword before `ReturnType<T, T2>::Type` is required because `Type` is a dependent name (a nested type dependent on template parameters).

---

## Key Edge Cases Highlighted in the Article

### Exact Matching Required

Implicit type conversions do not apply when selecting template specializations. If you call `sum(5.5f, 5.0)` (a `float` and a `double`), the compiler will look for `ReturnType<float, double>`. If no specialization matches, compilation fails with a missing definition error.

<details>
<summary>Deep Dive: Compiler Lookup Behavior</summary>
<p>
When a compiler evaluates a template trait lookup like <code>ReturnType&lt;float, double&gt;::Type</code>, it looks for an exact match among all specialized versions of <code>ReturnType</code>. Unlike regular function arguments, template specialization lookup does not perform implicit conversions (such as converting <code>float</code> to <code>double</code>).
</p>
<p>
If no matching specialization is provided, the primary template is selected. If the primary template is only declared (and not defined), accessing <code>::Type</code> results in a compile-time error: <code>incomplete type 'ReturnType&lt;float, double&gt;' used in nested name specifier</code>.
</p>
</details>

### Adding a Default Case

To prevent build errors for unspecialized type pairs, you can give the primary template a fallback type alias:

{% highlight cpp %}
template <typename T, typename T2>
struct ReturnType {
    typedef long double Type; // Default fallback type
};
{% endhighlight %}

---

## Takeaway

In C++98, achieving "automatic" return types requires manual boilerplate through template specialization and traits classes. This technique forms the historical foundation for modern metaprogramming tools like `std::common_type`.