---
layout: default
title: The Special Friendship of Templates
parent: Variadic Templates and Fold Expressions
grand_parent: Templates
nav_order: 6
---


# Special Friendship of Templates

Understand and master the complex relationship between C++ friend declarations and template instantiations.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">Templates</span>
<span class="label label-purple">Encapsulation</span>
<span class="label label-red">Pitfalls</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Introduction

In standard C++, a `friend` declaration allows an outside class or function to access private and protected members of a class[cite: 1]. However, when templates enter the picture, configuring friendship becomes significantly more complex[cite: 1]. 

Depending on software architecture needs, friendship can be established as one-to-one, one-to-many, or non-template-to-template relationships[cite: 1]. Understanding these patterns is essential for maintaining proper encapsulation while leveraging the flexibility of C++ templates[cite: 1].

---

## 1. Non-Template Class with a Template Friend (One-to-Many)

### Concept

A standard, non-template class can grant friendship to a function or class template[cite: 1]. This grants **all instantiations** of that template full access to the non-template class's private members[cite: 1].

### Code Implementation

{% highlight cpp %}
class SecretBank {
private:
    int secretCode = 1234;

    // Grants friendship to ANY instantiation of Auditor<T>
    template <typename T>
    friend class Auditor;
};

template <typename T>
class Auditor {
public:
    void inspect(SecretBank bank) {
        // Works for Auditor<int>, Auditor<std::string>, etc.
        std::cout << bank.secretCode << '\n'; 
    }
};
{% endhighlight %}

---

## 2. Template Class with a Non-Template Friend

### Concept

A class template can grant friendship to a standard, non-template function or class[cite: 1]. Every instantiation of the class template will trust that single, concrete entity[cite: 1].

### Code Implementation

{% highlight cpp %}
void globalPrinter(); // Forward declaration

template <typename T>
class DataBox {
private:
    T data;

    // Standard non-template function is a friend to ALL DataBox<T> instantiations
    friend void globalPrinter(); 
};
{% endhighlight %}

---

## 3. Template Class with a Specific Template Friend (One-to-One / Bound Friendship)

### Concept

This is the most common pattern when writing template classes (such as custom container types or math matrices)[cite: 1]. You want `DataBox<int>` to be friends only with `printData<int>`, but **not** with `printData<double>`[cite: 1].

Because the friend template parameter matches the class template parameter (`T`), you must forward-declare both the friend template and the class template beforehand[cite: 1].

### Code Implementation

{% highlight cpp %}
// 1. Forward declarations required
template <typename T> class DataBox;
template <typename T> void printData(const DataBox<T>& box);

// 2. Class template definition
template <typename T>
class DataBox {
private:
    T value;

public:
    DataBox(T v) : value(v) {}

    // 3. Bound Friendship: Notice the '<T>' after printData!
    // DataBox<int> is ONLY friends with printData<int>
    friend void printData<T>(const DataBox<T>& box);
};

template <typename T>
void printData(const DataBox<T>& box) {
    std::cout << box.value << '\n'; // Accesses private 'value'
}
{% endhighlight %}

<details>
<summary><strong>The Pitfall & Trap to Avoid</strong></summary>

<p><strong>The Trap:</strong> If you forget the <code>&lt;T&gt;</code> specialization syntax in <code>friend void printData&lt;T&gt;(...)</code>, the compiler will assume you are declaring a brand-new, standard non-template function rather than referencing the template function[cite: 1].</p>

<p>This subtle error manifests at link time as a <strong>Linker Error (Undefined Reference)</strong> because the compiler expects a non-template function definition that does not exist[cite: 1].</p>

</details>

---

## 4. Template Class with an Unbound Template Friend (Many-to-Many)

### Concept

If you want every instantiation of a template class to be friends with every instantiation of a friend template (regardless of types), you declare a nested template inside the `friend` declaration[cite: 1].

### Code Implementation

{% highlight cpp %}
template <typename T>
class DataBox {
private:
    T value;

public:
    DataBox(T v) : value(v) {}

    // Unbound Friendship: Uses a DIFFERENT template parameter 'U'
    // DataBox<int> is friends with Converter<double>, Converter<std::string>, etc.
    template <typename U>
    friend class Converter;
};
{% endhighlight %}

---

## Summary Matrix

The following table summarizes the key patterns for template friendship[cite: 1]:

| Friendship Type | Syntax Inside Class | Scope of Access |
| :--- | :--- | :--- |
| **Bound (One-to-One)** | `friend void func<T>(...);` | `Class<X>` is friends only with `func<X>`[cite: 1]. |
| **Unbound (Many-to-Many)** | `template <typename U> friend class FriendClass;` | `Class<X>` is friends with `FriendClass<Y>` for all types `Y`[cite: 1]. |
| **Non-Template Friend** | `friend void func(...);` | Single non-template function accesses all `Class<T>` instantiations[cite: 1]. |