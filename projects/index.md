---
title: Projects
permalink: /projects/
published: true
---
<div class="posts">
  {% for post in site.project %}
    <article class="post">
<div>
      <h1><a href="{{ site.baseurl }}{{ project.url }}">{{ project.title }}</a></h1>

      <div class="entry">
        {{ project.excerpt }}
      </div>

      <a href="{{ site.baseurl }}{{ project.url }}" class="read-more">Read More</a>
      
      </div>
    </article>
  {% endfor %}
</div>
