---
layout: default
title: Design Patterns
parent: Design Patterns and Architectural Patterns
nav_order: 2
has_children: true
---

# Design Patterns & Threading Visualization

Interactive execution flow diagrams and concurrency pattern visualizers.

<span class="label label-blue">C++11</span>
<span class="label label-purple">Concurrency</span>
<span class="label label-green">Interactive</span>

---

## Table of Contents

1. TOC
{:toc}

---

## Interactive Visualization Suite

Below is the embedded interactive call-flow diagram loaded directly from your site assets directory.

<iframe
  src="{{ '/assets/html/mutex_lock_flow_diagrams.html' | relative_url }}"
  width="100%"
  height="820"
  style="border: 1px solid #1f2a36; border-radius: 6px; background: #0b0f14;">
</iframe>

---

## Verification & Troubleshooting Checklist

If you still see a 404 after replacing the code above:

* **File Location**: Ensure `mutex_lock_flow_diagrams.html` is located exactly at `assets/html/mutex_lock_flow_diagrams.html` in your project root (not inside `_site/` or `_includes/`).
* **Jekyll Front Matter in HTML**: If `mutex_lock_flow_diagrams.html` has YAML front matter (`---`) at the top, remove it so Jekyll copies the file as static HTML without transforming it.
* **Base URL Subpaths**: Using the `| relative_url` filter automatically prepends `baseurl` (e.g., `/My-Repo-Name/assets/...`) when hosted on GitHub Pages or custom project subpaths.