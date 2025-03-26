---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults
title: Martin Schultheiß Blog
layout: default

---

## My Blog List

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
      <!-- Code removed for brevity -->
      {% assign excerptParts = post.excerpt | split: "<!-- excerpt-start -->" %}
      {{ excerptParts[1] | strip_newlines | truncatewords: 100 }}
    </li>
  {% endfor %}
</ul>


[back](./)