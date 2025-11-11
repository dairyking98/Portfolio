---
title: Collection Posts
layout: page
permalink: /typewriters/collection-posts/
---

Machine pages and posts about my typewriter collection.

{% assign collection_posts = site.posts | where: 'category', 'Typewriters' | where_exp: "post", "post.tags contains 'my-collection'" %}
{% if collection_posts.size > 0 %}
<div class="posts-list">
    {% for post in collection_posts %}
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
<p>No collection posts yet. Check back soon!</p>
{% endif %}

<div class="typewriters-machine-list">
    <h2>Typewriter Machine Pages</h2>
    <ul>
        {% for typewriter in site.typewriters %}
        <li><a href="{{ typewriter.url | relative_url }}">{{ typewriter.title }}</a></li>
        {% endfor %}
    </ul>
</div>

