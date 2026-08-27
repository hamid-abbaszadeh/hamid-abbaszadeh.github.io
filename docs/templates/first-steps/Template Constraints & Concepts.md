---
layout: default
title: Template Constraints & Concepts
parent: First Steps
grand_parent: Templates
nav_order: 14
---

# Template Constraints & Concepts
<span class="label label-blue">Modern C++</span> <span class="label label-green">C++20</span> <span class="label label-purple">Metaprogramming</span>

This text highlights one of the most fascinating (and sometimes dangerous) quirks of C++ templates: The compiler will completely ignore broken code inside a template, as long as you don't use it. We will explore the exact difference between Implicit (Lazy) and Explicit (Eager) instantiation, and how to safely constrain your types using C++11 `static_assert` and C++20 Concepts.

## Table of Contents
1. TOC
{:toc}

---

## 1. Implicit (Lazy) vs. Explicit (Eager) Instantiation

The author clarifies the exact difference between these instantiations using a very clever example. Let’s break down exactly what the code is proving.

*   **Implicit Instantiation is "Lazy":** When you write `Number<std::string> numb;`, you rely on implicit instantiation. The compiler says: *"I will only generate the memory for the `std::string` variable. I see there is an `absValue()` function, but since you didn't call it, I'm not even going to look at the code inside it."* Because it ignores the uncalled function, the code compiles perfectly, even though `std::abs(std::string)` is garbage and syntactically invalid.
*   **The Trigger:** If you actually call `numb.absValue();`, the compiler is finally forced to generate the machine code. It looks inside, realizes you can't calculate the absolute math value of a text string, and throws a massive error.
*   **Explicit Instantiation is "Eager":** Explicit instantiation acts like a strict boss telling the compiler: *"Do not wait for me to call these functions. Build them right now."* 
    *   `template class Number<std::string>;` forces the compiler to instantly generate machine code for every single method, whether used or not. It hits the `std::abs` error and crashes immediately.
    *   `template int Number<std::string>::absValue();` is a targeted eager instantiation, which again causes an instant error.

<details>
<summary>Deep Dive: Why does this actually matter in real C++?</summary>
This "lazy" behavior isn't a bug; it is a highly intentional design choice that makes C++ templates incredibly powerful. It allows you to write partially compatible types.
Imagine a massive template class like <code>std::vector&lt;T&gt;</code>:
<ul>
    <li>It has a method called <code>.clear()</code>, which requires the type <code>T</code> to be destructible.</li>
    <li>It has a method called <code>.resize()</code>, which requires the type <code>T</code> to have a default constructor.</li>
</ul>
Because of lazy instantiation, you can create a <code>std::vector</code> of a custom type that doesn't have a default constructor! The compiler will happily compile your code, as long as you never actually call <code>.resize()</code>. If templates were eager by default, you wouldn't be able to use <code>std::vector</code> at all unless your type satisfied the requirements for every single method.
</details>

---

## 2. Enforcing Constraints: `static_assert` vs. Concepts

If you want to intentionally defeat lazy instantiation and force the compiler to reject an invalid type the exact moment someone types `Number<std::string> numb;`, you need to put your constraints on the class itself.

### The C++11 Way: `static_assert`

A `static_assert` evaluates a condition at compile time. By placing it directly inside the class body (not inside a method), the compiler is forced to evaluate it the moment the class is instantiated.

{% highlight cpp %}
#include <cmath>
#include <string>
#include <type_traits> // Required for type checks

template <typename T>
struct Number {
    // 1. The compiler checks this immediately upon class instantiation
    static_assert(std::is_arithmetic_v<T>, "FATAL: T must be a numeric type!");

    int absValue() { return std::abs(val); }
    T val{};
};

int main() {
    Number<int> goodNum; // Compiles silently.
    
    // ERROR TRIPPED IMMEDIATELY! 
    // You don't even have to call numb.absValue()
    Number<std::string> numb; 
}
{% endhighlight %}

**Pros & Cons:** You get a highly specific, human-readable error message. However, the compiler still starts instantiating the class before hitting the wall, meaning it can sometimes spew out a few lines of internal template jargon.

### The C++20 Way: Concepts and `requires`

C++20 Concepts are the ultimate solution. Instead of letting the compiler try to instantiate the class and then failing an internal `static_assert`, Concepts act as a bouncer at the door. If the type doesn't meet the requirements, the compiler refuses to even begin instantiation.

{% highlight cpp %}
#include <cmath>
#include <string>
#include <type_traits>

// Use a 'requires' clause directly on the template signature
template <typename T>
requires std::is_arithmetic_v<T>
struct Number {
    int absValue() { return std::abs(val); }
    T val{};
};

int main() {
    Number<int> goodNum; 
    Number<std::string> numb; // ERROR TRIPPED IMMEDIATELY!
}
{% endhighlight %}

**The Upgrade:** The compiler error is incredibly clean. It won't complain about `std::abs` or missing methods. It simply tells you: `error: template constraint failure / note: the expression 'is_arithmetic_v<T>' evaluated to false`. Always prefer Concepts in C++20.

---

## 3. Building Custom C++20 Concepts

To build a custom Concept in C++20, use the `requires` expression. Think of the `requires` block as a compile-time sandbox: you write hypothetical code inside it, and if the compiler can successfully compile that code, the type passes.

{% highlight cpp %}
#include <iostream>
#include <string>
#include <concepts> // Required for std::same_as

// 1. Define the concept
template <typename T>
concept Serializable = requires(T obj) {
    // REQUIREMENT 1: Simple property check (must have public 'version')
    obj.version; 
    
    // REQUIREMENT 2: Compound requirement (Method + Return Type)
    { obj.serialize() } -> std::same_as<std::string>;
};

// A struct that PASSES the concept
struct User {
    int version = 1;
    std::string serialize() { return "{ user: data }"; }
};

// A struct that FAILS (missing 'version', and returns void)
struct BadData {
    void serialize() {}
};

// 2. Apply the concept to a function
void sendToNetwork(Serializable auto& data) {
    std::cout << "v" << data.version << " : " << data.serialize() << '\n';
}

int main() {
    User alice;
    sendToNetwork(alice); // Compiles perfectly!
    
    // sendToNetwork(BadData{}); // ERROR: required expression 'obj.version' is invalid
    return 0;
}
{% endhighlight %}

<details>
<summary>Checking for Nested Types</summary>
Sometimes you don't want to check a method or a variable, but a nested type (like <code>std::vector::iterator</code>). You can do this using the <code>typename</code> keyword inside the requires block:
{% highlight cpp %}
template <typename T>
concept HasValueType = requires {
    // Tests if T::value_type exists
    typename T::value_type; 
};
{% endhighlight %}
</details>

---

## 4. Combining Concepts

Combining C++20 concepts is incredibly straightforward. You use the exact same logical operators you already use in standard C++: `&&` (AND) and `||` (OR).

You can combine concepts by creating a brand-new "mega concept," or by combining them on the fly directly on a function.

{% highlight cpp %}
#include <iostream>
#include <string>

// 1. Two small, isolated concepts
template <typename T>
concept Printable = requires(T obj) { obj.print(); };

template <typename T>
concept Serializable = requires(T obj) { obj.serialize(); };

// 2. The "Mega Concept": Combine with AND (&&)
template <typename T>
concept Networkable = Printable<T> && Serializable<T>;

// 3. Combining with OR (||) on the fly
template <typename T>
requires Printable<T> || Serializable<T>
void processData(T& data) {
    std::cout << "Processing valid data...\n";
}

struct ServerLog { void print() {} void serialize() {} };
struct LocalLog { void print() {} }; // Missing serialize()

void broadcast(Networkable auto& data) {
    std::cout << "Broadcasting...\n";
}

int main() {
    ServerLog sLog;
    LocalLog lLog;

    processData(sLog); // OK: Satisfies both
    processData(lLog); // OK: Satisfies Printable (|| constraint)

    broadcast(sLog);   // OK: Satisfies both (&& constraint)
    // broadcast(lLog); // ERROR: required expression 'obj.serialize()' is invalid
    return 0;
}
{% endhighlight %}

> **Best Practice:** Write small, modular concepts and combine them with `&&`. This provides excellent reusability and enables **Constraint Subsumption**—the compiler automatically picks the best function overload based on how many concepts a type satisfies (e.g., `ConceptA && ConceptB` is more specialized than just `ConceptA`).