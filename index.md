# Snowmass CPM Meeting Attendance

This site shows some basic statistics for the Snowmass CPM meeting.

- List of [rooms](rooms) that are included.

Note that the data extracted from ZOOM contains no timezone information, as a result some of the plots might be a little off until that is corrected for.

## New unique users as a function of time

{% include vega.html %}
{% include plots/unique_users.html %}

## How many people were attending at a given time

{% assign running_room_id = "" %}
{% include plots/running_users.html %}

[Breakdown by room](running)
