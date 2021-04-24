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
   <p>{{ project.description }}</p>
  		<div class="entry">
        {{ project.excerpt }}
      	</div>
  
{% endfor %}