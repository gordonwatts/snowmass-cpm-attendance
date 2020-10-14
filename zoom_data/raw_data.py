from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import calendar


def load_zoom_data(file: Path):
    '''Load zoom meeting data from a csv file. This should be extracted from
    the ZOOM reporting interface.

    Args:
        file (Path): [description]
    '''
    # Get the raw data in
    try:
        header_info = pd.read_csv(file, nrows=1, parse_dates=['Start Time', 'End Time'])  # type: ignore
        meeting_info = pd.read_csv(file, skiprows=2, parse_dates=['Join Time', 'Leave Time'])  # type: ignore

        # The time shift
        shift = timedelta(hours=int(header_info['TM Shift'][0]))
        meeting_info['Join Time'] = meeting_info['Join Time'] + shift
        meeting_info['Leave Time'] = meeting_info['Leave Time'] + shift

        # And build the object
        return ZoomMeetingData(header_info['Meeting ID'][0], header_info['Topic'][0],
                               header_info['Start Time'][0], header_info['End Time'][0],
                               header_info['Duration (Minutes)'][0], header_info['Participants'][0],
                               meeting_info[['Name (Original Name)', 'Join Time', 'Leave Time']])

    except Exception as e:
        raise Exception(f'Failed while opening file {str(file)}') from e


class ZoomMeetingData:
    '''Raw information from a meeting, with raw list of people going
    in and out of the room.
    '''
    def __init__(self, meeting_id: int,
                 topic: str,
                 start_time: datetime, end_time: datetime,
                 total_minutes: int,
                 participants: int,
                 coming_and_going: pd.DataFrame
                 ):
        self._meeting_id = meeting_id
        self._topic = topic
        self._start_time = start_time
        self._end_time = end_time
        self._total_minutes = total_minutes
        self._participants = participants
        self._coming_and_going = coming_and_going

        self._coming_and_going.columns = ['Name', 'Join', 'Leave']

        # Extract the ID for the room
        if self._topic.startswith('CPM Breakout - Zoom'):
            self._id = 10 + int(self._topic[-2:])
        elif self._topic.startswith('Plenary '):
            day = self._topic.split(' ')[1]
            self._id = list(calendar.day_name).index(day)
        else:
            self._id = 0

    @property
    def id(self) -> int:
        '''Return the id for a particular room - a nice internal way of isolating things.

        Returns:
            int: The id of the room
        '''
        return self._id

    @property
    def coming_and_going(self) -> pd.DataFrame:
        '''Returns a panads DF of the coming and goings in a meeting. Columns are:

            - Name - The name of the person joining
            - Join - `datetime` of when they joined
            - Leave - `datetime` of when they left

        Returns:
            pd.DataFrame: The `pandas DataFrame` containing the join/leave information
            for each person.
        '''
        return self._coming_and_going

    @property
    def room_name(self) -> str:
        '''The name of the zoom room

        Returns:
            str: Name of the room
        '''
        return self._topic
