---
layout: default
title: Variadic Templates and Fold Expressions
parent: Templates
nav_order: 2
has_children: true
---


# Variadic Templates and Fold Expressions
<span class="label label-blue">Modern C++</span> <span class="label label-green">C++11 / C++17</span> <span class="label label-purple">Variadic Templates</span>

Variadic Templates are a feature introduced in C++11 that solve a classic programming problem: how do you write a function or class that accepts an arbitrary number of arguments, all of which can be completely different types? Before C++11, developers had to write dozens of overloaded functions just to handle different amounts of arguments. Variadic templates replace all of that boilerplate with a single, magical syntax.

## Table of Contents
1. TOC
{:toc}

---

## 1. The Power of the Three Dots (...)

The core of a variadic template is the ellipsis (`...`). The three dots create a **Parameter Pack**. You can do exactly two things with a parameter pack: **Pack it** or **Unpack it**. The compiler knows which one you want based on where you place the dots.

*   **Packing (Dots on the left):** If the `...` is to the left of the parameter name, it gathers a list of arguments into a single pack.
*   **Unpacking (Dots on the right):** If the `...` is to the right of the parameter name, it expands the pack back out into a comma-separated list of arguments.

{% highlight cpp %}
// 1. PACKING types into a template parameter pack 'Args'
template <typename... Args> 
// 2. PACKING values into a function parameter pack 'args'
void variadicFunction(Args... args) {
    
    // 3. UNPACKING 'args' to pass them along to another function
    someOtherFunction(args...); 
}
{% endhighlight %}

### Checking the Size
Because variadic templates are resolved at compile time, you can instantly know how many arguments were passed into the pack using a special operator: `sizeof...`

{% highlight cpp %}
template <typename... Args>
void countArguments(Args... args) {
    int numberOfArgs = sizeof...(args); // Returns the exact count
}
{% endhighlight %}

### Where are they used?
If you have used modern C++, you have already used variadic templates without knowing it. The Standard Template Library (STL) relies on them heavily:
*   `std::tuple`: A data structure that can hold any number of completely unrelated types (e.g., `std::tuple<int, double, std::string>`).
*   `std::thread`: When you create a thread, you pass it a function, followed by an arbitrary number of arguments that your specific function requires.
*   `std::lock`: Can lock an arbitrary number of mutexes in a single atomic step to prevent deadlocks.

---

## 2. Variadic Processing Paradigms

Variadic templates process parameter packs at compile-time using two primary paradigms: **Recursive Unpacking** (the traditional C++11 method) and **Fold Expressions** (the modern C++17 approach).

### How Variadic Processing Works
Because a parameter pack cannot be looped over with a standard `for` loop, you must expand it.

#### Traditional C++11: Recursive Unpacking
Recursive unpacking works similarly to structural recursion: you process the first element (the head) and pass the remaining elements (the tail) back into the same function. A base-case function (with zero or one arguments) is required to stop the recursion.

{% highlight cpp %}
#include <iostream>

// 1. BASE CASE: Stops recursion when there are no arguments left
void printAll() {
    std::cout << '\n';
}

// 2. RECURSIVE TEMPLATE: Takes the FIRST element and PACKS the rest
template <typename First, typename... Rest>
void printAll(First head, Rest... tail) {
    std::cout << head << " ";
    
    // Recurse with the remaining arguments (UNPACKING 'tail')
    printAll(tail...); 
}

int main() {
    // Calling with completely different types and varying count
    printAll(1, "hello", 3.14, 'c');
}
{% endhighlight %}

<details>
<summary>What the Compiler Generates Behind the Scenes</summary>
At compile time, the compiler generates a chain of specialized function overloads:
{% highlight cpp %}
printAll(1, "hello", 3.14, 'c'); // Calls printAll<int, const char*, double, char>
 └── printAll("hello", 3.14, 'c'); // Calls printAll<const char*, double, char>
      └── printAll(3.14, 'c');    // Calls printAll<double, char>
           └── printAll('c');     // Calls printAll<char>
                └── printAll();   // Calls base-case printAll()
{% endhighlight %}
</details>

#### Modern C++17: Fold Expressions
C++17 eliminated the need for base-case functions and recursion boilerplate by introducing fold expressions. A fold expression applies a binary operator across all elements of a pack in a single line.

{% highlight cpp %}
#include <iostream>

// Sum an arbitrary number of values
template <typename... Args>
auto sum(Args... args) {
    return (... + args); // Unary left fold: ((arg1 + arg2) + arg3)...
}

// Print an arbitrary number of values using the comma operator
template <typename... Args>
void printModern(Args... args) {
    ((std::cout << args << " "), ...); // Applies cout to every item
    std::cout << '\n';
}

int main() {
    std::cout << "Sum: " << sum(10, 20, 30, 40) << '\n'; // 100
    printModern(1, "hello", 3.14, 'c');
}
{% endhighlight %}

---

## 3. Real-World Applications in the C++ Standard Library (STL)

The STL utilizes variadic templates to provide flexible, type-safe interfaces. Here are three primary examples:

### A. In-Place Construction: `std::vector::emplace_back`
Unlike `push_back`, which creates a temporary object and copies/moves it into the container, `emplace_back` uses a variadic template to forward arguments directly to the element's constructor inside the vector's allocated memory.

{% highlight cpp %}
#include <vector>
#include <string>

struct User {
    std::string name;
    int age;
    double score;

    User(std::string n, int a, double s) : name(n), age(a), score(s) {}
};

int main() {
    std::vector<User> users;

    // Direct construction in memory; variadic args matched to User constructor
    users.emplace_back("Alice", 30, 95.5);
    users.emplace_back("Bob", 25, 88.0);
}
{% endhighlight %}

### B. Heterogeneous Data Storage: `std::tuple`
Unlike `std::pair`, which is fixed to two elements, `std::tuple` relies on a variadic class template to hold an arbitrary number of types.

{% highlight cpp %}
#include <iostream>
#include <tuple>
#include <string>

int main() {
    // std::tuple<typename... Types>
    std::tuple<int, std::string, double, char> student(101, "Carol", 3.9, 'A');

    // Access elements via index
    std::cout << "ID: " << std::get<0>(student) << '\n';
    std::cout << "Name: " << std::get<1>(student) << '\n';
}
{% endhighlight %}

### C. Type-Safe Formatting: `std::format` (C++20) / `std::print` (C++23)
Prior to C++20, `printf` provided variadic arguments via C-style `va_list`, which was type-unsafe and prone to runtime crashes. Modern C++ uses variadic templates to validate and format arguments safely at compile time.

{% highlight cpp %}
#include <print> // C++23 (or <format> in C++20)

int main() {
    int id = 42;
    double value = 99.9;
    
    // Variadic arguments parsed safely according to the format string
    std::println("ID: {}, Value: {:.2f}", id, value);
}
{% endhighlight %}

---

## 4. Deep Dive: Fold Expression Syntax & Cheat Sheet

In C++17, a fold expression reduces a parameter pack over a specific binary operator (like `+`, `-`, `*`, `&&`, or even `,`).

To fully grasp fold expressions, you only need to look at two things:
1. **Where are the three dots (`...`)?** This determines if the compiler groups the operations from left-to-right or right-to-left.
2. **Is there an initial value?** This determines if it is a Unary (no initial value) or Binary (has an initial value) fold.

| Type | Syntax | Mathematical Expansion (Assuming `args` is `a, b, c`) |
| :--- | :--- | :--- |
| **Unary Left Fold** | `(... op args)` | `((a op b) op c)` |
| **Unary Right Fold** | `(args op ...)` | `(a op (b op c))` |
| **Binary Left Fold** | `(init op ... op args)` | `(((init op a) op b) op c)` |
| **Binary Right Fold** | `(args op ... op init)` | `(a op (b op (c op init)))` |

*(Note: The outer parentheses around the fold expression are mandatory in C++ syntax).*

### Unary Folds (No Initial Value)
Unary folds use only the values provided inside the parameter pack. To see the difference between Left and Right folds, addition (`+`) is a bad example because `(1+2)+3` is the same as `1+(2+3)`. Let's use subtraction (`-`), where grouping drastically changes the result.

{% highlight cpp %}
#include <iostream>

// Unary Left Fold: Evaluates left-to-right
template <typename... Args>
int unaryLeftSub(Args... args) {
    return (... - args); 
}

// Unary Right Fold: Evaluates right-to-left
template <typename... Args>
int unaryRightSub(Args... args) {
    return (args - ...); 
}

int main() {
    // Unary Left expands to: ((10 - 5) - 2) = (5 - 2) = 3
    std::cout << "Left Fold:  " << unaryLeftSub(10, 5, 2) << '\n'; 
    
    // Unary Right expands to: (10 - (5 - 2)) = (10 - 3) = 7
    std::cout << "Right Fold: " << unaryRightSub(10, 5, 2) << '\n'; 
}
{% endhighlight %}

### Binary Folds (Providing an Initial Value)
Sometimes you want to fold a pack, but you want the chain of operations to start with a specific base value. This is where binary folds come in. You place the `init` value on the side where you want the evaluation to begin. Let's use a standard `std::string` concatenation as an example.

{% highlight cpp %}
#include <iostream>
#include <string>

// Binary Left Fold: Starts with 'init', then adds args left-to-right
template <typename... Args>
std::string addPrefix(std::string init, Args... args) {
    return (init + ... + args);
}

// Binary Right Fold: Evaluates right-to-left, ending with 'init'
template <typename... Args>
std::string addSuffix(std::string init, Args... args) {
    return (args + ... + init);
}

int main() {
    using namespace std::string_literals;

    // Left Fold expands to: ((("ID_" + "User") + "_") + "42")
    // Result: "ID_User_42"
    std::cout << addPrefix("ID_"s, "User"s, "_"s, "42"s) << '\n';

    // Right Fold expands to: ("User" + ("_" + ("42" + "_END")))
    // Result: "User_42_END"
    std::cout << addSuffix("_END"s, "User"s, "_"s, "42"s) << '\n';
}
{% endhighlight %}

### The Most Useful Fold Expression: The Comma Operator
While math is great for explaining how folds work, in professional C++ code, the most common fold expression doesn't use math at all. It uses the comma operator (`,`).

The comma operator evaluates the left side, throws away the result, and then evaluates the right side. Combined with a fold expression, it allows you to execute a function on every item in a pack without writing any recursive templates.

{% highlight cpp %}
#include <iostream>

template <typename T>
void processSingle(T item) {
    std::cout << "Processed: " << item << '\n';
}

template <typename... Args>
void processAll(Args... args) {
    // Unary Right Fold using the comma operator.
    // Expands to: processSingle(arg1), (processSingle(arg2), processSingle(arg3));
    (processSingle(args) , ...);
}

int main() {
    processAll(42, "Warning", 3.14);
    // Output:
    // Processed: 42
    // Processed: Warning
    // Processed: 3.14
}
{% endhighlight %}

---

## 5. Empty Parameter Packs & Fold Edge Cases

If you pass an empty parameter pack (zero arguments) to a Binary Fold, it works completely fine because the `init` value acts as the fallback result. However, if you pass an empty pack to a Unary Fold (which has no `init` value), it is a compile-time error for almost all operators.

Here is the exact behavior dictated by the C++ standard:

### 1. Binary Folds with Empty Packs (Always Safe)
Because a binary fold explicitly includes an initial value, passing zero arguments simply returns that initial value.

{% highlight cpp %}
template <typename... Args>
int sumWithBase(Args... args) {
    return (100 + ... + args); // Binary Left Fold
}

int main() {
    return sumWithBase(); // Returns 100! No compile error.
}
{% endhighlight %}

### 2. Unary Folds with Empty Packs (Mostly an Error)
If there are no elements in the pack and no `init` value, the compiler has no idea what value or type to produce. Therefore, unary fold expressions over an empty parameter pack are ill-formed.

{% highlight cpp %}
template <typename... Args>
auto multiply(Args... args) {
    return (... * args); // Unary Left Fold
}

int main() {
    multiply(); // COMPILE ERROR: fold expression has empty expansion
}
{% endhighlight %}

### 3. The Only Three Exceptions (The Safe Unary Operators)
To prevent unnecessary compile errors in common metaprogramming patterns, the C++ standard explicitly defines fallback values for exactly three operators when used in a unary fold with an empty parameter pack:

| Operator | Syntax Example | Result for Empty Pack | Meaning |
| :--- | :--- | :--- | :--- |
| **Logical AND (`&&`)** | `(... && args)` | `true` | Vacuous truth (all elements satisfy condition) |
| **Logical OR (`\|\|`)** | `(... \|\| args)` | `false` | No elements satisfy condition |
| **Comma Operator (`,`)** | `(args , ...)` | `void()` | Evaluates to an empty void expression |

#### Example: Check if all conditions are true
{% highlight cpp %}
#include <iostream>

template <typename... Args>
bool checkAll(Args... args) {
    return (... && args);
}

int main() {
    // Unary fold over empty pack using '&&'
    bool result = checkAll(); 
    
    std::cout << std::boolalpha << result << '\n'; // Prints: true
}
{% endhighlight %}

> **Best Practice:** If you are writing a generic library function using fold expressions and you expect users might call it with zero arguments, either:
> 1. Use a **Binary Fold** to provide an explicit default fallback value (e.g., `(0 + ... + args)` instead of `(... + args)`).
> 2. Constrain the template using C++20 Concepts or a `static_assert(sizeof...(args) > 0)` to fail early with a clear, custom error message.