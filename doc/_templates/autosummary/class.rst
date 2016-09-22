.. Copyright (c) 2005-2016, NumPy Developers
.. Licensed under the BSD License.
.. This file was adapted from NumPy 1.11.1.

{% extends "!autosummary/class.rst" %}

{% block methods %}
{% if methods %}
..
   HACK -- the point here is that we don't want this to appear in the output,
   but the autosummary should still generate the pages.
    .. autosummary::
        :toctree:
    {% for item in all_methods %}
        {%- if not item.startswith('_') or item in ['__call__'] %}
        {{ name }}.{{ item }}
        {%- endif -%}
    {%- endfor %}
{% endif %}
{% endblock %}

{% block attributes %}
{% if attributes %}
..
    HACK -- the point here is that we don't want this to appear in the output,
    but the autosummary should still generate the pages.
      .. autosummary::
         :toctree:
      {% for item in all_attributes %}
         {%- if not item.startswith('_') %}
         {{ name }}.{{ item }}
         {%- endif -%}
      {%- endfor %}
{% endif %}
{% endblock %}
