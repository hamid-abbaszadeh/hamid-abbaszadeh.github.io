---
layout: default
title: "21 Advanced C++ Coding Challenges"
parent: "<span style='color: #4ade80;'>Coding Challenges</span>"
nav_order: 2
---

# 21 Advanced C++ Coding Challenges for Senior Developers

Master complex C++ technical interview topics with detailed explanations and full code examples spanning template metaprogramming, memory management, lock-free concurrency, and C++20 features.

<span class="label label-blue">Modern C++</span>
<span class="label label-green">C++11 / C++17 / C++20</span>
<span class="label label-purple">Coding Challenges</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Overview

Here is the complete reference guide containing all 21 challenges complete with sample tasks, architectural context, and complete C++ implementations.

---

## Language Fundamentals

### Challenge 1: Const-Correctness
**Why It's Challenging:** Understanding when and how to enforce `const` guarantees separates entry-level developers from senior engineers. It requires controlling mutability while providing optimal access paths for both readable and writable instances.

**Sample Task:** Implement a class with a method that provides both `const` and non-const versions of an accessor.

{% highlight cpp %}
#include <iostream>
#include <string>

class Document {
    std::string content;
public:
    Document(const std::string& text) : content(text) {}

    // Read-only accessor for const instances
    const std::string& getContent() const { return content; }

    // Writable accessor for non-const instances
    std::string& getContent() { return content; }
};

int main() {
    Document doc("Sample text");
    doc.getContent() = "Modified text"; // Calls non-const version

    const Document constDoc("Read-only text");
    std::cout << "Const content: " << constDoc.getContent() << "\n"; // Calls const version
    return 0;
}
{% endhighlight %}

---

### Challenge 2: Perfect Forwarding with Variadic Templates
**Why It's Challenging:** Perfect forwarding relies on universal reference collapse rules (`T&&`), variadic parameter packs, and `std::forward` to preserve exact value categories (lvalues vs rvalues) without extra copies.

**Sample Task:** Implement a generic wrapper function that perfectly forwards its arguments to another function while logging argument types.

{% highlight cpp %}
#include <iostream>
#include <utility>
#include <typeinfo>
#include <string>

template <typename F, typename... Args>
auto function_logger(F&& f, Args&&... args) {
    // Log argument types using C++17 fold expression
    (std::cout << ... << (std::string(typeid(Args).name()) + " "));
    std::cout << "\n";

    // Perfect forward the call
    return std::forward<F>(f)(std::forward<Args>(args)...);
}

int add(int a, int b) { return a + b; }

int main() {
    auto result = function_logger(add, 5, 3);
    std::cout << "Result: " << result << "\n";
    return 0;
}
{% endhighlight %}

---

### Challenge 3: SFINAE with Type Traits
**Why It's Challenging:** SFINAE (Substitution Failure Is Not An Error) requires manipulating template substitution rules and standard type traits to selectively enable or disable function overloads.

**Sample Task:** Implement a function template that accepts only container types containing a `.size()` method.

{% highlight cpp %}
#include <iostream>
#include <vector>
#include <type_traits>

// Primary template fallback
template <typename T, typename = void>
struct has_size_method : std::false_type {};

// Specialization enabled via SFINAE when .size() exists
template <typename T>
struct has_size_method<T, std::void_t<decltype(std::declval<T>().size())>> : std::true_type {};

template <typename Container>
auto get_size(const Container& c) -> std::enable_if_t<has_size_method<Container>::value, std::size_t> {
    return c.size();
}

int main() {
    std::vector<int> vec = {10, 20, 30};
    std::cout << "Container size: " << get_size(vec) << "\n";
    return 0;
}
{% endhighlight %}

---

## Algorithms

### Challenge 4: Graph Traversal
**Why It's Challenging:** Tests understanding of recursive stack management, graph representations via adjacency lists, and state-tracking mechanisms.

**Sample Task:** Implement Depth First Search (DFS) for an undirected graph.

{% highlight cpp %}
#include <iostream>
#include <vector>

void dfs(int node, const std::vector<std::vector<int>>& graph, std::vector<bool>& visited) {
    visited[node] = true;
    std::cout << node << " ";

    for (int neighbor : graph[node]) {
        if (!visited[neighbor]) {
            dfs(neighbor, graph, visited);
        }
    }
}

int main() {
    std::vector<std::vector<int>> graph = {
        {1, 2},    // Node 0
        {0, 3},    // Node 1
        {0},       // Node 2
        {1}        // Node 3
    };

    std::vector<bool> visited(graph.size(), false);
    std::cout << "DFS Nodes: ";
    dfs(0, graph, visited);
    std::cout << "\n";
    return 0;
}
{% endhighlight %}

---

### Challenge 5: Lock-Free Algorithm Implementation
**Why It's Challenging:** Requires low-level knowledge of `std::atomic`, atomic compare-and-swap operations (`compare_exchange_weak`), and lock-free node allocation.

**Sample Task:** Implement a lock-free queue using atomic operations.

<details>
<summary>Click to view Lock-Free Queue implementation</summary>

{% highlight cpp %}
#include <iostream>
#include <atomic>
#include <memory>

template <typename T>
class LockFreeQueue {
    struct Node {
        std::shared_ptr<T> data;
        std::atomic<Node*> next;
        Node() : next(nullptr) {}
    };

    std::atomic<Node*> head;
    std::atomic<Node*> tail;

public:
    LockFreeQueue() {
        Node* dummy = new Node();
        head.store(dummy);
        tail.store(dummy);
    }

    ~LockFreeQueue() {
        while (Node* old_head = head.load()) {
            head.store(old_head->next);
            delete old_head;
        }
    }

    void enqueue(T value) {
        auto new_data = std::make_shared<T>(value);
        Node* new_node = new Node();
        Node* old_tail = nullptr;

        while (true) {
            old_tail = tail.load();
            Node* next = old_tail->next.load();
            if (old_tail == tail.load()) {
                if (next == nullptr) {
                    new_node->data = new_data;
                    if (old_tail->next.compare_exchange_weak(next, new_node)) {
                        break;
                    }
                } else {
                    tail.compare_exchange_weak(old_tail, next);
                }
            }
        }
        tail.compare_exchange_weak(old_tail, new_node);
    }
};

int main() {
    LockFreeQueue<int> q;
    q.enqueue(100);
    std::cout << "Lock-free enqueue executed successfully.\n";
    return 0;
}
{% endhighlight %}
</details>

---

### Challenge 6: Dijkstra's Algorithm
**Why It's Challenging:** Requires efficiently updating shortest distance tracks using graph adjacency structures and priority queues.

**Sample Task:** Write a function that finds the shortest path in a weighted graph represented as an adjacency list.

{% highlight cpp %}
#include <iostream>
#include <vector>
#include <queue>
#include <limits>

using Edge = std::pair<int, int>; // {neighbor, weight}

std::vector<int> dijkstra(int start, const std::vector<std::vector<Edge>>& graph) {
    std::vector<int> dist(graph.size(), std::numeric_limits<int>::max());
    std::priority_queue<Edge, std::vector<Edge>, std::greater<Edge>> pq;

    dist[start] = 0;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        if (d > dist[u]) continue;

        for (const auto& [v, weight] : graph[u]) {
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

int main() {
    std::vector<std::vector<Edge>> graph = {
        { {1, 4}, {2, 1} }, // Node 0
        { {3, 1} },         // Node 1
        { {1, 2}, {3, 5} }, // Node 2
        {}                  // Node 3
    };

    auto distances = dijkstra(0, graph);
    std::cout << "Shortest distance from 0 to 3: " << distances[3] << "\n";
    return 0;
}
{% endhighlight %}

---

### Challenge 7: Merge Intervals
**Why It's Challenging:** Tests ordering custom data structures using sorting algorithms and merging overlapping bounds in $O(N \log N)$ time.

**Sample Task:** Given an array of intervals, merge all overlapping intervals into a single consolidated vector.

{% highlight cpp %}
#include <iostream>
#include <vector>
#include <algorithm>

std::vector<std::vector<int>> mergeIntervals(std::vector<std::vector<int>>& intervals) {
    if (intervals.empty()) return {};
    
    std::sort(intervals.begin(), intervals.end());
    std::vector<std::vector<int>> merged;
    auto current = intervals[0];

    for (size_t i = 1; i < intervals.size(); ++i) {
        if (intervals[i][0] <= current[1]) {
            current[1] = std::max(current[1], intervals[i][1]);
        } else {
            merged.push_back(current);
            current = intervals[i];
        }
    }
    merged.push_back(current);
    return merged;
}

int main() {
    std::vector<std::vector<int>> input = { {1, 3}, {2, 6}, {8, 10}, {15, 18} };
    auto result = mergeIntervals(input);
    
    for (const auto& interval : result) {
        std::cout << "[" << interval[0] << ", " << interval[1] << "] ";
    }
    std::cout << "\n";
    return 0;
}
{% endhighlight %}

---

## Data Structures

### Challenge 8: Custom Hash Map
**Why It's Challenging:** Design requires understanding bucket management, dynamic rehashing, key equality, and collision resolution techniques.

**Sample Task:** Design a lightweight hash map supporting fundamental insertion and retrieval operations.

{% highlight cpp %}
#include <iostream>
#include <vector>
#include <list>
#include <utility>
#include <string>

template <typename K, typename V>
class SimpleHashMap {
    struct KeyValue { K key; V value; };
    std::vector<std::list<KeyValue>> buckets;
    size_t capacity;

    size_t getHash(const K& key) const {
        return std::hash<K>{}(key) % capacity;
    }

public:
    SimpleHashMap(size_t cap = 16) : capacity(cap), buckets(cap) {}

    void insert(const K& key, const V& value) {
        auto& bucket = buckets[getHash(key)];
        for (auto& pair : bucket) {
            if (pair.key == key) {
                pair.value = value;
                return;
            }
        }
        bucket.push_back({key, value});
    }

    bool get(const K& key, V& outValue) const {
        const auto& bucket = buckets[getHash(key)];
        for (const auto& pair : bucket) {
            if (pair.key == key) {
                outValue = pair.value;
                return true;
            }
        }
        return false;
    }
};

int main() {
    SimpleHashMap<std::string, int> map;
    map.insert("Apple", 5);
    int val = 0;
    if (map.get("Apple", val)) {
        std::cout << "Apple count: " << val << "\n";
    }
    return 0;
}
{% endhighlight %}

---

### Challenge 9: Advanced Tree Structure (LRU Cache with Hash Map & Doubly Linked List)
**Why It's Challenging:** Requires managing $O(1)$ operations across dual data structures (lookup table coupled with node relocation).

**Sample Task:** Implement a Least Recently Used (LRU) Cache supporting constant-time lookups and evictions.

<details>
<summary>Click to view LRU Cache implementation</summary>

{% highlight cpp %}
#include <iostream>
#include <unordered_map>
#include <list>

class LRUCache {
    int capacity;
    std::list<std::pair<int, int>> cacheList;
    std::unordered_map<int, decltype(cacheList.begin())> cacheMap;

public:
    LRUCache(int cap) : capacity(cap) {}

    int get(int key) {
        auto it = cacheMap.find(key);
        if (it == cacheMap.end()) return -1;
        cacheList.splice(cacheList.begin(), cacheList, it->second);
        return it->second->second;
    }

    void put(int key, int value) {
        auto it = cacheMap.find(key);
        if (it != cacheMap.end()) {
            it->second->second = value;
            cacheList.splice(cacheList.begin(), cacheList, it->second);
            return;
        }
        if (cacheList.size() == capacity) {
            int oldKey = cacheList.back().first;
            cacheMap.erase(oldKey);
            cacheList.pop_back();
        }
        cacheList.push_front({key, value});
        cacheMap[key] = cacheList.begin();
    }
};

int main() {
    LRUCache cache(2);
    cache.put(1, 100);
    cache.put(2, 200);
    std::cout << "Get 1: " << cache.get(1) << "\n"; // Returns 100
    cache.put(3, 300); // Evicts key 2
    std::cout << "Get 2: " << cache.get(2) << "\n"; // Returns -1 (not found)
    return 0;
}
{% endhighlight %}
</details>

---

### Challenge 10: Custom Linked List Implementation
**Why It's Challenging:** Tests raw pointer ownership, manual memory cleanup, node allocation, and boundary checks.

**Sample Task:** Implement a single-linked list supporting efficient node reversal.

{% highlight cpp %}
#include <iostream>

template <typename T>
class LinkedList {
    struct Node {
        T data;
        Node* next;
        Node(T val) : data(val), next(nullptr) {}
    };
    Node* head = nullptr;

public:
    ~LinkedList() {
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }

    void push_front(T val) {
        Node* node = new Node(val);
        node->next = head;
        head = node;
    }

    void reverse() {
        Node* prev = nullptr;
        Node* current = head;
        Node* next = nullptr;
        while (current) {
            next = current->next;
            current->next = prev;
            prev = current;
            current = next;
        }
        head = prev;
    }

    void print() const {
        Node* curr = head;
        while (curr) {
            std::cout << curr->data << " -> ";
            curr = curr->next;
        }
        std::cout << "nullptr\n";
    }
};

int main() {
    LinkedList<int> list;
    list.push_front(3);
    list.push_front(2);
    list.push_front(1);
    list.reverse();
    list.print();
    return 0;
}
{% endhighlight %}

---

## Object-Oriented Programming

### Challenge 11: Polymorphism with Abstract Classes
**Why It's Challenging:** Demonstrates proper usage of pure virtual functions (`= 0`), virtual destructors, and interface abstraction contracts.

**Sample Task:** Design an abstract class `Shape` with derived classes `Circle` and `Rectangle` implementing custom area calculations.

{% highlight cpp %}
#include <iostream>
#include <vector>
#include <memory>

class Shape {
public:
    virtual double area() const = 0; // Pure virtual function
    virtual ~Shape() = default;      // Virtual destructor
};

class Circle : public Shape {
    double radius;
public:
    Circle(double r) : radius(r) {}
    double area() const override { return 3.14159 * radius * radius; }
};

class Rectangle : public Shape {
    double width, height;
public:
    Rectangle(double w, double h) : width(w), height(h) {}
    double area() const override { return width * height; }
};

int main() {
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(5.0));
    shapes.push_back(std::make_unique<Rectangle>(4.0, 6.0));

    for (const auto& shape : shapes) {
        std::cout << "Shape Area: " << shape->area() << "\n";
    }
    return 0;
}
{% endhighlight %}

---

### Challenge 12: Policy-Based Design
**Why It's Challenging:** Policy-based design uses template parameters to configure compile-time behavioral strategies without incurring virtual function overhead.

**Sample Task:** Implement a logger class that accepts customizable output destination policies at compile time.

{% highlight cpp %}
#include <iostream>
#include <string>

struct ConsoleOutputPolicy {
    static void write(const std::string& msg) {
        std::cout << "[Console]: " << msg << "\n";
    }
};

struct DetailedOutputPolicy {
    static void write(const std::string& msg) {
        std::cout << "[Detailed Log]: " << msg << "\n";
    }
};

template <typename OutputPolicy>
class Logger : public OutputPolicy {
public:
    void log(const std::string& message) {
        OutputPolicy::write(message);
    }
};

int main() {
    Logger<ConsoleOutputPolicy> consoleLogger;
    consoleLogger.log("Application started");

    Logger<DetailedOutputPolicy> detailedLogger;
    detailedLogger.log("Critical system state check");
    return 0;
}
{% endhighlight %}

---

### Challenge 13: Operator Overloading
**Why It's Challenging:** Designing clean arithmetic and stream operator overloads requires keeping value semantics intact while adhering to expected mathematical invariants.

**Sample Task:** Create a `ComplexNumber` class that overloads `+`, `-`, and stream insertion (`<<`) operators.

{% highlight cpp %}
#include <iostream>

class ComplexNumber {
    double real;
    double imag;
public:
    ComplexNumber(double r = 0, double i = 0) : real(r), imag(i) {}

    ComplexNumber operator+(const ComplexNumber& other) const {
        return ComplexNumber(real + other.real, imag + other.imag);
    }

    friend std::ostream& operator<<(std::ostream& os, const ComplexNumber& c) {
        os << c.real << " + " << c.imag << "i";
        return os;
    }
};

int main() {
    ComplexNumber c1(3.0, 4.0);
    ComplexNumber c2(1.5, 2.5);
    ComplexNumber c3 = c1 + c2;

    std::cout << "Sum: " << c3 << "\n";
    return 0;
}
{% endhighlight %}

---

## Efficient Memory Management

### Challenge 14: Custom Smart Pointer
**Why It's Challenging:** Requires controlling reference counts, move semantics, copy assignment logic, and automatic RAII destruction.

**Sample Task:** Implement a reference-counted custom shared pointer (`MySharedPtr`).

<details>
<summary>Click to view Custom Smart Pointer implementation</summary>

{% highlight cpp %}
#include <iostream>

template <typename T>
class MySharedPtr {
    T* ptr = nullptr;
    size_t* ref_count = nullptr;

    void cleanup() {
        if (ref_count) {
            (*ref_count)--;
            if (*ref_count == 0) {
                delete ptr;
                delete ref_count;
            }
        }
    }

public:
    explicit MySharedPtr(T* p = nullptr) : ptr(p) {
        if (p) ref_count = new size_t(1);
    }

    ~MySharedPtr() { cleanup(); }

    MySharedPtr(const MySharedPtr& other) : ptr(other.ptr), ref_count(other.ref_count) {
        if (ref_count) (*ref_count)++;
    }

    MySharedPtr& operator=(const MySharedPtr& other) {
        if (this != &other) {
            cleanup();
            ptr = other.ptr;
            ref_count = other.ref_count;
            if (ref_count) (*ref_count)++;
        }
        return *this;
    }

    T& operator*() const { return *ptr; }
    T* operator->() const { return ptr; }
    size_t use_count() const { return ref_count ? *ref_count : 0; }
};

int main() {
    MySharedPtr<int> p1(new int(42));
    {
        MySharedPtr<int> p2 = p1;
        std::cout << "Ref count: " << p1.use_count() << "\n"; // Outputs 2
    }
    std::cout << "Ref count after scope: " << p1.use_count() << "\n"; // Outputs 1
    return 0;
}
{% endhighlight %}
</details>

---

### Challenge 15: Memory Pool Implementation
**Why It's Challenging:** Pre-allocating contiguous memory chunks improves speed by bypassing frequent OS global `new`/`delete` calls.

**Sample Task:** Implement a block-based fixed-size memory pool allocator.

{% highlight cpp %}
#include <iostream>
#include <vector>

class FixedMemoryPool {
    struct Block { Block* next; };
    Block* freeList = nullptr;
    std::vector<char*> poolStorage;
    size_t blockSize;

public:
    FixedMemoryPool(size_t bSize, size_t blockCount) : blockSize(bSize) {
        char* pool = new char[bSize * blockCount];
        poolStorage.push_back(pool);
        
        for (size_t i = 0; i < blockCount; ++i) {
            Block* block = reinterpret_cast<Block*>(pool + (i * bSize));
            block->next = freeList;
            freeList = block;
        }
    }

    ~FixedMemoryPool() {
        for (char* pool : poolStorage) delete[] pool;
    }

    void* allocate() {
        if (!freeList) throw std::bad_alloc();
        Block* head = freeList;
        freeList = freeList->next;
        return head;
    }

    void deallocate(void* ptr) {
        Block* block = static_cast<Block*>(ptr);
        block->next = freeList;
        freeList = block;
    }
};

int main() {
    FixedMemoryPool pool(sizeof(int), 10);
    int* p1 = static_cast<int*>(pool.allocate());
    *p1 = 99;
    std::cout << "Allocated Pool Value: " << *p1 << "\n";
    pool.deallocate(p1);
    return 0;
}
{% endhighlight %}

---

### Challenge 16: Memory Arena Allocator
**Why It's Challenging:** Arenas provide ultra-fast bump allocation across a single contiguous buffer and perform instant reset releases.

**Sample Task:** Implement a contiguous Arena Memory Allocator supporting standard alignment restrictions.

{% highlight cpp %}
#include <iostream>
#include <cstddef>
#include <cstdint>

class ArenaAllocator {
    char* buffer;
    size_t capacity;
    size_t offset = 0;

public:
    ArenaAllocator(size_t cap) : capacity(cap) {
        buffer = new char[cap];
    }

    ~ArenaAllocator() { delete[] buffer; }

    void* allocate(size_t bytes, size_t alignment = alignof(std::max_align_t)) {
        uintptr_t currentPtr = reinterpret_cast<uintptr_t>(buffer + offset);
        size_t padding = (alignment - (currentPtr % alignment)) % alignment;

        if (offset + padding + bytes > capacity) throw std::bad_alloc();

        offset += padding;
        void* ptr = buffer + offset;
        offset += bytes;
        return ptr;
    }

    void reset() { offset = 0; }
};

int main() {
    ArenaAllocator arena(1024);
    int* num = static_cast<int*>(arena.allocate(sizeof(int)));
    *num = 777;
    std::cout << "Arena Allocated Value: " << *num << "\n";
    arena.reset(); // Resets allocation offset in O(1) time
    return 0;
}
{% endhighlight %}

---

## Concurrency and Multithreading

### Challenge 17: Thread Synchronization with Mutex
**Why It's Challenging:** Demonstrates managing concurrent access to shared data using `std::mutex` and safe RAII wrappers (`std::lock_guard`).

**Sample Task:** Protect a shared counter updated concurrently across multiple threads.

{% highlight cpp %}
#include <iostream>
#include <thread>
#include <vector>
#include <mutex>

class SynchronizedCounter {
    int count = 0;
    std::mutex mtx;

public:
    void increment() {
        std::lock_guard<std::mutex> lock(mtx);
        count++;
    }

    int get() {
        std::lock_guard<std::mutex> lock(mtx);
        return count;
    }
};

int main() {
    SynchronizedCounter counter;
    std::vector<std::thread> threads;

    for (int i = 0; i < 10; ++i) {
        threads.emplace_back([&counter]() {
            for (int j = 0; j < 1000; ++j) counter.increment();
        });
    }

    for (auto& t : threads) t.join();
    std::cout << "Final Counter Value: " << counter.get() << "\n";
    return 0;
}
{% endhighlight %}

---

### Challenge 18: Condition Variable Usage
**Why It's Challenging:** Demonstrates thread communication mechanics using `std::condition_variable` while handling spurious wakeups safely.

**Sample Task:** Implement a thread-safe Producer-Consumer queue.

{% highlight cpp %}
#include <iostream>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>

class BoundedBuffer {
    std::queue<int> buffer;
    size_t capacity;
    std::mutex mtx;
    std::condition_variable cv_produce;
    std::condition_variable cv_consume;

public:
    BoundedBuffer(size_t cap) : capacity(cap) {}

    void produce(int val) {
        std::unique_lock<std::mutex> lock(mtx);
        cv_produce.wait(lock, [this]() { return buffer.size() < capacity; });
        buffer.push(val);
        cv_consume.notify_one();
    }

    int consume() {
        std::unique_lock<std::mutex> lock(mtx);
        cv_consume.wait(lock, [this]() { return !buffer.empty(); });
        int val = buffer.front();
        buffer.pop();
        cv_produce.notify_one();
        return val;
    }
};

int main() {
    BoundedBuffer bb(5);
    std::thread producer([&]() { bb.produce(42); });
    std::thread consumer([&]() { std::cout << "Consumed: " << bb.consume() << "\n"; });

    producer.join();
    consumer.join();
    return 0;
}
{% endhighlight %}

---

### Challenge 19: Deadlock Prevention
**Why It's Challenging:** Shows how to lock multiple mutexes safely without causing circular wait conditions.

**Sample Task:** Transfer resources between two accounts safely using `std::scoped_lock` (C++17).

{% highlight cpp %}
#include <iostream>
#include <mutex>
#include <thread>

class Account {
public:
    int balance;
    std::mutex mtx;
    Account(int b) : balance(b) {}
};

void transfer(Account& from, Account& to, int amount) {
    // std::scoped_lock safely locks multiple mutexes without deadlocks
    std::scoped_lock lock(from.mtx, to.mtx);
    from.balance -= amount;
    to.balance += amount;
}

int main() {
    Account acc1(1000);
    Account acc2(500);

    std::thread t1(transfer, std::ref(acc1), std::ref(acc2), 200);
    std::thread t2(transfer, std::ref(acc2), std::ref(acc1), 100);

    t1.join();
    t2.join();

    std::cout << "Acc 1: " << acc1.balance << ", Acc 2: " << acc2.balance << "\n";
    return 0;
}
{% endhighlight %}

---

## Advanced Features of C++

### Challenge 20: Concept-Based Template Constraints
**Why It's Challenging:** Requires using C++20 concepts and standard type constraints to simplify template compilation errors.

**Sample Task:** Implement a concept-constrained serializable list structure.

{% highlight cpp %}
#include <iostream>
#include <concepts>
#include <string>

// Custom Concept defining serialization behavior
template <typename T>
concept Serializable = requires(T a) {
    { a.serialize() } -> std::same_as<std::string>;
};

template <Serializable T>
class SerializerWrapper {
    T item;
public:
    SerializerWrapper(T val) : item(val) {}
    void printSerialized() const {
        std::cout << "Serialized Data: " << item.serialize() << "\n";
    }
};

struct User {
    std::string name;
    std::string serialize() const { return "User:" + name; }
};

int main() {
    User user{"Alice"};
    SerializerWrapper<User> wrapper(user);
    wrapper.printSerialized();
    return 0;
}
{% endhighlight %}

---

### Challenge 21: Compile-Time String Processing
**Why It's Challenging:** Uses `constexpr`, compile-time string views, and custom literals to process configuration keys during compilation.

**Sample Task:** Create a `constexpr` compile-time string literal parser that calculates character lengths at compile time.

{% highlight cpp %}
#include <iostream>
#include <string_view>

template <size_t N>
struct FixedString {
    char buf[N]{};
    constexpr FixedString(const char* str) {
        for (size_t i = 0; i < N; ++i) buf[i] = str[i];
    }
};

template <size_t N>
FixedString(const char (&)[N]) -> FixedString<N>;

constexpr size_t countUppercase(std::string_view str) {
    size_t count = 0;
    for (char c : str) {
        if (c >= 'A' && c <= 'Z') count++;
    }
    return count;
}

int main() {
    // Evaluated completely at compile time
    constexpr std::string_view config = "CONF_KEY_NAME";
    constexpr size_t uppercaseCount = countUppercase(config);

    static_assert(uppercaseCount == 13, "Compile-time validation failed");
    std::cout << "Uppercase letters (Compile-Time Verified): " << uppercaseCount << "\n";
    return 0;
}
{% endhighlight %}

---

## Technical Interview Summary Matrix

| Domain | Key Topics Evaluated | Core Language Features |
| :--- | :--- | :--- |
| **Language Fundamentals** | Universal references, `const` overloads, SFINAE. | `std::forward`, `std::enable_if_t`, `std::void_t`. |
| **Algorithms** | Graph search, lock-free state loops, dynamic interval merges. | `std::priority_queue`, `std::atomic`, `compare_exchange_weak`. |
| **Data Structures** | Custom bucket maps, doubly linked list eviction, raw pointers. | `std::hash`, splice mechanics, RAII nodes. |
| **OOP Design** | Polymorphic interfaces, policy strategies, operator dispatch. | Pure virtual functions (`= 0`), virtual destructors, template mixins. |
| **Memory Control** | Smart pointers, pool allocators, alignment arenas. | Reference tracking, `reinterpret_cast`, bump offsets. |
| **Multithreading** | Shared state locks, conditional notifications, deadlock avoidance. | `std::mutex`, `std::condition_variable`, `std::scoped_lock`. |
| **Modern Standards** | Concept constraints, compile-time parsing. | C++20 `concept`, `requires`, `constexpr`. |