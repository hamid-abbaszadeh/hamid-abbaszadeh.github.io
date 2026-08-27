---
layout: default
title: Architecture with Alias Templates
parent: Templates
nav_order: 6
---

# Architecture with Alias Templates
<span class="label label-blue">Modern C++</span> <span class="label label-purple">Architecture</span> <span class="label label-green">Performance</span>

Combining alias templates with policy-based design and lazy instantiation is a powerful way to write highly configurable, massive classes without suffering from code bloat. This is an excellent architectural use case for modern C++. {: .fs-5 .fw-300 }

## Table of Contents {: .no_toc .text-delta }
1. TOC
{:toc}

---

## The Core Concept: Lazy Instantiation

In C++, member functions of a class template are **lazily instantiated**. This means that even if a template class has 100 methods, the compiler will only generate machine code for the exact methods you actually call on that specific instantiation. 

By leveraging alias templates, we can create specific, domain-friendly configurations of a massive "Big Template" (like a complex data pipeline) while keeping binaries small and compile times fast.

---

## The "Big Template" Architecture

Let's examine a `DataPipeline` template configured with various policies. It includes multiple API groups, some of which might rely on heavy dependencies (like Machine Learning or Cloud SDKs).

{% highlight cpp %}
#include <iostream>
#include <string>
#include <vector>

// ---------------------------------------------------------
// 1. Dummy Policies (To make the template compile)
// ---------------------------------------------------------
struct InMemoryStorage { static void save(auto d) {} };
struct DatabaseStorage { static void save(auto d) {} };
struct StrictValidation { static bool check(auto d) { return true; } };
struct NoValidation { static bool check(auto d) { return true; } };
struct ConsoleLogger { static void log(auto msg) {} };
struct FileLogger { static void log(auto msg) {} };

// ---------------------------------------------------------
// 2. The "Big Template" with many APIs
// ---------------------------------------------------------
template <
    typename DataType, 
    typename StoragePolicy, 
    typename ValidationPolicy, 
    typename LoggingPolicy
>
class DataPipeline {
public:
    // API Group 1: Storage
    void save(const DataType& data) {
        StoragePolicy::save(data);
    }

    void batchSave(const std::vector<DataType>& dataList) {
        for (const auto& item : dataList) StoragePolicy::save(item);
    }

    // API Group 2: Validation
    bool isValid(const DataType& data) {
        return ValidationPolicy::check(data);
    }

    // API Group 3: Logging & Auditing
    void audit(const std::string& message) {
        LoggingPolicy::log(message);
    }

    // API Group 4: Heavy Analytics
    void performHeavyAnalytics() {
        // Because of lazy instantiation, this block of code is ONLY compiled
        // if a specific alias actually calls performHeavyAnalytics().
        // If it's never called, you don't pay the compile-time or binary size cost.
        std::cout << "Performing heavy ML analytics..." << std::endl;
    }

    // API Group 5: Network Sync
    void syncWithCloud() {
        std::cout << "Syncing with AWS..." << std::endl;
    }
};
{% endhighlight %}

---

## Creating Specific Tools with Alias Templates

Instead of forcing developers to type out these verbose template parameters, we use alias templates to create clean, domain-specific types.

{% highlight cpp %}
// ---------------------------------------------------------
// 3. The Alias Templates (Creating specific tools)
// ---------------------------------------------------------

// Alias 1: A fast, purely in-memory pipeline for temporary data.
// Leaves the DataType open for the user to specify.
template <typename T>
using FastLocalPipeline = DataPipeline<T, InMemoryStorage, NoValidation, ConsoleLogger>;

// Alias 2: A secure, strict database pipeline for production environments.
template <typename T>
using SecureProdPipeline = DataPipeline<T, DatabaseStorage, StrictValidation, FileLogger>;

// Alias 3: A fully concrete type (No open template parameters).
// Specifically for processing String Usernames in memory.
using UsernameValidator = DataPipeline<std::string, InMemoryStorage, StrictValidation, ConsoleLogger>;
{% endhighlight %}

---

## How Lazy Instantiation Saves You

Let's look at how these aliases are used in practice and why the compiler remains highly efficient.

{% highlight cpp %}
int main() {
    // 1. Using the Fast Pipeline
    FastLocalPipeline<int> quickMath;
    quickMath.save(42); 
    // COMPILER BEHAVIOR: Generates DataPipeline<int...>. 
    // It ONLY compiles the save() method. 
    // syncWithCloud() and performHeavyAnalytics() are completely ignored by the compiler.

    // 2. Using the Secure Pipeline
    SecureProdPipeline<double> financialData;
    financialData.save(100.50);
    financialData.isValid(100.50);
    financialData.syncWithCloud();
    // COMPILER BEHAVIOR: Generates a distinct DataPipeline<double...>.
    // It compiles save(), isValid(), and syncWithCloud().
    // performHeavyAnalytics() is still ignored.

    // 3. Using the specific non-template Alias
    UsernameValidator userCheck;
    userCheck.isValid("Admin");

    return 0;
}
{% endhighlight %}

<details>
<summary>Deep Dive: Key Architectural Benefits</summary>
<ul>
    <li><strong>Zero Overhead for Unused Code:</strong> You can stuff your <code>DataPipeline</code> template with database connectors, cloud syncs, and heavy math libraries. If a specific alias (like <code>FastLocalPipeline</code>) never calls those functions, the compiler never instantiates them, preventing dependencies from blowing up your binary size.</li>
    <li><strong>Semantic Meaning:</strong> <code>SecureProdPipeline&lt;Trade&gt;</code> is much easier for another developer to read and maintain than <code>DataPipeline&lt;Trade, DatabaseStorage, StrictValidation, FileLogger&gt;</code>.</li>
    <li><strong>Trivial Refactoring:</strong> If you decide to change the logging policy for all "Fast" pipelines across your entire codebase, you only need to change the single <code>using FastLocalPipeline</code> alias definition.</li>
</ul>
</details>