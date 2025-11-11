---
title: Typewriter Collection
layout: page
permalink: /typewriters/collection/
---

A comprehensive catalog of my typewriter collection, featuring detailed information about each machine in both list and pivot views.

{% if site.data.typewriters %}
<div class="typewriters-collection">
    <h2>Collection Overview</h2>
    <p>Total machines: {{ site.data.typewriters.size }}</p>
    
    <table class="typewriters-table">
        <thead>
            <tr>
                <th>Make</th>
                <th>Model</th>
                <th>Serial</th>
                <th>Year</th>
                <th>Type</th>
                <th>Location</th>
            </tr>
        </thead>
        <tbody>
            {% for tw in site.data.typewriters %}
            <tr>
                <td>{{ tw['Typewriter Brand'] | default: tw.make }}</td>
                <td>{{ tw.Model | default: tw.model }}</td>
                <td>{{ tw['Serial No'] | default: tw.serial }}</td>
                <td>{{ tw.Year | default: tw.year }}</td>
                <td>{{ tw['Electric/Manual'] | default: tw.type }}</td>
                <td>{{ tw.Location | default: tw.location }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% else %}
<p>Collection data is being loaded...</p>
{% endif %}

