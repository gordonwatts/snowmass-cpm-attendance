from pathlib import Path
from typing import List
from .raw_data import ZoomMeetingData, load_zoom_data


def load_all(dir: Path) -> List[ZoomMeetingData]:
    '''Load all the zoom csv files found in a particular directory, return a list.

    Args:
        dir (Path): Directory where the meetings are located

    Returns:
        List[ZoomMeetingData]: List of all zoom files loaded, one object per file.
    '''
    return [load_zoom_data(f) for f in dir.glob('*.csv') if f.is_file()]
