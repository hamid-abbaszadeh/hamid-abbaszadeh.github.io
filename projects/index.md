---
title: Projects
permalink: /projects/
published: true
---

  
{% for project in site.projects %}
  <h2>
      <a href="{{ project.url }}">
      {{ project.title }}
      </a>
  </h2>
  		<div class="entry">
        {{ project.excerpt }}
      	</div>
   <p>{{ project.description }}</p>
{% endfor %}