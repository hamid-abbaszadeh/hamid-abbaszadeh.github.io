---
layout: default
title: Type Checks in C++ <type_traits>
parent: Techniques
grand_parent: Templates
nav_order: 6
---



# Type Checks in the C++ `<type_traits>` Library

Explore how compile-time type checks work in the modern C++ `<type_traits>` library, understand the 14 primary type categories, dive under the hood of template specialization mechanics, and write safer template code.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++11 / C++17</span>
<span class="label label-purple">Metaprogramming</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Introduction to Compile-Time Type Checks

The `<type_traits>` header, introduced in C++11 and significantly enhanced in C++14 and C++17, forms the backbone of compile-time template metaprogramming. It enables developers to inspect, query, and modify type properties during compilation—eliminating runtime overhead while maximizing type safety.

---

## The 14 Primary Type Categories

In C++, every single type belongs to **exactly one** primary type category. The `<type_traits>` library provides class templates to check for each category at compile time. Each trait evaluates to a boolean constant exposed via the `::value` member (or `_v` variable template helper in C++17).

Below is the complete list of all 14 primary type categories:

1. **`std::is_void<T>`** — Checks if `T` is `void`.
2. **`std::is_integral<T>`** — Checks if `T` is an integral type (e.g., `int`, `char`, `bool`, `long`).
3. **`std::is_floating_point<T>`** — Checks if `T` is a floating-point type (`float`, `double`, `long double`).
4. **`std::is_array<T>`** — Checks if `T` is an array type of known or unknown bound.
5. **`std::is_pointer<T>`** — Checks if `T` is a raw pointer type (excluding member pointers).
6. **`std::is_null_pointer<T>`** — Checks if `T` is `std::nullptr_t`.
7. **`std::is_member_object_pointer<T>`** — Checks if `T` is a pointer to a non-static data member.
8. **`std::is_member_function_pointer<T>`** — Checks if `T` is a pointer to a non-static member function.
9. **`std::is_enum<T>`** — Checks if `T` is an enumeration type (scoped or unscoped).
10. **`std::is_union<T>`** — Checks if `T` is a union type.
11. **`std::is_class<T>`** — Checks if `T` is a non-union class/struct type.
12. **`std::is_function<T>`** — Checks if `T` is a function type.
13. **`std::is_lvalue_reference<T>`** — Checks if `T` is an lvalue reference (`T&`).
14. **`std::is_rvalue_reference<T>`** — Checks if `T` is an rvalue reference (`T&&`).

---

## Under the Hood: How Type Traits Work

The core mechanics of standard type traits rely on two main C++ metaprogramming concepts: **base helper structures** (`std::integral_constant`) and **explicit template specialization**.

### 1. Base Helper (`std::integral_constant`)

`std::integral_constant` wraps a compile-time value of a specified type into a distinct C++ type. The standard library provides two predefined typedefs for boolean values:

{% highlight cpp %}
namespace std {
    template <class T, T v>
    struct integral_constant {
        static constexpr T value = v;
        using value_type = T;
        using type = integral_constant<T, v>;
        constexpr operator value_type() const noexcept { return value; }
        constexpr value_type operator()() const noexcept { return value; }
    };

    // Standard helper typedefs for boolean flags:
    using true_type  = integral_constant<bool, true>;
    using false_type = integral_constant<bool, false>;
}
{% endhighlight %}

### 2. Primary Template (Default Fallback)

The generic template acts as a default fallback. It inherits from `std::false_type`, asserting that unknown or unspecialized types do not match the trait.

{% highlight cpp %}
template <class T>
struct is_integral : public std::false_type {};
{% endhighlight %}

### 3. Explicit Specializations

Target types are explicitly specialized to inherit from `std::true_type`.

{% highlight cpp %}
template <> struct is_integral<int>                : public std::true_type {};
template <> struct is_integral<unsigned int>       : public std::true_type {};
template <> struct is_integral<char>               : public std::true_type {};
template <> struct is_integral<signed char>        : public std::true_type {};
template <> struct is_integral<unsigned char>      : public std::true_type {};
template <> struct is_integral<short>              : public std::true_type {};
template <> struct is_integral<unsigned short>     : public std::true_type {};
template <> struct is_integral<long>               : public std::true_type {};
template <> struct is_integral<unsigned long>      : public std::true_type {};
template <> struct is_integral<long long>          : public std::true_type {};
template <> struct is_integral<unsigned long long> : public std::true_type {};
template <> struct is_integral<bool>               : public std::true_type {};
// ... (and cv-qualified variations)
{% endhighlight %}

### Compilation Resolution Workflow

When the compiler evaluates `is_integral<int>::value`:
1. The compiler checks for an explicit template specialization for `int`.
2. It finds `struct is_integral<int>`, which inherits from `std::true_type`.
3. `std::true_type::value` resolves to `true`.

When evaluating `is_integral<double>::value`:
1. No explicit specialization matches `double`.
2. The compiler falls back to the primary template `template <class T> struct is_integral`.
3. It inherits from `std::false_type`, so `::value` resolves to `false`.

<details>
<summary>Click to view custom implementation example of <code>is_pointer</code></summary>

{% highlight cpp %}
#include <iostream>
#include <type_traits>

// Custom implementation of is_pointer
template <typename T>
struct MyIsPointer : std::false_type {};

template <typename T>
struct MyIsPointer<T*> : std::true_type {};

int main() {
    std::cout << std::boolalpha;
    std::cout << "int is pointer: " << MyIsPointer<int>::value << "\n";      // false
    std::cout << "int* is pointer: " << MyIsPointer<int*>::value << "\n";    // true
    return 0;
}
{% endhighlight %}
</details>

---

## Modern C++ Convenience: Variable Templates (`_v` Suffix)

Prior to C++17, accessing trait values required appending `::value` to the template instantiation:

{% highlight cpp %}
// C++11 syntax
bool is_int = std::is_integral<T>::value;
{% endhighlight %}

Introduced in C++17, **variable templates** provide a cleaner and less verbose alternative using the `_v` suffix shortcut:

{% highlight cpp %}
// C++17 inline variable template helper
template <class T>
inline constexpr bool is_integral_v = is_integral<T>::value;

// C++17 syntax usage
bool is_int = std::is_integral_v<T>;
{% endhighlight %}

---

## Composite Type Categories, Properties, and Queries

Beyond the 14 primary type categories, `<type_traits>` includes traits for composite categories, type properties, and numerical queries.

### 1. Composite Type Categories
Composite categories are constructed by combining two or more primary type categories.

* **`std::is_fundamental<T>`** — Checks if `T` is fundamental (arithmetic types, `void`, or `std::nullptr_t`).
* **`std::is_arithmetic<T>`** — Checks if `T` is integral or floating-point.
* **`std::is_object<T>`** — Checks if `T` is an object type (types that are not functions, references, or `void`).
* **`std::is_reference<T>`** — Checks if `T` is an lvalue or rvalue reference.
* **`std::is_compound<T>`** — Checks if `T` is non-fundamental (array, function, pointer, class, union, enum, etc.).

### 2. Type Properties
Traits that inspect internal capabilities, construction rules, or qualifiers:

* **`std::is_const<T>`** / **`std::is_volatile<T>`** — CV-qualifier checks.
* **`std::is_empty<T>`** — Checks if `T` is a class with no non-static data members.
* **`std::is_polymorphic<T>`** — Checks if `T` has at least one virtual function.
* **`std::is_copy_constructible<T>`** — Checks if `T` can be copy-constructed.
* **`std::is_trivially_copyable<T>`** — Checks if `T` can be copied byte-for-byte safely (`std::memcpy`).

### 3. Type Property Queries
Traits that return numeric constant values rather than boolean flags:

* **`std::alignment_of<T>::value`** (or `std::alignment_of_v<T>`) — Returns alignment requirements in bytes.
* **`std::rank<T>::value`** (or `std::rank_v<T>`) — Returns the number of dimensions of an array type.
* **`std::extent<T, N>::value`** (or `std::extent_v<T, N>`) — Returns the size of the $N$-th dimension of an array.

<details>
<summary>Click to view practical application example</summary>

{% highlight cpp %}
#include <iostream>
#include <type_traits>

template <typename T>
void inspect_type() {
    std::cout << std::boolalpha;
    std::cout << "Is arithmetic: " << std::is_arithmetic_v<T> << "\n";
    std::cout << "Is fundamental: " << std::is_fundamental_v<T> << "\n";
    std::cout << "Is polymorphic: " << std::is_polymorphic_v<T> << "\n";
    std::cout << "Alignment requirement: " << std::alignment_of_v<T> << " bytes\n";
    std::cout << "Array rank: " << std::rank_v<T> << "\n";
}

int main() {
    std::cout << "--- int[10][20] ---\n";
    inspect_type<int[10][20]>();
    return 0;
}
{% endhighlight %}
</details>