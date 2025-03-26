---
layout: default
title: Tags
---

<h1>Tags</h1>

{% capture tags_list %}{% for tag in site.tags %}{{ tag[0] }}{% unless forloop.last %},{% endunless %}{% endfor %}{% endcapture %}
{% assign tags = tags_list | split: ',' | sort %}

<ul>
  {% for tag in tags %}
  <li>
    <a href="#{{ tag }}">{{ tag }}</a>
  </li>
  {% endfor %}
</ul>

{% for tag in tags %}
  <h2 id="{{ tag }}">{{ tag }}</h2>
  <ul>
    {% for post in site.tags[tag] %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
    {% endfor %}
  </ul>
{% endfor %}