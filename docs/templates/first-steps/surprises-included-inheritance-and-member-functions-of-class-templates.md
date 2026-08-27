---
layout: default
title:  Two-Phase Lookup & Dependent Names
parent: First Steps
grand_parent: Templates
nav_order: 5
---


# Two-Phase Lookup & Dependent Names in C++
{: .fs-9 }

In C++, the issues caused by two-phase lookup and dependent names typically manifest in specific structural scenarios where the compiler cannot resolve a name until the template is instantiated. Let's break down exactly where these lookup issues occur and how to fix them.
{: .fs-5 .fw-300 }

<span class="label label-purple">Template Metaprogramming</span> <span class="label label-blue">Modern C++</span>

---

## Table of Contents
1. TOC
{:toc}

---

## 1. Dependent Base Classes (Inheritance)

**The Issue:** Calling member functions or accessing member variables defined in a base class that depends on a template parameter (`Base<T>`).

**Why it happens:** In C++ templates, name lookup happens in two phases. Phase 1 occurs when the template is defined (before instantiation). Non-dependent names are looked up in Phase 1, but the compiler completely ignores dependent base classes during this phase because it doesn't know what `Base<T>` might look like until `T` is known. 

**The Fix:** Tell the compiler that the name depends on the instance by using `this->`, `Base<T>::`, or introducing the name with a `using` declaration.

{% highlight cpp %}
template <typename T>
class Base {
protected:
    void doSomething() { /* ... */ }
    int count = 0;
};

template <typename T>
class Derived : public Base<T> {
public:
    void execute() {
        // ERROR: The compiler won't look in Base<T> during Phase 1.
        // doSomething(); 
        // count++;       

        // FIX: Make the names dependent so they are resolved in Phase 2.
        this->doSomething(); 
        this->count++;       
        
        // ALTERNATIVE FIX: Explicit scoping
        // Base<T>::doSomething();
    }
};
{% endhighlight %}

<details>
<summary>Deep Dive: Why doesn't the compiler just wait?</summary>
If the compiler waited until Phase 2 to parse everything, it would defeat the purpose of early syntax checking. By parsing non-dependent names in Phase 1, C++ guarantees that basic syntax errors in templates are caught immediately, even if the template is never instantiated. Furthermore, specialized versions of <code>Base&lt;T&gt;</code> might not even have <code>doSomething()</code>, which is why the compiler refuses to assume it exists in Phase 1.
</details>

## 2. Dependent Nested Types

**The Issue:** Accessing a type defined inside a template parameter or dependent scope (e.g., iterators, inner structs like `T::value_type`).

**Why it happens:** The compiler encounters `T::value_type`. Because `T` is unknown, the compiler doesn't know if `value_type` is a static member variable, a static function, or a type definition. By default, C++ assumes it is a **value**, not a type.

**The Fix:** Prefix the expression with the `typename` keyword to explicitly tell the compiler, "This identifier represents a type."

{% highlight cpp %}
#include <vector>
#include <iostream>

template <typename T>
void printFirstElement(const T& container) {
    // ERROR: Compiler assumes 'value_type' is a static member variable, 
    // so it tries to multiply it by 'firstElement' (pointer syntax).
    // T::value_type* firstElement; 

    // FIX: Use 'typename' to declare it as a type.
    typename T::value_type firstElement = *container.begin();
    
    std::cout << firstElement << '\n';
}
{% endhighlight %}

## 3. Dependent Template Member Functions

**The Issue:** Calling a member function that is itself a template on a dependent object (e.g., `obj.foo<int>()` where `obj` depends on `T`).

**Why it happens:** When parsing `obj.foo<int>()` in Phase 1, the compiler doesn't know if `foo` is a template. Therefore, it misinterprets the `<` symbol as a **"less-than"** arithmetic operator rather than the start of a template argument list.

**The Fix:** Use the `.template` (or `->template`) disambiguator to tell the compiler that the following name is a template.

{% highlight cpp %}
struct MyPrinter {
    template <typename U>
    void print(U value) {
        // ...
    }
};

template <typename T>
void processAndPrint(T obj) {
    // ERROR: Parses as: (obj.print) < (int) > (42) ... syntax error!
    // obj.print<int>(42); 

    // FIX: Use the .template disambiguator
    obj.template print<int>(42);
}

// Usage:
// processAndPrint(MyPrinter{});
{% endhighlight %}

## 4. Dependent Nested Class Templates

**The Issue:** Constructing or referencing a nested class template that depends on a template parameter (e.g., `T::InnerTemplate<int>`).

**Why it happens:** This is a combination of issues #2 and #3. The compiler defaults to assuming that nested names are values, and it defaults to assuming that `<` is the less-than operator.

**The Fix:** Use the `typename` keyword at the start, and the `template` keyword before the nested template name.

{% highlight cpp %}
struct Context {
    template <typename U>
    struct Builder {
        U build() { return U{}; }
    };
};

template <typename T>
void constructAndRun() {
    // ERROR: Compiler doesn't know 'Builder' is a type OR a template.
    // T::Builder<int> myObj; 

    // ERROR: Compiler knows it's a type, but parsing fails at '<'.
    // typename T::Builder<int> myObj; 

    // FIX: Use both typename and template
    typename T::template Builder<int> myObj;
    
    int result = myObj.build();
}
{% endhighlight %}

---

## Summary Checklist

Whenever you are writing a C++ template and you use an identifier tied to a template parameter (`T`), watch out for these syntax requirements to satisfy two-phase lookup:

*   <span class="label label-green">Inheritance</span> Access dependent base class members using `this->member`
*   <span class="label label-green">Types</span> Access dependent nested types using `typename T::type`
*   <span class="label label-green">Templates</span> Call dependent template methods using `object.template method<U>()`