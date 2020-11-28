"""Helps parse and handle videos and image frame files."""

import re

_FRAME_REGEX = re.compile(
    r'([A-Za-z0-9\s]+)_([A-Za-z0-9\s]+)_([0-9]+)_([0-9]+)_([0-9]+).png')


def video_from_frame_filename(filename):
    """Parse the video that we pulled this frame from."""

    match = _FRAME_REGEX.match(filename)
    if match is None:
        raise RuntimeError('tried to parse non-frame filename %s' % filename)
    away, home, week, season = match.group(1, 2, 3, 4)
    return _VideoKey(away, home, week, season)


class _VideoKey:
    """Defines a unique key for a video that we pulled image frames from.

    Useful to have as a key type for dictionaries.
    """

    def __init__(self, away, home, week, season):
        self.away = away
        self.home = home
        self.week = int(week)
        self.season = int(season)

    def _fields(self):
        return (self.away, self.home, self.week, self.season)

    def __hash__(self):
        return hash(self._fields())

    def __eq__(self, other):
        return self._fields() == other._fields()
