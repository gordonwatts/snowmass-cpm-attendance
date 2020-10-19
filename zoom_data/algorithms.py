from datetime import datetime
from typing import List, Dict, Set
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
    joining: Dict[datetime, List[str]] = defaultdict(list)
    for zm in meetings:
        for _, row in zm.coming_and_going.iterrows():
            joining[row.Join].append(row.Name)

    running_total = defaultdict(int)
    already_seen: Set[str] = set()
    count = 0
    for k in sorted(joining.keys()):
        for n in joining[k]:
            if n not in already_seen:
                already_seen.add(n)
                count += 1
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


def all_attendees(meetings: List[ZoomMeetingData]) -> List[str]:
    '''Return a list of all users that attended the meeting

    Args:
        meetings (List[ZoomMeetingData]): List of meetings to accumulate over

    Returns:
        List[str]: List of all users
    '''
    already_seen: Set[str] = set()
    for zm in meetings:
        for _, row in zm.coming_and_going.iterrows():
            already_seen.add(row.Name)

    return list(already_seen)
