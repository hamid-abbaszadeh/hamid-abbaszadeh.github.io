---
layout: default
title: "120 Advanced C++ Questions"
parent: "<span style='color: #4ade80;'>Coding Challenges</span>"
nav_order: 1
---

# 120 Advanced C++ Interview Questions

A comprehensive guide covering 120 senior-level C++ interview questions with code examples.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++11 / C++14 / C++17 / C++20 / C++23</span>
<span class="label label-purple">Coding Challenges</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Introduction


Each question below provides a simple English explanation and a concise example to help you quickly understand complex modern C++ concepts[cite: 1].

---

## Section 1: Template Metaprogramming & Advanced Templates (Q1–12)

### 1. Explain SFINAE and provide a practical use case
**Simple explanation:** SFINAE stands for "Substitution Failure Is Not An Error." When the compiler tries to fill in template types and one version doesn't make sense, it doesn't throw an error — it just quietly removes that version from the list of choices and tries another one[cite: 1]. Think of it like a restaurant menu: if a dish's ingredient is unavailable, that dish is simply removed from the menu, not the whole menu being thrown away[cite: 1].

**Example:**
{% highlight cpp %}
template<typename T>
typename std::enable_if<std::is_integral<T>::value, void>::type
print(T value) {
    std::cout << "Integer: " << value << "\n";
}
// This function only "exists" for integer types like int, long, etc.
// For a double, the compiler silently skips it instead of erroring.
{% endhighlight %}

### 2. What are forwarding references (universal references) and how do they differ from rvalue references?
**Simple explanation:** A forwarding reference is written as `T&&` where `T` is a template type[cite: 1]. It's special because it can accept BOTH temporary values (rvalues) and named variables (lvalues)[cite: 1]. A normal rvalue reference like `MyClass&&` can only accept temporaries[cite: 1].

**Example:**
{% highlight cpp %}
template<typename T>
void foo(T&& x) { }   // forwarding reference — accepts anything

void bar(std::string&& x) { } // rvalue reference — only accepts temporaries

int a = 5;
foo(a);        // OK, a is lvalue
foo(10);       // OK, 10 is rvalue
bar(std::move(a)); // OK
// bar(a);     // ERROR - a is lvalue, bar only takes rvalue
{% endhighlight %}

### 3. Implement a compile-time factorial using template metaprogramming
**Simple explanation:** You can make the compiler do math for you before the program even runs, using templates that call themselves (recursion), similar to a recursive function but happening at compile time[cite: 1].

**Example:**
{% highlight cpp %}
template<int N>
struct Factorial {
    static constexpr int value = N * Factorial<N - 1>::value;
};

template<>
struct Factorial<0> {
    static constexpr int value = 1;
};

// Factorial<5>::value is calculated by the COMPILER, equals 120
{% endhighlight %}

### 4. Explain the Curiously Recurring Template Pattern (CRTP). What are its advantages over virtual functions?
**Simple explanation:** CRTP is a trick where a class inherits from a template, and passes itself as the template argument[cite: 1]. It's like saying "Base, here I am, use my exact type." This lets the base class call functions of the derived class without needing virtual functions (no runtime lookup table), making it faster[cite: 1].

**Example:**
{% highlight cpp %}
template<typename Derived>
struct Base {
    void interface() { static_cast<Derived*>(this)->implementation(); }
};

struct Derived : Base<Derived> {
    void implementation() { std::cout << "Derived implementation\n"; }
};

Derived d;
d.interface();  // calls Derived::implementation() with no vtable lookup
{% endhighlight %}

### 5. What is template template parameter? Provide an example
**Simple explanation:** Normally a template parameter is a type (like `int` or `std::string`)[cite: 1]. A "template template parameter" means the parameter itself is a template — for example, you can pass in `std::vector` (without saying what it holds yet) and decide the inner type later[cite: 1].

**Example:**
{% highlight cpp %}
template<template<typename> class Container>
class MyClass {
    Container<int> data; // decide the inner type here
};

MyClass<std::vector> obj; // pass std::vector itself, not std::vector<int>
{% endhighlight %}

### 6. How does std::enable_if work internally?
**Simple explanation:** `enable_if` is like an "if door." If the condition you give it is `true`, it creates a `type` member so the code compiles[cite: 1]. If the condition is `false`, there's no `type` member, so trying to use it fails silently (thanks to SFINAE) and that function is removed from consideration[cite: 1].

**Example:**
{% highlight cpp %}
template<bool Condition, typename T = void>
struct MyEnableIf {}; // empty by default — no "type" member

template<typename T>
struct MyEnableIf<true, T> { using type = T; }; // only defined when Condition is true
{% endhighlight %}

### 7. Explain variadic templates and fold expressions (C++17)
**Simple explanation:** Variadic templates let a function or class accept ANY number of arguments of different types, using `Args...`[cite: 1]. Fold expressions (from C++17) let you combine all of them using an operator (like `+`) in one short line instead of writing recursive code[cite: 1].

**Example:**
{% highlight cpp %}
template<typename... Args>
auto sum(Args... args) {
    return (args + ...); // fold expression: adds all arguments together
}

sum(1, 2, 3, 4); // returns 10
{% endhighlight %}

### 8. What are the differences between partial and full template specialization?
**Simple explanation:** Full specialization means you write a completely custom version of a template for one exact type[cite: 1]. Partial specialization means you customize it for a *pattern* of types (like all pointers, or a template with two parameters where one is fixed) while keeping some parts generic[cite: 1]. Partial specialization only works for class templates, not standalone functions[cite: 1].

**Example:**
{% highlight cpp %}
template<typename T> struct Box { }; // generic

template<> struct Box<int> { };      // full specialization (only for int)

template<typename T> struct Box<T*> { }; // partial specialization (for any pointer type)
{% endhighlight %}

### 9. How do you detect if a type has a specific member function at compile-time?
**Simple explanation:** You can write a small "detector" using SFINAE: try calling the function inside `decltype`; if it compiles, the type has it; if not, the compiler silently picks the fallback version[cite: 1].

**Example:**
{% highlight cpp %}
template<typename T>
class HasFoo {
    template<typename U>
    static auto test(U*) -> decltype(std::declval<U>().foo(), std::true_type{});
    template<typename>
    static std::false_type test(...);
public:
    static constexpr bool value = decltype(test<T>(nullptr))::value;
};
// HasFoo<MyClass>::value is true if MyClass has a foo() method
{% endhighlight %}

### 10. Explain dependent names and typename keyword usage
**Simple explanation:** A "dependent name" is something whose meaning depends on a template parameter — the compiler can't be 100% sure if it's a type or a value until the template is actually used[cite: 1]. You must add `typename` to tell the compiler "trust me, this is a type."[cite: 1]

**Example:**
{% highlight cpp %}
template<typename T>
void func() {
    typename T::value_type x; // tells compiler value_type is a TYPE, not a variable
}
{% endhighlight %}

### 11. What is Expression Templates and where is it useful?
**Simple explanation:** Instead of calculating something immediately, expression templates build a tiny "recipe" (expression tree) at compile time, and only actually compute the result once, avoiding wasted temporary objects[cite: 1]. It's commonly used in math/vector libraries like Eigen for performance[cite: 1].

**Example:**
{% highlight cpp %}
// Without expression templates: vector3 = vector1 + vector2 + vector3
// creates 2 temporary vectors.
// With expression templates, the whole expression compiles into ONE loop,
// with no temporaries created — like a chef combining all ingredients
// in one pass instead of making a new bowl for every step.
{% endhighlight %}

### 12. Implement is_base_of type trait using template metaprogramming
**Simple explanation:** You can check "is class A a parent of class B?" at compile time by trying to convert a `Derived*` pointer to a `Base*` pointer and seeing if that conversion is legal[cite: 1].

**Example:**
{% highlight cpp %}
template<typename Derived, typename Base>
class IsBaseOf {
    static std::true_type test(Base*);
    static std::false_type test(...);
public:
    static constexpr bool value =
        std::is_same_v<decltype(test(static_cast<Derived*>(nullptr))), std::true_type>;
};
{% endhighlight %}

---

## Section 2: Move Semantics & Perfect Forwarding (Q13–28)

### 13. What is the difference between lvalue, rvalue, prvalue, xvalue, and glvalue?
**Simple explanation:** These are labels for different "kinds" of expressions[cite: 1].
- **lvalue**: has a name/address, like a variable (`x`)[cite: 1].
- **rvalue**: a temporary value with no permanent home (`5`, `x + 1`)[cite: 1].
- **prvalue**: a "pure" rvalue — a plain temporary (`5`)[cite: 1].
- **xvalue**: an "expiring" value — something about to be destroyed/reused (`std::move(x)`)[cite: 1].
- **glvalue**: umbrella term meaning "lvalue or xvalue"[cite: 1].

**Example:**
{% highlight cpp %}
int x = 5;      // x is an lvalue
int y = x + 1;  // (x + 1) is a prvalue
int z = std::move(x); // std::move(x) is an xvalue
{% endhighlight %}

### 14. Explain reference collapsing rules in detail
**Simple explanation:** When references-to-references appear (which happens inside templates), C++ "collapses" them into a single reference using simple rules: an `&` anywhere wins over `&&` unless both sides are `&&`[cite: 1].

**Example:**
{% highlight text %}
T&  &   -> T&
T&  &&  -> T&
T&& &   -> T&
T&& &&  -> T&&   (only case that stays an rvalue reference)
{% endhighlight %}

### 15. What's the difference between std::move and std::forward?
**Simple explanation:** `std::move` always turns something into an rvalue (marks it as "movable"), no matter what it originally was[cite: 1]. `std::forward` is smarter — it only turns it into an rvalue if the original argument actually WAS an rvalue, keeping lvalues as lvalues[cite: 1]. `forward` is used to pass arguments along exactly as they were received[cite: 1].

**Example:**
{% highlight cpp %}
template<typename T>
void wrapper(T&& arg) {
    target(std::forward<T>(arg)); // keeps original "lvalue-ness" or "rvalue-ness"
}
std::string s = "hi";
std::string s2 = std::move(s); // s is now empty/moved-from
{% endhighlight %}

### 16. Explain the Rule of Zero, Rule of Three, and Rule of Five
**Simple explanation:**
- **Rule of Zero:** Best case — don't write any special functions (destructor, copy, move) yourself; let smart pointers/containers manage resources for you[cite: 1].
- **Rule of Three:** If you write ANY of destructor, copy constructor, or copy assignment, you probably need all three[cite: 1].
- **Rule of Five:** Same as Rule of Three but also add move constructor and move assignment[cite: 1].

**Example:**
{% highlight cpp %}
class Good {
    std::vector<int> data; // Rule of Zero — no need for destructor etc.
};

class Risky {
    int* ptr;
public:
    ~Risky() { delete ptr; }               // if you write this...
    Risky(const Risky&);                  // ...you likely need this...
    Risky& operator=(const Risky&);       // ...and this too (Rule of Three)
};
{% endhighlight %}

### 17. When would a move constructor NOT be implicitly generated?
**Simple explanation:** The compiler won't auto-generate a move constructor if you've already written your own copy constructor, copy assignment operator, move assignment operator, or destructor[cite: 1]. Writing any of these tells the compiler "I'm handling special behavior myself," so it stays out of the way[cite: 1].

**Example:**
{% highlight cpp %}
class MyClass {
public:
    ~MyClass() {} // you defined a destructor
    // Move constructor is now NOT auto-generated!
};
{% endhighlight %}

### 18. What are the performance implications of returning by value with move semantics?
**Simple explanation:** In modern C++, returning objects by value is efficient[cite: 1]. The compiler often eliminates the copy entirely (RVO), and if it can't, it moves the object instead of copying it (which is fast)[cite: 1]. So don't be afraid to `return` by value[cite: 1].

**Example:**
{% highlight cpp %}
std::vector<int> createVector() {
    std::vector<int> v = {1, 2, 3};
    return v; // no expensive copy — RVO or move happens automatically
}
{% endhighlight %}

### 19. Explain mandatory copy elision (C++17) and how it differs from NRVO
**Simple explanation:** Since C++17, when you return a brand-new temporary object directly, the compiler is REQUIRED to build it directly in place (no copy/move constructor needed at all)[cite: 1]. NRVO (returning a named local variable) is still just an optional optimization compilers are allowed to skip[cite: 1].

**Example:**
{% highlight cpp %}
Widget makeWidget() {
    return Widget{}; // guaranteed elision (C++17) — no move/copy call needed
}
Widget makeWidget2() {
    Widget w;
    return w; // NRVO — optional, compiler usually does it but not guaranteed
}
{% endhighlight %}

### 20. What happens when you call std::move on a const object?
**Simple explanation:** `std::move` on a `const` object doesn't actually let you move it — because move operations need a non-const rvalue reference, but a const object can only bind to a const reference[cite: 1]. So it silently falls back to copying instead[cite: 1]. This is a sneaky bug that's easy to miss[cite: 1].

**Example:**
{% highlight cpp %}
const std::string s = "hello";
std::string s2 = std::move(s); // this actually COPIES, not moves! (s is const)
{% endhighlight %}

### 21. How do you implement move semantics correctly for a class with raw pointers?
**Simple explanation:** Steal the pointer from the other object, then set the other object's pointer to `nullptr` so its destructor doesn't accidentally delete memory you now own[cite: 1].

**Example:**
{% highlight cpp %}
class Buffer {
    char* data; size_t size;
public:
    Buffer(Buffer&& other) noexcept : data(other.data), size(other.size) {
        other.data = nullptr; // prevent double-delete
        other.size = 0;
    }
};
{% endhighlight %}

### 22. Why should move constructors and move assignment operators be noexcept?
**Simple explanation:** Containers like `std::vector` need to guarantee that if something goes wrong while resizing, they can safely undo it[cite: 1]. They can only trust "moving" objects to be safe if the move is marked `noexcept`[cite: 1]. If it's not, `vector` plays it safe and copies instead — which is slower[cite: 1].

**Example:**
{% highlight cpp %}
class MyClass {
public:
    MyClass(MyClass&&) noexcept { } // vector will use fast move
    // without noexcept, vector::push_back falls back to copying during reallocation
};
{% endhighlight %}

### 23. Explain perfect forwarding failure cases
**Simple explanation:** Perfect forwarding (passing arguments through unchanged) breaks in a few tricky situations: passing `{1,2,3}` directly (braces confuse type deduction), passing overloaded function names, bitfields, `0`/`NULL` instead of `nullptr`, and static const members that are only declared, not defined[cite: 1].

**Example:**
{% highlight cpp %}
template<typename T>
void wrapper(T&& arg) { target(std::forward<T>(arg)); }

// wrapper({1, 2, 3}); // FAILS — compiler can't deduce T from a brace list
{% endhighlight %}

### 24. What is the "Has-A-Name" rule for rvalues?
**Simple explanation:** Once an rvalue reference is given a name (like a function parameter `T&& x`), it behaves like an lvalue inside the function body, because it now "has a name."[cite: 1] You must explicitly use `std::move` again to treat it as an rvalue[cite: 1].

**Example:**
{% highlight cpp %}
void func(std::string&& s) {
    // s here IS an lvalue (it has a name), even though its TYPE is rvalue reference
    std::string s2 = s;            // this COPIES
    std::string s3 = std::move(s); // this MOVES
}
{% endhighlight %}

### 25. What is the purpose of std::move_if_noexcept?
**Simple explanation:** It moves an object only if that move is guaranteed not to throw an exception; otherwise, it copies instead[cite: 1]. This protects containers like `std::vector` from ending up in a broken, half-modified state if an exception happens mid-move[cite: 1].

**Example:**
{% highlight cpp %}
// used internally by std::vector when growing its storage,
// to decide whether to move or copy each element safely
{% endhighlight %}

### 26. Explain the moved-from state and what guarantees it provides
**Simple explanation:** After you move an object, the original is left in a "valid but unspecified" state — meaning you can still safely destroy it or assign a new value to it, but you shouldn't assume it still has its old contents[cite: 1].

**Example:**
{% highlight cpp %}
std::vector<int> a = {1, 2, 3};
std::vector<int> b = std::move(a);
// a is now valid but empty/unspecified — safe to reuse, e.g. a = {4,5};
{% endhighlight %}

### 27. How does Return Value Optimization (RVO) interact with move semantics?
**Simple explanation:** RVO builds the returned object directly where it will be used, skipping copy AND move entirely — which is even faster than moving[cite: 1]. Because of this, you should NOT wrap a return value in `std::move()`, as doing so can actually prevent RVO from happening[cite: 1].

**Example:**
{% highlight cpp %}
Widget make() {
    Widget w;
    return w;            // GOOD — allows RVO/NRVO
    // return std::move(w); // BAD — can block the optimization
}
{% endhighlight %}

### 28. What is the universal reference (forwarding reference) and how does template argument deduction work with it?
**Simple explanation:** `T&&` in a template is special: when you pass an lvalue, `T` becomes `SomeType&`; when you pass an rvalue, `T` becomes just `SomeType`[cite: 1]. Combined with reference collapsing, this lets one function correctly accept and forward both kinds of values[cite: 1].

**Example:**
{% highlight cpp %}
template<typename T>
void f(T&& x) { }

int a = 1;
f(a);   // T deduced as int&  -> x is int&
f(10);  // T deduced as int   -> x is int&&
{% endhighlight %}

---

## Section 3: Memory Model & Atomics (Q29–36)

### 29. Explain the six memory ordering models in C++11
**Simple explanation:** These control how strictly the CPU/compiler must keep operations on atomic variables in order across threads[cite: 1]. From loosest to strictest:
- `relaxed`: no ordering guarantee, just atomic (safe from data races only)[cite: 1].
- `consume`: orders things that depend on the loaded value (rarely used)[cite: 1].
- `acquire`: nothing after this can be reordered before it (for loads)[cite: 1].
- `release`: nothing before this can be reordered after it (for stores)[cite: 1].
- `acq_rel`: both acquire and release together[cite: 1].
- `seq_cst`: strictest — everything happens in one single global order (default, safest, a bit slower)[cite: 1].

**Example:**
{% highlight cpp %}
std::atomic<int> counter{0};
counter.fetch_add(1, std::memory_order_relaxed); // just needs to be atomic, order doesn't matter
{% endhighlight %}

### 30. What is the happens-before relationship?
**Simple explanation:** It's a guarantee that if operation A "happens-before" operation B, then any changes A made are visible to B[cite: 1]. Think of it like passing a note: once you hand it over (happens-before), the other person is guaranteed to be able to read it[cite: 1].

**Example:**
{% highlight cpp %}
// Thread 1: data = 42; flag.store(true, memory_order_release);
// Thread 2: while(!flag.load(memory_order_acquire)); use(data); // sees data=42 safely
{% endhighlight %}

### 31. Explain acquire-release semantics
**Simple explanation:** A "release" store on one thread and a matching "acquire" load on another thread create a safe handoff point — everything written before the release is guaranteed visible after the matching acquire[cite: 1]. It's like locking a diary (release) and someone else unlocking it (acquire) to read everything you wrote[cite: 1].

**Example:**
{% highlight cpp %}
std::atomic<bool> ready{false};
int data = 0;
// Thread A: data = 5; ready.store(true, std::memory_order_release);
// Thread B: if (ready.load(std::memory_order_acquire)) { /* data is guaranteed 5 here */ }
{% endhighlight %}

### 32. What's the difference between std::atomic<T>::is_lock_free() and std::atomic<T>::is_always_lock_free?
**Simple explanation:** `is_lock_free()` checks AT RUNTIME whether this specific atomic object uses lock-free hardware instructions[cite: 1]. `is_always_lock_free` is a compile-time constant telling you if that type is ALWAYS guaranteed lock-free on this platform (known ahead of time, no runtime check needed)[cite: 1].

**Example:**
{% highlight cpp %}
std::atomic<int> x;
bool runtimeCheck = x.is_lock_free();          // checked at runtime
constexpr bool compileTimeCheck = std::atomic<int>::is_always_lock_free; // known at compile time
{% endhighlight %}

### 33. When would you use memory_order_relaxed?
**Simple explanation:** Use it when you only care that an operation is atomic (won't be corrupted by simultaneous access), but you don't care about the ORDER relative to other memory operations — like a simple counter where only the final total matters[cite: 1].

**Example:**
{% highlight cpp %}
std::atomic<long> hitCounter{0};
hitCounter.fetch_add(1, std::memory_order_relaxed); // just counting, order doesn't matter
{% endhighlight %}

### 34. Explain the ABA problem in lock-free programming
**Simple explanation:** Imagine you check a value, see it's "A", and think nothing changed — but actually it changed to "B" and then back to "A" while you weren't looking[cite: 1]. A simple compare-and-swap can't tell the difference, which can cause hidden bugs[cite: 1]. Fixes include using version-tagged pointers or hazard pointers[cite: 1].

**Example:**
{% highlight text %}
Thread 1 reads value = A
Thread 2 changes A -> B -> A
Thread 1's compare-and-swap sees "A" and thinks nothing happened — but something did!
{% endhighlight %}

### 35. What are the differences between compare_exchange_weak and compare_exchange_strong?
**Simple explanation:** `weak` might fail even when the values actually match (a "false alarm"), but it's faster on some CPUs — good when you're already looping and retrying anyway[cite: 1]. `strong` never has false failures, but can be a little slower — use it when a retry loop isn't already happening[cite: 1].

**Example:**
{% highlight cpp %}
int expected = 10;
while (!atomicVar.compare_exchange_weak(expected, 20)) {
    // loop retries on failure anyway, so "weak" is fine here
}
{% endhighlight %}

### 36. Explain memory fences (std::atomic_thread_fence)
**Simple explanation:** A fence is like a "checkpoint" you place in code that enforces ordering rules WITHOUT needing an atomic variable at that exact spot[cite: 1]. It can make regular (non-atomic) reads/writes near it respect acquire/release ordering too[cite: 1].

**Example:**
{% highlight cpp %}
data = 42;
std::atomic_thread_fence(std::memory_order_release); // ensures 'data' write is visible
flag.store(true, std::memory_order_relaxed);
{% endhighlight %}

---

## Section 4: Modern C++ Features (Q37–44)

### 37. Explain structured bindings (C++17) and their limitations
**Simple explanation:** Structured bindings let you "unpack" a pair, tuple, struct, or array into separate named variables in one line, instead of accessing `.first`/`.second` or `std::get<0>`[cite: 1]. Limitation: you can't specify types individually or skip elements easily[cite: 1].

**Example:**
{% highlight cpp %}
std::pair<int, std::string> p = {1, "hello"};
auto [id, name] = p; // id = 1, name = "hello"
{% endhighlight %}

### 38. What is std::optional and when should you use it instead of pointers?
**Simple explanation:** `std::optional<T>` represents "a value that might or might not exist" — like a box that's either full or empty[cite: 1]. It avoids null pointer confusion and doesn't need heap allocation, making intent clearer than using a raw pointer for "maybe there's a value."[cite: 1]

**Example:**
{% highlight cpp %}
std::optional<int> findAge(std::string name) {
    if (name == "Bob") return 30;
    return std::nullopt; // no value
}
auto age = findAge("Alice");
if (age) std::cout << *age;
else std::cout << "not found";
{% endhighlight %}

### 39. Explain if constexpr (C++17) and how it differs from regular if
**Simple explanation:** `if constexpr` decides which branch to use AT COMPILE TIME, and completely throws away the code in the unused branch (it doesn't even need to be valid code!)[cite: 1]. A regular `if` keeps both branches and decides at runtime, so both branches must compile correctly[cite: 1].

**Example:**
{% highlight cpp %}
template<typename T>
void print(T val) {
    if constexpr (std::is_pointer_v<T>)
        std::cout << *val; // only compiled if T is a pointer
    else
        std::cout << val;
}
{% endhighlight %}

### 40. What is std::variant and how does it compare to unions?
**Simple explanation:** `std::variant` is a "type-safe union" — a box that can hold ONE of several possible types, but unlike a plain C-style union, it always knows which type is currently stored, and it correctly constructs/destroys objects for you[cite: 1].

**Example:**
{% highlight cpp %}
std::variant<int, std::string> v = "hello";
std::visit([](auto&& val){ std::cout << val; }, v); // prints "hello"
v = 5; // now holds an int
{% endhighlight %}

### 41. Explain std::string_view and its pitfalls
**Simple explanation:** `std::string_view` is a lightweight "window" into a string's characters, without owning or copying them[cite: 1]. It's fast for read-only access, but dangerous if the original string is destroyed while you still hold the view (dangling reference)[cite: 1].

**Example:**
{% highlight cpp %}
std::string_view getView() {
    std::string temp = "hi";
    return temp; // DANGEROUS - temp is destroyed, view now dangles!
}
{% endhighlight %}

### 42. What are designated initializers (C++20)?
**Simple explanation:** They let you set specific struct fields by name when creating an object, making the code more readable and less likely to break if the struct's field order changes[cite: 1].

**Example:**
{% highlight cpp %}
struct Point { int x; int y; };
Point p{.x = 10, .y = 20}; // clearly labeled, in declaration order
{% endhighlight %}

### 43. Explain concepts (C++20) and their advantages over SFINAE
**Simple explanation:** Concepts let you write template requirements in plain, readable language (like "T must be an integer type") instead of complicated SFINAE tricks[cite: 1]. They also give much clearer compiler error messages when misused[cite: 1].

**Example:**
{% highlight cpp %}
template<std::integral T>
T add(T a, T b) { return a + b; }
// add(1, 2);      OK
// add(1.5, 2.5);  Clear error: double doesn't satisfy std::integral
{% endhighlight %}

### 44. What is std::span (C++20) and when should you use it?
**Simple explanation:** `std::span` is a lightweight, non-owning "view" over a contiguous chunk of memory (like an array or vector), with size info attached[cite: 1]. Use it as a function parameter instead of passing a raw pointer + length, or forcing a `std::vector` copy[cite: 1].

**Example:**
{% highlight cpp %}
void printAll(std::span<int> data) {
    for (int x : data) std::cout << x << " ";
}
int arr[] = {1,2,3};
std::vector<int> v = {4,5,6};
printAll(arr); // works
printAll(v);   // also works, no copy
{% endhighlight %}

---

## Section 5: Concurrency & Multithreading (Q45–50)

### 45. Explain the differences between std::mutex, std::recursive_mutex, and std::shared_mutex
**Simple explanation:**
- `std::mutex`: a simple lock — only one thread can hold it at a time, and if the same thread tries to lock it again it deadlocks[cite: 1].
- `std::recursive_mutex`: the SAME thread is allowed to lock it multiple times (useful for recursive functions)[cite: 1].
- `std::shared_mutex`: allows MANY readers at once, OR one exclusive writer (like a library — many people can read a book, but only one can rewrite it)[cite: 1].

**Example:**
{% highlight cpp %}
std::shared_mutex rwLock;
void read() { std::shared_lock lock(rwLock); /* many readers OK */ }
void write() { std::unique_lock lock(rwLock); /* exclusive writer */ }
{% endhighlight %}

### 46. What is std::condition_variable and how does it relate to spurious wakeups?
**Simple explanation:** A `condition_variable` lets a thread sleep until another thread signals it[cite: 1]. A "spurious wakeup" is when the thread wakes up for no real reason (not because it was notified)[cite: 1]. That's why you should always check the actual condition in a loop, not just wake up and assume it's true[cite: 1].

**Example:**
{% highlight cpp %}
std::condition_variable cv;
std::mutex m;
bool ready = false;
// Correct: wait with predicate handles spurious wakeups automatically
std::unique_lock<std::mutex> lock(m);
cv.wait(lock, []{ return ready; });
{% endhighlight %}

### 47. Explain deadlock and how to prevent it
**Simple explanation:** Deadlock happens when two threads each hold a lock the other one needs, so both wait forever — like two people each holding one chopstick, waiting for the other's[cite: 1]. Prevention: always lock resources in the same order, or use `std::lock` to grab multiple mutexes safely at once[cite: 1].

**Example:**
{% highlight cpp %}
std::mutex m1, m2;
// Safe way to lock two mutexes without deadlock risk:
std::lock(m1, m2);
std::lock_guard<std::mutex> lk1(m1, std::adopt_lock);
std::lock_guard<std::mutex> lk2(m2, std::adopt_lock);
{% endhighlight %}

### 48. What is std::future and std::promise?
**Simple explanation:** `std::promise` is where one thread "promises" to deliver a result later[cite: 1]. `std::future` is how another thread waits for and picks up that result[cite: 1]. It's like ordering food (promise) and getting a receipt (future) to collect it when it's ready[cite: 1].

**Example:**
{% highlight cpp %}
std::promise<int> p;
std::future<int> f = p.get_future();
std::thread t([&p]{ p.set_value(42); });
std::cout << f.get(); // waits and prints 42
t.join();
{% endhighlight %}

### 49. Explain memory barriers and their role in thread synchronization
**Simple explanation:** A memory barrier stops the CPU/compiler from reordering instructions across it, ensuring that writes made by one thread are actually visible to another thread in the expected order[cite: 1]. It's essential for writing correct lock-free code[cite: 1].

**Example:**
{% highlight cpp %}
// see Q36 example — std::atomic_thread_fence is a manual memory barrier
{% endhighlight %}

### 50. What is thread_local storage and when should you use it?
**Simple explanation:** A `thread_local` variable gives EACH thread its own private copy, so threads don't interfere with each other without needing locks[cite: 1]. Great for things like random number generators or per-thread caches[cite: 1].

**Example:**
{% highlight cpp %}
thread_local int counter = 0;
void increment() { counter++; } // each thread has its own independent counter
{% endhighlight %}

---

## Section 6: RAII & Smart Pointers (Q51–58)

### 51. Explain RAII and why it's considered a fundamental C++ idiom
**Simple explanation:** RAII means "Resource Acquisition Is Initialization" — you grab a resource (memory, file, lock) in a constructor and release it in the destructor[cite: 1]. Since destructors run automatically (even during exceptions), resources are never leaked[cite: 1]. It's like a hotel key card that automatically deactivates when you check out[cite: 1].

**Example:**
{% highlight cpp %}
{
    std::lock_guard<std::mutex> lock(myMutex); // acquires lock
    // ... do work ...
} // lock automatically released here, even if an exception happens
{% endhighlight %}

### 52. When would you use std::unique_ptr vs std::shared_ptr vs raw pointers?
**Simple explanation:**
- `unique_ptr`: ONE clear owner, super lightweight. Use by default[cite: 1].
- `shared_ptr`: MULTIPLE owners share responsibility, counted with a reference count[cite: 1].
- Raw pointer: just "looking" at something you don't own — no responsibility to delete it[cite: 1].

**Example:**
{% highlight cpp %}
std::unique_ptr<Widget> w1 = std::make_unique<Widget>(); // sole owner
std::shared_ptr<Widget> w2 = std::make_shared<Widget>();  // shared owners
Widget* observer = w2.get(); // just observing, not owning
{% endhighlight %}

### 53. What is std::make_unique and why is it preferred over new?
**Simple explanation:** `make_unique` creates and wraps an object in one safe step[cite: 1]. Using `new` directly can leak memory if an exception happens between allocating the object and wrapping it in a smart pointer (due to unpredictable evaluation order of function arguments)[cite: 1].

**Example:**
{% highlight cpp %}
auto w = std::make_unique<Widget>(); // safe, one-liner
// std::unique_ptr<Widget> w2(new Widget()); // works but riskier in complex expressions
{% endhighlight %}

### 54. Explain the control block in std::shared_ptr and its performance implications
**Simple explanation:** The "control block" is a hidden helper object that tracks how many `shared_ptr`s and `weak_ptr`s point to the same data[cite: 1]. It costs a bit of performance (extra memory, atomic counting)[cite: 1]. `make_shared` is more efficient because it allocates the object and its control block together in a single memory chunk[cite: 1].

**Example:**
{% highlight cpp %}
auto sp = std::make_shared<Widget>(); // ONE allocation (object + control block together)
std::shared_ptr<Widget> sp2(new Widget()); // TWO separate allocations, slightly slower
{% endhighlight %}

### 55. What's the difference between std::shared_ptr and std::weak_ptr?
**Simple explanation:** `shared_ptr` owns the object and keeps it alive[cite: 1]. `weak_ptr` just "watches" the object without owning it or keeping it alive — useful to avoid circular ownership[cite: 1]. You must call `.lock()` on a `weak_ptr` to safely use the object (it returns empty if the object is already gone)[cite: 1].

**Example:**
{% highlight cpp %}
std::shared_ptr<Widget> sp = std::make_shared<Widget>();
std::weak_ptr<Widget> wp = sp; // doesn't increase ownership count
if (auto locked = wp.lock()) { /* object still exists, safe to use */ }
{% endhighlight %}

### 56. How do custom deleters work with smart pointers?
**Simple explanation:** Sometimes cleanup isn't just `delete` — like closing a file handle[cite: 1]. Smart pointers let you supply a custom function to call instead of `delete` when the pointer goes out of scope[cite: 1].

**Example:**
{% highlight cpp %}
std::unique_ptr<FILE, decltype(&fclose)> file(fopen("data.txt", "r"), &fclose);
// automatically calls fclose(file) when it goes out of scope
{% endhighlight %}

### 57. Explain the std::enable_shared_from_this pattern
**Simple explanation:** If an object wants to create a `shared_ptr` to ITSELF (say, to pass "me" into a callback), it needs to inherit from `std::enable_shared_from_this`[cite: 1]. This makes sure the new `shared_ptr` correctly shares the SAME reference count as the existing ones, instead of creating a separate, broken one[cite: 1].

**Example:**
{% highlight cpp %}
class MyClass : public std::enable_shared_from_this<MyClass> {
public:
    std::shared_ptr<MyClass> getSelf() { return shared_from_this(); }
};
{% endhighlight %}

### 58. What are the dangers of circular references with std::shared_ptr and how do you break them?
**Simple explanation:** If object A holds a `shared_ptr` to B, and B holds a `shared_ptr` back to A, their reference counts never reach zero — they leak memory forever (they keep each other "alive" even when nobody else needs them)[cite: 1]. Fix: make one direction a `weak_ptr` instead[cite: 1].

**Example:**
{% highlight cpp %}
struct Child; 
struct Parent { std::shared_ptr<Child> child; };
struct Child { std::weak_ptr<Parent> parent; }; // weak_ptr breaks the cycle
{% endhighlight %}

---

## Section 7: Obscure Language Features & Edge Cases (Q59–66)

### 59. Explain the Most Vexing Parse problem
**Simple explanation:** `Widget w(Foo());` LOOKS like it creates a `Widget` using a temporary `Foo`, but C++ actually parses it as a FUNCTION DECLARATION (a function named `w` that returns a `Widget` and takes a `Foo`-returning-function parameter)[cite: 1]. Fix it using `{}` braces instead[cite: 1].

**Example:**
{% highlight cpp %}
Widget w(Foo()); // Most Vexing Parse — this is a function declaration, not an object!
Widget w2{Foo{}}; // correct — creates an object using uniform initialization
{% endhighlight %}

### 60. What is the difference between struct and class beyond default access?
**Simple explanation:** The only real difference is that `struct` members are `public` by default, and `class` members are `private` by default (same for inheritance)[cite: 1]. Everything else works identically[cite: 1]. Convention: use `struct` for simple data bags, `class` for objects with behavior/invariants[cite: 1].

**Example:**
{% highlight cpp %}
struct S { int x; };   // x is public by default
class C { int x; };    // x is private by default
{% endhighlight %}

### 61. Explain the empty base optimization (EBO)
**Simple explanation:** If a base class has no data members (it's "empty"), the compiler can make it take up ZERO extra bytes in the derived object, instead of wasting at least 1 byte like a normal empty object would[cite: 1]. This is used in things like stateless allocators[cite: 1].

**Example:**
{% highlight cpp %}
struct Empty {};
struct Derived : Empty { int x; };
// sizeof(Derived) == sizeof(int) thanks to EBO, not int + 1 extra byte
{% endhighlight %}

### 62. What happens when you throw an exception from a destructor?
**Simple explanation:** If a destructor throws WHILE another exception is already being handled (stack unwinding), the program calls `std::terminate()` and crashes immediately[cite: 1]. Since C++11, destructors are `noexcept` by default — so you should catch and handle any errors inside the destructor itself[cite: 1].

**Example:**
{% highlight cpp %}
~MyClass() {
    try { riskyCleanup(); } catch(...) { /* handle here, never let it escape */ }
}
{% endhighlight %}

### 63. Explain name lookup and why using is sometimes needed in templates
**Simple explanation:** In templates, the compiler looks up names in two phases[cite: 1]. Names that depend on the template parameter (like base class members in CRTP) aren't automatically visible, so you need `this->` or a `using Base::member;` statement to tell the compiler where to find them[cite: 1].

**Example:**
{% highlight cpp %}
template<typename T>
struct Derived : Base<T> {
    using Base<T>::memberFunc; // needed to make Base's member visible here
};
{% endhighlight %}

### 64. What is the "copy-and-swap" idiom?
**Simple explanation:** A clean way to write assignment operators: make a full copy of the incoming object, then just SWAP its contents with `*this`[cite: 1]. The old data gets destroyed automatically by the temporary's destructor[cite: 1]. This gives strong exception safety and naturally handles self-assignment[cite: 1].

**Example:**
{% highlight cpp %}
MyClass& operator=(MyClass other) { // note: parameter taken by value (a copy)
    swap(*this, other);
    return *this;
} // 'other' (holding old data) is destroyed here automatically
{% endhighlight %}

### 65. Explain the static initialization order fiasco
**Simple explanation:** Global/static variables in DIFFERENT files might be initialized in any order the compiler chooses[cite: 1]. If one global's constructor uses another global from a different file, it might run before that other global is ready — undefined behavior[cite: 1]. Fix: use a function-local static (Meyers Singleton) which only initializes on first use[cite: 1].

**Example:**
{% highlight cpp %}
// BAD: two globals in different files, order unknown
// GOOD:
MyClass& getInstance() {
    static MyClass instance; // created safely on first call, in any file
    return instance;
}
{% endhighlight %}

### 66. What is Argument-Dependent Lookup (ADL) / Koenig Lookup?
**Simple explanation:** When you call a function with arguments from a certain namespace, the compiler also automatically looks in THAT namespace for a matching function, even without you writing the namespace explicitly[cite: 1]. This is why `swap(a, b)` can find `std::swap` (or a custom `swap`) without you typing `std::`[cite: 1].

**Example:**
{% highlight cpp %}
namespace MyNS { struct Point {}; void print(Point) { } }
MyNS::Point p;
print(p); // found via ADL, even without MyNS:: prefix
{% endhighlight %}

---

## Section 8: Copy Constructor & Special Members (Q67–72)

### 67. What is the copy-elision guarantee in C++17 and how does it affect copy constructors?
**Simple explanation:** Since C++17, creating a temporary and using it directly (`T obj = T();`) is GUARANTEED to skip the copy/move constructor entirely — the object is built directly where it's needed, even if the copy constructor is deleted or private[cite: 1]. Named objects returned from functions (NRVO) are still just an optional optimization[cite: 1].

**Example:**
{% highlight cpp %}
struct NoCopy { NoCopy() {} NoCopy(const NoCopy&) = delete; };
NoCopy make() { return NoCopy(); } // compiles fine in C++17 - guaranteed elision
{% endhighlight %}

### 68. Explain the difference between shallow copy and deep copy. When does the default copy constructor fail?
**Simple explanation:** A shallow copy just copies the pointer VALUE (both objects now point to the same memory)[cite: 1]. A deep copy actually duplicates the data being pointed to[cite: 1]. The compiler's auto-generated copy constructor does a shallow copy — which breaks (double-free, dangling pointers) when your class manages raw resources like `new`'d memory[cite: 1].

**Example:**
{% highlight cpp %}
class Bad {
    int* data;
public:
    Bad(int val) { data = new int(val); }
    // no custom copy constructor -> shallow copy -> BOTH objects delete the SAME pointer -> crash
};
{% endhighlight %}

### 69. What is the copy-on-write (COW) optimization and why is it problematic in multithreaded code?
**Simple explanation:** COW delays copying data until it's actually modified — multiple objects share the same data until one of them changes it[cite: 1]. The problem: tracking "how many objects share this" needs thread-safe counting, which adds overhead and can cause bugs — that's why C++11 banned this technique for `std::string`[cite: 1].

**Example:**
{% highlight cpp %}
// Old COW std::string implementations shared a buffer between copies
// until write() was called — this broke thread safety guarantees.
{% endhighlight %}

### 70. How does the copy constructor interact with inheritance?
**Simple explanation:** A derived class's copy constructor must EXPLICITLY call the base class's copy constructor, or else the base part gets default-constructed instead of copied — a common, sneaky bug[cite: 1].

**Example:**
{% highlight cpp %}
class Derived : public Base {
    int extra;
public:
    Derived(const Derived& other) : Base(other), extra(other.extra) {} // must call Base(other)!
};
{% endhighlight %}

### 71. Explain the copy elision rules for function parameters and return values
**Simple explanation:** Function PARAMETERS are always copied/moved — that step can never be skipped[cite: 1]. Return VALUES, on the other hand, can skip the copy entirely (RVO/NRVO)[cite: 1]. Don't wrap return values in `std::move()` — it can block this optimization[cite: 1].

**Example:**
{% highlight cpp %}
void takesByValue(std::string s) { } // s is always copied/moved in
std::string makeString() { std::string s = "hi"; return s; } // elision possible here
{% endhighlight %}

### 72. What happens when copy constructor throws an exception?
**Simple explanation:** If the copy constructor throws partway through, the object being built is considered "never fully constructed" — so its destructor is NOT called on it, but any already-constructed MEMBERS get properly destroyed[cite: 1]. This is why using member initializer lists (rather than assigning in the body) is safer[cite: 1].

**Example:**
{% highlight cpp %}
class Risky {
    std::string a, b; // if copying 'b' throws, 'a' (already constructed) is destroyed safely
public:
    Risky(const Risky& other) : a(other.a), b(other.b) {}
};
{% endhighlight %}

---

## Section 9: STL Containers Deep Dive (Q73–80)

### 73. Explain iterator invalidation rules for std::vector, std::deque, and std::list
**Simple explanation:**
- `vector`: If it reallocates (grows beyond capacity), ALL iterators/pointers become invalid[cite: 1]. Insert/erase invalidates everything at and after that point[cite: 1].
- `deque`: Inserting in the middle invalidates everything; inserting at the ends invalidates iterators but references/pointers usually stay valid[cite: 1].
- `list`: Only the specific erased element's iterator becomes invalid — everything else stays safe, even after insertion[cite: 1].

**Example:**
{% highlight cpp %}
std::vector<int> v = {1,2,3};
auto it = v.begin();
v.push_back(4); // MIGHT reallocate -> 'it' could now be invalid/dangling
{% endhighlight %}

### 74. What is Small String Optimization (SSO) and how does it affect std::string performance?
**Simple explanation:** Short strings (usually under ~15-23 characters) are stored directly INSIDE the `std::string` object itself, instead of allocating separate heap memory[cite: 1]. This makes small strings much faster to create/copy since there's no heap allocation involved[cite: 1].

**Example:**
{% highlight cpp %}
std::string small = "hi";       // stored inline, no heap allocation (SSO)
std::string big = "a very very long string that exceeds SSO buffer size"; // heap allocated
{% endhighlight %}

### 75. Explain the difference between std::map and std::unordered_map in terms of complexity and when to use each
**Simple explanation:** `std::map` keeps keys sorted using a tree, giving O(log n) operations — good when you need ordered data or range queries[cite: 1]. `std::unordered_map` uses a hash table, giving average O(1) lookups (faster on average) but no ordering, and worst case can degrade to O(n)[cite: 1].

**Example:**
{% highlight cpp %}
std::map<std::string,int> ordered;       // iterates in sorted key order
std::unordered_map<std::string,int> fast; // faster average lookups, no order
{% endhighlight %}

### 76. What are the guarantees of std::vector::push_back vs emplace_back?
**Simple explanation:** `push_back` builds a temporary object first, then moves/copies it in[cite: 1]. `emplace_back` builds the object DIRECTLY inside the vector using the arguments you give it — no temporary needed[cite: 1]. Both are equally exception-safe when the move constructor is `noexcept`[cite: 1].

**Example:**
{% highlight cpp %}
std::vector<std::pair<int,int>> v;
v.push_back(std::make_pair(1,2));   // creates a temporary pair, then moves it in
v.emplace_back(1, 2);               // constructs the pair directly inside the vector
{% endhighlight %}

### 77. Explain why std::vector<bool> is considered broken
**Simple explanation:** `std::vector<bool>` is a special case that packs bits together to save space, so `operator[]` can't return a real `bool&` (there's no individual byte to reference) — it returns a "proxy" object instead[cite: 1]. This breaks normal container expectations, like taking the address of an element[cite: 1].

**Example:**
{% highlight cpp %}
std::vector<bool> v = {true, false};
// bool& ref = v[0]; // ERROR — v[0] doesn't return a real bool reference
{% endhighlight %}

### 78. What is the difference between reserve() and resize() for std::vector?
**Simple explanation:** `reserve(n)` just pre-allocates memory for n elements WITHOUT creating them — the size stays the same[cite: 1]. `resize(n)` actually changes the size and constructs (or destroys) elements to match[cite: 1].

**Example:**
{% highlight cpp %}
std::vector<int> v;
v.reserve(100); // capacity=100, size still 0
v.resize(100);  // size=100, all elements now exist (default-constructed as 0)
{% endhighlight %}

### 79. How does std::unordered_map handle collisions and what is load factor?
**Simple explanation:** When two keys hash to the same "bucket," `unordered_map` chains them together in a small list within that bucket[cite: 1]. "Load factor" = number of elements divided by number of buckets; when it gets too high, the map automatically "rehashes" (grows and redistributes) — which invalidates all iterators[cite: 1].

**Example:**
{% highlight cpp %}
std::unordered_map<int,int> m;
m.reserve(1000); // pre-allocate buckets to avoid repeated rehashing
{% endhighlight %}

### 80. Explain the performance characteristics of inserting into middle of different containers
**Simple explanation:**
- `vector`: O(n) — has to shift everything after the insertion point[cite: 1].
- `deque`: O(n) too, but has faster front/back insertion than vector[cite: 1].
- `list`: O(1) once you already have the iterator — no shifting needed[cite: 1].
- `map`/`set`: O(log n) — needs tree rebalancing[cite: 1].

**Example:**
{% highlight cpp %}
// Frequent middle insertions? Prefer std::list
// Mostly appending at the end? Prefer std::vector
{% endhighlight %}

---

## Section 10: Compile-Time Programming (Q81–87)

### 81. What's the difference between constexpr, consteval, and constinit (C++20)?
**Simple explanation:**
- `constexpr`: CAN run at compile time if given compile-time-known inputs, otherwise runs normally at runtime[cite: 1].
- `consteval`: MUST always run at compile time — using it with runtime-only values is a compile error[cite: 1].
- `constinit`: Forces compile-time INITIALIZATION for a static/global variable, but the variable stays mutable (not const) afterward[cite: 1].

**Example:**
{% highlight cpp %}
constexpr int square(int x) { return x * x; } // can run at compile OR runtime
consteval int mustSquare(int x) { return x * x; } // MUST run at compile time
constinit int globalCounter = 0; // initialized at compile time, but can change later
{% endhighlight %}

### 82. Can you have a constexpr function that doesn't run at compile-time?
**Simple explanation:** Yes! `constexpr` just means "ALLOWED to run at compile time" if the inputs are known then[cite: 1]. If you call it with a value only known at runtime, it just runs like a normal function at runtime instead[cite: 1].

**Example:**
{% highlight cpp %}
constexpr int square(int x) { return x * x; }
constexpr int a = square(5);   // computed at compile time
int n; std::cin >> n;
int b = square(n);             // computed at RUNTIME (n unknown until then)
{% endhighlight %}

### 83. What are the restrictions on constexpr functions in C++11 vs C++14 vs C++20?
**Simple explanation:** Each new C++ version relaxed the rules:
- **C++11**: Only ONE return statement allowed, no loops, no local variable changes[cite: 1].
- **C++14**: Loops, multiple statements, local variables, and mutation are now allowed[cite: 1].
- **C++20**: Even `new`/`delete`, virtual functions, `try`/`catch`, and containers like `std::vector`/`std::string` are allowed[cite: 1].

**Example:**
{% highlight cpp %}
// C++14 style constexpr with a loop (not allowed in C++11):
constexpr int sum(int n) {
    int total = 0;
    for (int i = 1; i <= n; i++) total += i;
    return total;
}
{% endhighlight %}

### 84. Why would you use constinit instead of constexpr for a global variable?
**Simple explanation:** Use `constinit` when you need the variable to be initialized safely at compile time (avoiding the static init order problem), but you STILL need to be able to change its value later — `constexpr` would force it to stay constant forever[cite: 1].

**Example:**
{% highlight cpp %}
constinit int appVersion = 1; // safely initialized at compile time
void update() { appVersion = 2; } // still allowed to change later, unlike constexpr
{% endhighlight %}

### 85. Explain if constexpr and how it enables compile-time branching in templates
**Simple explanation:** Inside a template function, `if constexpr` lets you have different code paths for different template types, and the unused branch doesn't even need to compile — this is cleaner than old SFINAE tricks[cite: 1].

**Example:**
{% highlight cpp %}
template<typename T>
auto getValue(T t) {
    if constexpr (std::is_pointer_v<T>) return *t;
    else return t;
}
{% endhighlight %}

### 86. Can a constexpr constructor contain throw statements?
**Simple explanation:** Since C++20, yes — but ONLY if that throw statement is never actually reached during compile-time evaluation[cite: 1]. If the compiler tries to evaluate a path that throws, compilation fails; but if that throwing branch is only reached at runtime, it's fine[cite: 1].

**Example:**
{% highlight cpp %}
constexpr int checkedDivide(int a, int b) {
    if (b == 0) throw std::runtime_error("div by zero"); // OK if never hit at compile time
    return a / b;
}
{% endhighlight %}

### 87. What happens when you use constinit with a non-static variable?
**Simple explanation:** It's a compile error[cite: 1]. `constinit` only makes sense for variables with "static storage duration" (globals, static locals, thread_locals) — regular local variables inside a function can't use it[cite: 1]. Use plain `constexpr` for local compile-time constants instead[cite: 1].

**Example:**
{% highlight cpp %}
void func() {
    // constinit int x = 5; // ERROR — local variables can't use constinit
    constexpr int y = 5;    // this is fine
}
{% endhighlight %}

---

## Section 11: Modern C++ Attributes (Q88–93)

### 88. What is [[no_unique_address]] (C++20) and when would you use it?
**Simple explanation:** It tells the compiler "this member is allowed to take zero extra space if it's empty" — extending the Empty Base Optimization idea (Q61) to regular member variables, not just base classes[cite: 1]. Handy for stateless helper objects like custom allocators[cite: 1].

**Example:**
{% highlight cpp %}
struct EmptyLogger {};
struct Widget {
    [[no_unique_address]] EmptyLogger logger; // takes zero extra bytes
    int data;
};
{% endhighlight %}

### 89. Explain [[nodiscard]] with a string message (C++20)
**Simple explanation:** `[[nodiscard]]` warns if you call a function and ignore its return value[cite: 1]. In C++20, you can attach a custom message explaining WHY ignoring it is a problem, which shows up in the compiler warning[cite: 1].

**Example:**
{% highlight cpp %}
[[nodiscard("You must check the error code!")]]
int riskyOperation();

riskyOperation(); // compiler warning shows your custom message
{% endhighlight %}

### 90. What is [[carries_dependency]] and when would you use it?
**Simple explanation:** It's a hint related to `memory_order_consume` (Q29), telling the compiler that a dependency chain should be preserved for optimization purposes[cite: 1]. It's very rarely used in practice, since `memory_order_consume` itself is uncommon due to how complex it is to implement correctly[cite: 1].

**Example:**
{% highlight cpp %}
// Rare in real code — most developers use memory_order_acquire instead
{% endhighlight %}

### 91. How does [[maybe_unused]] differ from commenting out warnings?
**Simple explanation:** `[[maybe_unused]]` is a standard, portable way to tell the compiler "I know this variable/parameter isn't used, don't warn me" — cleaner and more explicit than tricks like casting to `(void)` or commenting things[cite: 1].

**Example:**
{% highlight cpp %}
void func([[maybe_unused]] int debugFlag) {
    // debugFlag might only be used in debug builds
}
{% endhighlight %}

### 92. Can you combine multiple attributes on the same declaration?
**Simple explanation:** Yes, you can stack multiple standard attributes together on one declaration, and the order generally doesn't matter[cite: 1].

**Example:**
{% highlight cpp %}
[[nodiscard]] [[deprecated("use newFunc() instead")]]
int oldFunc();
{% endhighlight %}

### 93. What is [[assume]] (C++23) and how does it help optimization?
**Simple explanation:** It tells the compiler "trust me, this condition is always true here" so it can optimize around that assumption (like skipping a null check)[cite: 1]. WARNING: if the assumption is actually wrong at runtime, it's undefined behavior — so only use it for things you've truly proven[cite: 1].

**Example:**
{% highlight cpp %}
void func(int* ptr) {
    [[assume(ptr != nullptr)]];
    *ptr = 5; // compiler can skip generating a null-check here
}
{% endhighlight %}

---

## Section 12: Lambda Expressions Advanced (Q94–100)

### 94. Why do lambdas capture by value as const by default? When do you need mutable?
**Simple explanation:** A lambda's internal `operator()` is `const` by default, meaning captured-by-value variables can't be changed inside the lambda[cite: 1]. If you need the lambda to modify its own copy of a captured variable (like a running counter), add the `mutable` keyword[cite: 1].

**Example:**
{% highlight cpp %}
int count = 0;
auto counter = [count]() mutable { count++; return count; };
counter(); // returns 1
counter(); // returns 2 (count is its own mutable copy inside the lambda)
{% endhighlight %}

### 95. Explain the difference between capturing [=], [&], [this], and [*this] (C++17)
**Simple explanation:**
- `[=]`: capture everything used, BY VALUE (copies)[cite: 1].
- `[&]`: capture everything used, BY REFERENCE[cite: 1].
- `[this]`: capture the `this` pointer, so you can access the object's members (but the object itself isn't copied)[cite: 1].
- `[*this]`: capture a full COPY of the whole object (C++17) — safer for async code where `this` might be destroyed before the lambda runs[cite: 1].

**Example:**
{% highlight cpp %}
struct Widget {
    int value = 5;
    auto getLambdaSafe() { return [*this]() { return value; }; } // safe copy
    auto getLambdaRisky() { return [this]() { return value; }; } // dangling if Widget destroyed
};
{% endhighlight %}

### 96. What is a stateless lambda and why is it convertible to function pointer?
**Simple explanation:** A lambda with an empty capture list `[]` doesn't store any extra data, so it behaves just like a plain function — the compiler allows converting it directly to a C-style function pointer, useful for old C APIs[cite: 1].

**Example:**
{% highlight cpp %}
int (*fp)(int) = [](int x) { return x * 2; }; // works — no captures, so it's "stateless"
{% endhighlight %}

### 97. Explain init-capture (generalized lambda capture) and move-only captures
**Simple explanation:** Since C++14, you can capture a variable WITH an expression/initializer, letting you rename it or even MOVE a move-only object (like `unique_ptr`) directly into the lambda[cite: 1].

**Example:**
{% highlight cpp %}
auto ptr = std::make_unique<int>(42);
auto lambda = [p = std::move(ptr)]() { return *p; }; // move-only capture
{% endhighlight %}

### 98. How do generic lambdas (C++14) differ from template functions?
**Simple explanation:** A generic lambda uses `auto` as a parameter type, which makes the compiler create a templated function-call operator behind the scenes[cite: 1]. It's basically shorthand for a mini template function, but you can't explicitly specify the type when calling it (until C++20 template lambdas)[cite: 1].

**Example:**
{% highlight cpp %}
auto add = [](auto a, auto b) { return a + b; };
add(1, 2);       // works with ints
add(1.5, 2.5);   // works with doubles too — same lambda, different types
{% endhighlight %}

### 99. What is the lifetime of lambda captures and what are the dangers?
**Simple explanation:** Captured-BY-REFERENCE variables can "dangle" (become invalid) if the original variable is destroyed before the lambda runs — especially dangerous for async/delayed calls[cite: 1]. Captured-BY-VALUE variables are copied when the lambda is created, so they're safer and independent[cite: 1].

**Example:**
{% highlight cpp %}
std::function<int()> makeDangerous() {
    int local = 5;
    return [&local]() { return local; }; // DANGER: local is destroyed when function returns!
}
{% endhighlight %}

### 100. Explain immediately-invoked lambda expressions (IIFE) and their use cases
**Simple explanation:** You define a lambda AND call it immediately with `()` right after — useful for running some complex setup logic once, and assigning the RESULT to a `const` variable in one clean line[cite: 1].

**Example:**
{% highlight cpp %}
const int result = [&]() {
    if (someCondition) return 10;
    return 20;
}(); // called immediately — result is const, but logic was complex
{% endhighlight %}

---

## Section 13: Virtual Functions & OOP Deep Dive (Q101–107)

### 101. Why is it important to make destructors virtual in base classes?
**Simple explanation:** If you `delete` a derived object through a BASE class pointer, and the destructor isn't virtual, only the base class's destructor runs — the derived part's cleanup gets skipped, leaking memory/resources[cite: 1]. Rule: if a class has ANY virtual function, its destructor should be virtual too[cite: 1].

**Example:**
{% highlight cpp %}
class Base { public: virtual ~Base() = default; }; // virtual — safe!
class Derived : public Base { std::vector<int> data; };

Base* obj = new Derived();
delete obj; // correctly calls Derived's destructor too, thanks to virtual
{% endhighlight %}

### 102. What is the performance cost of virtual functions?
**Simple explanation:** Calling a virtual function requires looking up the correct function in a "vtable" (a hidden lookup table), which is an extra indirect step compared to calling a normal function directly[cite: 1]. This is usually a small cost (~1.5–3x slower for that call), often unnoticeable except in very tight, performance-critical loops[cite: 1].

**Example:**
{% highlight cpp %}
// direct call: compiler can inline it easily
regularFunc();
// virtual call: must look up the right function via vtable pointer at runtime
basePtr->virtualFunc();
{% endhighlight %}

### 103. Explain pure virtual functions and abstract classes. Can abstract classes have constructors?
**Simple explanation:** A "pure virtual" function (`= 0`) has no implementation and forces derived classes to provide one[cite: 1]. A class with at least one pure virtual function is "abstract" and can't be instantiated directly[cite: 1]. YES, abstract classes can have constructors — they just get called automatically when a derived (concrete) class is created[cite: 1].

**Example:**
{% highlight cpp %}
class Shape {
public:
    Shape() { /* still runs when Derived is created */ }
    virtual double area() = 0; // pure virtual — makes Shape abstract
};
class Circle : public Shape {
public:
    double area() override { return 3.14; }
};
{% endhighlight %}

### 104. What is the difference between override and final specifiers?
**Simple explanation:** `override` tells the compiler "I intend to override a base class virtual function — please check that I actually did it right" (catches typos in function signatures)[cite: 1]. `final` PREVENTS further overriding of that function (or further inheriting from that class), which can also help the compiler optimize[cite: 1].

**Example:**
{% highlight cpp %}
class Base { virtual void foo(); };
class Derived : public Base {
    void foo() override final; // overrides correctly, and can't be overridden further
};
{% endhighlight %}

### 105. Can you override a non-virtual function? What happens?
**Simple explanation:** You CAN write a function with the same name in a derived class, but since the base version wasn't `virtual`, this isn't a true "override" — it's called "hiding."[cite: 1] Which version gets called depends on the STATIC type of the pointer/reference used, not the actual object type — a common source of bugs[cite: 1].

**Example:**
{% highlight cpp %}
class Base { public: void greet() { std::cout << "Base"; } };
class Derived : public Base { public: void greet() { std::cout << "Derived"; } };

Base* b = new Derived();
b->greet(); // prints "Base" — NOT "Derived", because greet() isn't virtual!
{% endhighlight %}

### 106. Explain covariant return types in virtual functions
**Simple explanation:** When overriding a virtual function, the derived class's version is ALLOWED to return a more specific (derived) pointer/reference type than the base version, as long as it's still related by inheritance[cite: 1]. Only works with pointers/references, not plain values[cite: 1].

**Example:**
{% highlight cpp %}
class Base { public: virtual Base* clone() { return new Base(*this); } };
class Derived : public Base { public: Derived* clone() override { return new Derived(*this); } };
// Derived::clone() returns Derived*, not Base* — that's covariant
{% endhighlight %}

### 107. What is the "slicing problem" and how do you prevent it?
**Simple explanation:** If you assign a DERIVED object to a BASE-typed variable BY VALUE (not pointer/reference), only the base part gets copied — the derived-specific data is "sliced off" and lost, and polymorphism breaks[cite: 1]. Prevention: always use pointers or references for polymorphic objects[cite: 1].

**Example:**
{% highlight cpp %}
class Base { public: int x = 1; };
class Derived : public Base { public: int y = 2; };

Derived d;
Base b = d; // SLICED! b.x copied, but 'y' is lost, and b behaves as pure Base now
{% endhighlight %}

---

## Section 14: Scoped Enums & Casting (Q108–114)

### 108. What are the advantages of enum class over traditional enum?
**Simple explanation:** `enum class` (scoped enum) doesn't silently convert to `int`, and its values don't leak into the surrounding scope (no naming conflicts)[cite: 1]. Regular `enum` allows implicit conversion to int and pollutes the enclosing namespace with its names[cite: 1].

**Example:**
{% highlight cpp %}
enum class Color { Red, Green };  // Color::Red - scoped, no implicit int conversion
enum OldColor { OldRed, OldGreen }; // OldRed usable directly, converts to int silently
{% endhighlight %}

### 109. How do you convert between scoped enum and integer types?
**Simple explanation:** Since `enum class` doesn't implicitly convert, you must use an EXPLICIT `static_cast` in both directions[cite: 1].

**Example:**
{% highlight cpp %}
enum class Color { Red = 1 };
int val = static_cast<int>(Color::Red);       // enum -> int
Color c = static_cast<Color>(1);              // int -> enum
{% endhighlight %}

### 110. Explain the four types of C++ casts and when to use each
**Simple explanation:**
- `static_cast`: normal, checked conversions (int to float, related class pointers)[cite: 1]. Most common, safest choice[cite: 1].
- `dynamic_cast`: safe downcasting for polymorphic types at RUNTIME, returns `nullptr` on failure[cite: 1]. Slower (uses RTTI)[cite: 1].
- `const_cast`: adds or removes `const`[cite: 1]. Rarely needed — usually a sign of bad design[cite: 1].
- `reinterpret_cast`: reinterprets raw bits (like pointer to integer)[cite: 1]. Very dangerous, low-level only[cite: 1].

**Example:**
{% highlight cpp %}
double d = 3.14;
int i = static_cast<int>(d);          // safe, common

Base* b = new Derived();
Derived* dPtr = dynamic_cast<Derived*>(b); // safe downcast, nullptr if wrong type
{% endhighlight %}

### 111. What is RTTI and when is dynamic_cast safe?
**Simple explanation:** RTTI (Run-Time Type Information) lets the program figure out an object's REAL type while running, which is what powers `dynamic_cast` and `typeid`[cite: 1]. It requires the class to have virtual functions[cite: 1]. `dynamic_cast` is "safe" because it returns `nullptr` (for pointers) instead of crashing if the cast is wrong[cite: 1].

**Example:**
{% highlight cpp %}
Base* b = new Base();
Derived* d = dynamic_cast<Derived*>(b); // returns nullptr — b isn't really a Derived
if (!d) std::cout << "cast failed safely";
{% endhighlight %}

### 112. Explain const-correctness and the different types of const member functions
**Simple explanation:** Marking a member function `const` promises it won't change the object's data, which lets you call it on `const` objects too[cite: 1]. "Bitwise const" means literally nothing changes; "logical const" allows changing hidden implementation details (like a cache) using `mutable`, while the object still LOOKS unchanged from the outside[cite: 1].

**Example:**
{% highlight cpp %}
class Widget {
    int value;
public:
    int getValue() const { return value; } // promises not to modify Widget
};
{% endhighlight %}

### 113. What is mutable keyword and when would you use it?
**Simple explanation:** `mutable` lets a specific member be changed even inside a `const` member function — useful for things like caching a computed result, or a mutex used just for internal synchronization, where the object's LOGICAL state doesn't actually change[cite: 1].

**Example:**
{% highlight cpp %}
class ExpensiveCalc {
    mutable std::optional<int> cache;
public:
    int getResult() const {
        if (!cache) cache = doExpensiveWork(); // allowed even though function is const
        return *cache;
    }
};
{% endhighlight %}

### 114. Can you const_cast away const and modify the object?
**Simple explanation:** If the object was ORIGINALLY non-const (just accessed through a const pointer/reference), removing const and modifying it is technically okay[cite: 1]. But if the object was truly declared `const` from the start, modifying it after `const_cast` is undefined behavior — don't do it[cite: 1].

**Example:**
{% highlight cpp %}
void legacyFunc(int* p) { *p += 1; } // old API, doesn't use const (but doesn't need to modify)
const int x = 5;
// const_cast<int*>(&x); then modifying -> UNDEFINED BEHAVIOR, x was truly const
{% endhighlight %}

---

## Section 15: Advanced Edge Cases & Best Practices (Q115–120)

### 115. What is the difference between nullptr, NULL, and 0 in C++?
**Simple explanation:** `nullptr` is a proper, type-safe null pointer (its own type), and always correctly picks pointer-related function overloads[cite: 1]. `NULL` is just an old macro (usually `0`), and `0` is a plain integer — both can accidentally cause confusing overload resolution issues[cite: 1]. Always use `nullptr` in modern C++[cite: 1].

**Example:**
{% highlight cpp %}
void f(int x) { std::cout << "int"; }
void f(char* p) { std::cout << "pointer"; }
f(NULL);    // ambiguous/confusing — NULL might pick int version!
f(nullptr); // always correctly picks the pointer version
{% endhighlight %}

### 116. Explain the difference between delete and delete[]. What happens if you mix them?
**Simple explanation:** `delete` frees a SINGLE object (calls one destructor)[cite: 1]. `delete[]` frees an ARRAY of objects (calls a destructor for each element)[cite: 1]. Mixing them up (e.g., `new[]` then `delete`) causes undefined behavior — wrong destructor counts, heap corruption[cite: 1]. Best practice: use `std::vector` or `std::unique_ptr<T[]>` instead of manual arrays[cite: 1].

**Example:**
{% highlight cpp %}
int* arr = new int[10];
// delete arr;   // WRONG — should be delete[] arr;
delete[] arr;    // correct
{% endhighlight %}

### 117. What is the "as-if" rule in C++ optimization?
**Simple explanation:** The compiler is free to rewrite/optimize your code HOWEVER it wants, as long as the observable, visible behavior stays exactly the same "as if" it ran your original code literally[cite: 1]. This is what allows aggressive optimizations like inlining, reordering, and dead-code removal[cite: 1].

**Example:**
{% highlight cpp %}
int compute() {
    int a = 5; // compiler might completely remove this since it's unused elsewhere
    return 10; // observable result is what matters
}
{% endhighlight %}

### 118. Explain name mangling and why extern "C" is needed
**Simple explanation:** C++ "mangles" (encodes) function names to include extra info like parameter types and namespaces, so overloaded functions can have unique internal names[cite: 1]. C doesn't do this[cite: 1]. `extern "C"` tells the compiler to use plain, unmangled C-style names — needed when linking with C libraries or exporting from DLLs[cite: 1].

**Example:**
{% highlight cpp %}
extern "C" {
    void myFunc(int x); // exported with a plain C name, usable from C code
}
{% endhighlight %}

### 119. What is aggregate initialization and how does it differ from list initialization?
**Simple explanation:** Aggregate initialization directly fills in a simple struct/array's public members in order, without needing a constructor at all[cite: 1]. List initialization (`{}`) is a broader concept that ALSO works with constructors (via `std::initializer_list` or normal constructors), not just simple aggregates[cite: 1].

**Example:**
{% highlight cpp %}
struct Point { int x; int y; }; // no constructors -> "aggregate"
Point p{1, 2}; // aggregate initialization — fills x=1, y=2 directly

std::vector<int> v{1, 2, 3}; // list initialization, uses constructor internally
{% endhighlight %}

### 120. Explain the "zero-overhead principle" in C++ and give examples where it's violated
**Simple explanation:** The idea is: "you shouldn't pay (in performance) for a feature you don't use, and if you DO use it, hand-written code couldn't do better."[cite: 1] Things like RAII, templates, and `constexpr` mostly follow this[cite: 1]. But some features break it a little: exceptions can bloat code size even in paths that never throw, RTTI adds overhead even if you never use `dynamic_cast`, and `std::shared_ptr`'s atomic reference counting has a cost you can't fully "opt out" of once you use it[cite: 1].

**Example:**
{% highlight cpp %}
// std::shared_ptr always pays for atomic increment/decrement,
// even in single-threaded programs where it's unnecessary — a small violation
// of "you don't pay for what you don't need."
{% endhighlight %}

---

