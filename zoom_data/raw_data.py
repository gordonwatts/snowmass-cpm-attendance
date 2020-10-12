from datetime import datetime
from pathlib import Path
import pandas as pd


def load_zoom_data(file: Path):
    '''Load zoom meeting data from a csv file. This should be extracted from
    the ZOOM reporting interface.

    Args:
        file (Path): [description]
    '''
    # Get the raw data in
    header_info = pd.read_csv(file, nrows=1, parse_dates=['Start Time', 'End Time'])  # type: ignore
    meeting_info = pd.read_csv(file, skiprows=2, parse_dates=['Join Time', 'Leave Time'])  # type: ignore

    # And build the object
    return ZoomMeetingData(header_info['Meeting ID'][0], header_info['Topic'][0],
                           header_info['Start Time'][0], header_info['End Time'][0],
                           header_info['Duration (Minutes)'][0], header_info['Participants'][0],
                           meeting_info[['Name (Original Name)', 'Join Time', 'Leave Time']])


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
