from datetime import datetime
from typing import List, Dict
from zoom_data import ZoomMeetingData
from collections import defaultdict


def accumulated_attendance(meetings: List[ZoomMeetingData]) -> Dict[datetime, int]:
    '''Given a list of meetings, create accumulated attendance information. Shows, by the minute,
    the number of unique people that show up in the room.

    Useful to understand total number of unique people joining a room accross a meeting.

    Args:
        meetings (List[ZoomMeetingData]): The list of zoom meetings. They are all considered together,
        and unique people are considered unique accross all rooms.
    '''
    already_seen = set()
    joining = defaultdict(int)
    for zm in meetings:
        for index, row in zm.coming_and_going.iterrows():
            name = row.Name
            if name not in already_seen:
                already_seen.add(name)
                joining[row.Join] += 1

    running_total = dict(joining)
    count = 0
    for k in sorted(running_total.keys()):
        count += running_total[k]
        running_total[k] = count

    return running_total


def running_attendance(meetings: List[ZoomMeetingData]) -> Dict[datetime, int]:
    '''Given a list of meetings, create the number of people in the meeting as a function
    of time.

    Useful to understand the number of people joining in rooms at any one time.

    Args:
        meetings (List[ZoomMeetingData]): List of meetings to accumulate

    Returns:
        Dict[datetime, int]: List of times and the number of people in the room at
        each of those times.
    '''
    joining = defaultdict(int)
    leaving = defaultdict(int)
    for zm in meetings:
        for index, row in zm.coming_and_going.iterrows():
            joining[row.Join] += 1
            leaving[row.Leave] -= 1

    all_keys = sorted(set(list(joining.keys()) + list(leaving.keys())))

    running_attendance = defaultdict(int)
    count = 0
    for k in all_keys:
        if k in joining:
            count += joining[k]
        if k in leaving:
            count += leaving[k]
        running_attendance[k] = count

    return running_attendance
