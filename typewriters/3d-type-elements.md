---
title: 3D Type Elements
layout: page
permalink: /typewriters/3d-type-elements/
---

3D printing projects related to typewriters, with documentation and GitHub links for each sub-project.

{% assign type_elements_posts = site.posts | where: 'category', 'Typewriters' | where_exp: "post", "post.tags contains '3d-type-elements'" %}
{% if type_elements_posts.size > 0 %}
<div class="posts-list">
    {% for post in type_elements_posts %}
    <article class="post-preview">
        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        <div class="post-meta">
            <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time>
            {% if post.tags %}
            <span class="tags">
                {% for tag in post.tags %}
                <a href="{{ site.baseurl }}/tag/{{ tag | slugify }}" class="tag">{{ tag }}</a>
                {% endfor %}
            </span>
            {% endif %}
        </div>
        {% if post.excerpt %}
        <p class="post-summary">{{ post.excerpt | strip_html | truncatewords: 30 }}</p>
        {% endif %}
        <a href="{{ post.url | relative_url }}" class="read-more">Read more →</a>
    </article>
    {% endfor %}
</div>
{% else %}
<p>No 3D type elements posts yet. Check back soon!</p>
{% endif %}

