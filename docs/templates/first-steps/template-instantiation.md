---
layout: default
title: Template Instantiation Strategies
parent: First Steps
grand_parent: Templates
nav_order: 12
---


# Template Instantiation Strategies
<span class="label label-blue">Modern C++</span> <span class="label label-purple">Build Performance</span> <span class="label label-green">C++11</span>

Think of a template as a cookie cutter. It is not a real function yet; it’s just the shape of a function. The compiler needs the cookie cutter to bake the actual cookies (the machine code). 

## Table of Contents
1. TOC
{:toc}

---

## 1. The Normal Way (Implicit Instantiation)

Usually, you have to put the entire template code inside your `.h` header file.

**Math.h**
{% highlight cpp %}
// The compiler needs to see the whole implementation here
template <typename T>
T add(T a, T b) {
    return a + b;
}
{% endhighlight %}

<details>
<summary>What happens behind the scenes?</summary>
If you include <code>Math.h</code> in 50 different <code>.cpp</code> files and call <code>add(5, 10)</code> in all of them, the compiler blindly bakes 50 identical <code>int</code> cookies. Later, the linker says, "Wait, I only need one!" and deletes the other 49. This wastes a massive amount of compile time.
</details>

---

## 2. The Fix: Explicit Instantiation

What if we want to hide the implementation inside a `.cpp` file, just like normal functions, so we only compile it once? 

If you just move the code to a `.cpp` file normally, you will get a Linker Error. But we can fix this using Explicit Instantiation. We tell the compiler exactly which versions to build ahead of time. Here is how you split it up:

**Math.h (Just the declaration)**
{% highlight cpp %}
// Look, no implementation! Just the declaration.
template <typename T>
T add(T a, T b);
{% endhighlight %}

**Math.cpp (The implementation AND explicit instantiation)**
{% highlight cpp %}
#include "Math.h"

// 1. The hidden implementation
template <typename T>
T add(T a, T b) {
    return a + b;
}

// 2. EXPLICIT INSTANTIATION
// We are forcing the compiler to build these specific versions right now.
template int add<int>(int, int);
template double add<double>(double, double);
{% endhighlight %}

**main.cpp (Using it)**
{% highlight cpp %}
#include "Math.h"

int main() {
    // The compiler sees the declaration in Math.h and trusts the linker.
    // The linker finds the pre-baked 'int' version inside Math.cpp!
    int result = add(5, 10); 
    
    // ERROR: add(5.5f, 2.0f); 
    // We didn't explicitly instantiate a 'float' version in Math.cpp!
    
    return 0;
}
{% endhighlight %}

**Why is this awesome?**
*   **Faster Compilation:** The code for `add` is only compiled exactly once inside `Math.cpp`, not 50 times across your project.
*   **Hidden Source Code:** If you are writing a closed-source library, you don't have to expose all your secret logic in the header file. You just expose the specific types you support (like `int` and `double`).

---

## 3. The C++11 `extern template` Trick

In the previous example, we solved the compilation problem by completely hiding the template implementation inside a `.cpp` file. 

But sometimes you can't do that. What if you want the compiler to be able to inline your template functions for maximum performance? To inline a function, the compiler must see the full implementation in the header file. If you put the implementation back in the header, we are back to the original problem: the compiler will generate duplicate code in every single `.cpp` file that includes it.

C++11 introduced `extern template` to solve this exact dilemma. It allows you to keep the full implementation in the header, but tells the compiler: *"Stop! Do not generate the machine code for this type here. I promise I already built it in another file."*

Here is how you set it up across three files:

**1. The Header File (Implementation + extern)**
**Logger.h**
{% highlight cpp %}
#pragma once
#include <iostream>
#include <string>

// 1. The FULL implementation is in the header
template <typename T>
class Logger {
public:
    void print(T message) {
        std::cout << "[LOG]: " << message << '\n';
    }
};

// 2. THE C++11 EXTERN TRICK
// We know std::string is going to be used constantly across our project.
// This line tells every file that includes Logger.h: 
// "DO NOT instantiate Logger<std::string>. Trust the linker."
extern template class Logger<std::string>;
{% endhighlight %}

**2. The Single Source File (The Actual Build)**
Now we need exactly one file in our entire project to actually build the machine code, otherwise the linker will fail.

**Logger.cpp**
{% highlight cpp %}
#include "Logger.h"

// 3. EXPLICIT INSTANTIATION
// Notice there is no 'extern' here. 
// Because this is missing 'extern', the compiler will actually bake 
// the Logger<std::string> machine code right here, exactly once.
template class Logger<std::string>;
{% endhighlight %}

**3. The Usage Files**
**main.cpp**
{% highlight cpp %}
#include "Logger.h"

int main() {
    Logger<std::string> myLogger;
    
    // The compiler sees the 'extern' in the header. 
    // It skips generating the code and just leaves a note for the linker: 
    // "Go find Logger<std::string>::print() later."
    myLogger.print("Hello World!"); 
    
    // What if we use a type we DIDN'T mark as extern?
    Logger<int> intLogger;
    
    // The compiler falls back to standard behavior (Implicit Instantiation).
    // It builds the 'int' version right here in main.cpp.
    intLogger.print(42);
    
    return 0;
}
{% endhighlight %}

**The Best of Both Worlds**
By using `extern template`, you get two massive benefits:
*   **Fast Builds:** The heavily used `Logger<std::string>` is only compiled once (in `Logger.cpp`), drastically reducing compile time and object file sizes.
*   **High Performance:** Because the source code is still fully visible in `Logger.h`, the compiler's optimizer can still inline the `print` function if it decides that is the fastest option.

---

## 4. When to Avoid Explicit Instantiation

While explicit instantiation is a fantastic tool for optimizing build times, implicit instantiation is actually the default and preferred approach for 95% of C++ code. You should avoid explicit instantiation (and just let the compiler do its thing) in the following scenarios:

### 1. You Have a Combinatorial Explosion of Types
The main draw of templates is that they write the code for you. If you write a generic container like `std::vector` or a math matrix class, your users might instantiate it with `int`, `double`, `std::string`, `Player`, `Enemy`, and a hundred other custom structs. If you try to explicitly instantiate them, you have to manually write a line of code for every single type your program will ever use.

{% highlight cpp %}
// This becomes a maintenance nightmare very quickly:
template class Vector<int>;
template class Vector<double>;
template class Vector<Player>;
// ... 500 lines later
{% endhighlight %}
> **Verdict:** If your template is meant to be used with a massive, unpredictable variety of types, stick to implicit instantiation.

### 2. You are Writing a Header-Only Library
Modern C++ developers love header-only libraries (like many Boost libraries, Eigen, or nlohmann/json). They are incredibly easy to share—you just `#include` the file and it works, with no need to configure CMake to build and link a separate `.cpp` file. If you use explicit instantiation in a `.cpp` file, your users are now forced to compile that source file and link the resulting binary. You have destroyed the plug-and-play nature of the header-only library.
> **Verdict:** If ease of distribution is your goal, put everything in the header and let the compiler instantiate implicitly.

### 3. Your Template Accepts Lambdas or Functors
If your template takes a callable object (like `std::sort` or `std::for_each`), explicit instantiation is practically impossible. Every single time you write a lambda in C++, the compiler generates a brand new, unique, invisible class type for it. Because you don't know the name of that type (only the compiler does), you literally cannot write the explicit instantiation syntax for it.
> **Verdict:** Templates relying on lambdas or heavily customized policy classes must be implicitly instantiated.

### 4. The Template is Tiny (Micro-Optimizations)
If your template is a three-line getter, a simple math wrapper, or a small type trait, the overhead for the compiler to generate it and the linker to deduplicate it is microscopic. Adding `.cpp` files, `extern template` declarations, and maintaining lists of instantiated types adds unnecessary boilerplate and cognitive load for the developers reading your code.
> **Verdict:** Don't add explicit instantiation boilerplate unless a profiler (like ClangBuildAnalyzer) proves that a specific template is bottlenecking your compile times.

---

## 5. The Golden Rule of Thumb

*   **Default to Implicit:** Put your templates completely in the header file. It is the easiest to maintain, gives the optimizer maximum visibility for inlining, and is standard C++ practice.
*   **Opt-in to Explicit:** Only reach for explicit instantiation when a specific, massive template (like a heavy `std::regex` or complex JSON parser) is being instantiated with the exact same type (like `std::string`) in dozens of files, and it is actively slowing down your daily compile times.