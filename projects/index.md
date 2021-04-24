---
title: Projects
permalink: /projects/
published: true
---
  {% for post in site.project %}
<div>
      <h1><a href="{{ site.baseurl }}{{ project.url }}">{{ project.title }}</a></h1>

      <div class="entry">
        {{ project.excerpt }}
      </div>

      <a href="{{ site.baseurl }}{{ project.url }}" class="read-more">Read More</a>
      
      </div>
  {% endfor %}
