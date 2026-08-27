---
layout: default
title:  Evolution of Compile-Time Branching
parent: First Steps
grand_parent: Templates
nav_order: 10
---


# Evolution of Compile-Time Branching
<span class="label label-blue">Modern C++</span> <span class="label label-green">C++17 / 20</span> <span class="label label-purple">Metaprogramming</span>

From standard runtime `if-else` statements to C++20 Concepts, modern C++ provides incredibly powerful ways to shift decision-making from the CPU to the compiler. Moving logic to compile-time results in zero-cost abstractions, safer codebases, and more readable generic programming. {: .fs-5 .fw-300 }

## Table of Contents
1. TOC
{:toc}

---

## 1. Runtime Checks vs. Template Specialization

Traditionally, logic branching happens at runtime using values (like Enums) evaluated by the CPU. To eliminate this runtime cost, C++ developers historically used **Template Specialization** to perform checks using *types* during compilation.

The primary template acts as the "else" branch, while the specialization acts as the "if" branch.

{% highlight cpp %}
#include <iostream>

// 1. Define roles as types (instead of runtime enums)
struct User {};
struct Admin {};

// 2. The Primary Template (The "Else" branch)
template <typename T>
struct CanDelete {
    static constexpr bool value = false;
};

// 3. The Full Specialization (The "If" branch)
template <>
struct CanDelete<Admin> {
    static constexpr bool value = true;
};

int main() {
    // Evaluated entirely by the compiler. Zero CPU cost.
    std::cout << "Admin can delete? " << CanDelete<Admin>::value << '\n';
    return 0;
}
{% endhighlight %}

| Feature | Runtime `if-else` | Compile-time Templates |
| :--- | :--- | :--- |
| **When decided?** | While the application is running | During compilation |
| **What is checked?** | Variable values | Variable types |
| **Performance Cost** | CPU branching overhead | Zero cost |

---

## 2. The C++17 Revolution: `if constexpr`

Template specialization requires heavy struct boilerplate. C++17 introduced `if constexpr`, allowing you to write compile-time logic using standard procedural syntax. Its superpower is **discarded statements**: the compiler physically ignores the false branch, preventing compilation errors when a type lacks a specific method.

{% highlight cpp %}
#include <iostream>
#include <type_traits>

struct User {};
struct Admin { void deleteDatabase() { std::cout << "Deleted!\n"; } };

template <typename T>
void executeDeletion(T user) {
    // Evaluated at compile-time
    if constexpr (std::is_same_v<T, Admin>) {
        user.deleteDatabase(); // Safe! Ignored if T is not Admin.
    } else {
        std::cout << "Access denied.\n";
    }
}
{% endhighlight %}

<details>
<summary>Deep Dive: Why this is safer</summary>
If you used a standard <code>if</code> statement here, the compiler would check both branches for validity. Passing a <code>User</code> would cause a compilation error because <code>User</code> does not have a <code>deleteDatabase()</code> method. <code>if constexpr</code> safely strips away the invalid code before the compiler fully parses it.
</details>

---

## 3. C++20 Concepts: Self-Documenting Constraints

While `if constexpr` is fantastic, it hides the logic *inside* the function body. C++20 Concepts fix this by moving type requirements directly into the function signature, enabling "Duck Typing" and producing dramatically cleaner error messages.

{% highlight cpp %}
#include <iostream>

// 1. Define what an Administrator looks like
template <typename T>
concept Administrator = requires(T user) {
    user.deleteDatabase();
};

struct Admin { void deleteDatabase() {} };
struct Guest {};

// 2. Overload 1: Constrained by the Concept
void executeDeletion(Administrator auto& user) {
    user.deleteDatabase();
}

// 3. Overload 2: The Fallback
void executeDeletion(auto& user) {
    std::cout << "Access denied.\n";
}

int main() {
    Admin alice;
    Guest bob;

    executeDeletion(alice); // Matches Concept overload
    executeDeletion(bob);   // Falls back to generic overload
}
{% endhighlight %}

*   **Self-Documenting:** The signature `Administrator auto&` instantly communicates requirements.
*   **Duck Typing:** Any struct with a `deleteDatabase()` method automatically qualifies.
*   **Better Diagnostics:** Compiler errors clearly state which exact constraint failed, rather than dumping pages of template instantiation errors.
