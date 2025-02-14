---
title: SearchEngine Application in C++
description: In this project i want to implement a mini search engine by Trie Algorithm
layout: project_page
published: true
---

[![Benjamin Bannekat ](https://raw.githubusercontent.com/hamid-abbaszadeh/hamid-abbaszadeh.github.io/master/images/trie.jpg)](https://hamid-abbaszadeh.github.io/projects/SearchEngine-Application-in-C++)

> For the corresponding Github repository click [here](https://github.com/hamid-abbaszadeh/MiniSearchEngine-CPP).

# Contents
- [Introduction](#introduction)
- Initializing Program Variables
  - Checking Arguments
  - Initialising Memory Size
- Initialising Structs
  - Map Initialisation
  - Explaining trie struct
  - Initialising the Trie
- Input Manager
 - Search functionality
   - Search per document
   - Search per word
    - Search Implementation Part1
    - Heap Implementation
    - Search Implementation Part2
    
  
# Introduction
Search Engines are powered by various algorithms.For the past few decades, people from all around the world were sharing, posting and gaining information through the Internet. So we need technology to help us effectively search for the information we need. Thankfully we have it, and we call it a  **Search Engine**. In this project i want to implement a mini search engine by _**Trie Algorithm**_.
[Trie](http://en.wikipedia.org/wiki/Trie) is an efficient information retrieval data structure. Using Trie, search complexities can be brought to optimal limit (key length). If we store keys in binary search tree, a well balanced BST will need time proportional to **M * log N**, where M is maximum string length and N is number of keys in tree. Using Trie, we can search the key in **O(M)** time.
 
 ![](       )
