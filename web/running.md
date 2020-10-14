# Room attendance per room

{% include vega.html %}

{% for room in site.data.rooms %}

## {{room.name}}

{% assign running_room_id = room.id %}
{% include plots/running_users.html %}

{% endfor %}
