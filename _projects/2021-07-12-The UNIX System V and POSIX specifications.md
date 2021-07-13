---
title: The UNIX System V and POSIX specifications
description: >-
  Some recent tasks at work highlighted some obvious gaps in my working
  knowledge of Linux inter-process communication (IPC). I spent some personal
  time brushing up on things I had used before and learning about some
  mechanisms that I had not used before.
layout: project_page
published: true
---

[![Benjamin Bannekat ](https://raw.githubusercontent.com/hamid-abbaszadeh/hamid-abbaszadeh.github.io/master/images/shared.jpg)](https://hamid-abbaszadeh.github.io/projects/The-UNIX-System-V-and-POSIX-specifications)

> Some recent tasks at work highlighted some obvious gaps in my working knowledge of Linux inter-process communication (IPC). I spent some personal time brushing up on things I had used before and learning about some mechanisms that I had not used before. I am not discussing pipes or sockets here; I am discussing message queues, semaphores, and shared memory. The System V and POSIX specifications have different APIs for using basically the same three IPC mechanisms. I am not exploring every nuance or feature of each API and I am not comparing performance. My goal was simply to demonstrate each IPC mechanism for each API in a set of very simple programs. I show the programs side by side where appropriate, but the code is also available in [here](https://github.com/hamid-abbaszadeh/Linux-inter-process-communication-IPC).
