"""Creates an IPython GUI for labeling image data from videos."""

import os
import pathlib
import re
import sqlite3
from IPython.display import display
from ipywidgets import Button, Image, Label, HBox, VBox

_FRAME_REGEX = re.compile(
    r'([A-Za-z0-9\s]+)_([A-Za-z0-9\s]+)_([0-9]+)_([0-9]+)_([0-9]+).png')


class LabelingGui:  # pylint: disable=too-few-public-methods
    """Holds the state and widgets necessary to render and update the GUI for labeling data."""

    def __init__(self, directory_to_label, labels, output_labels_file=None):
        self._output_labels_file = output_labels_file if not None else 'labels.db'
        self._db = sqlite3.connect(self._output_labels_file)
        self._db.execute('''
            CREATE TABLE IF NOT EXISTS labels (path TEXT PRIMARY KEY, label TEXT)
        ''')
        self._db.commit()

        self._videos_to_frames = _group_video_frames(directory_to_label)
        self._videos = list(self._videos_to_frames.keys())
        self._frames_to_labels = self._frames_to_labels_from_file()
        self._current_video_index = 0
        self._current_frame_index = 0

        self._image_name = Label(value=self._current_frame_filepath())
        self._image_label = Label(value=self._label_for_current_frame())

        initial_image_data = None
        with open(self._current_frame_filepath(), 'rb') as image:
            initial_image_data = image.read()
        self._image = Image(value=initial_image_data)

        self._label_buttons = [Button(description=label) for label in labels]
        for button in self._label_buttons:

            def handle_button(_):
                self._label_current_frame(button.description)  # pylint: disable=cell-var-from-loop
                self._increment_frame()
                self._refresh_frame()

            button.on_click(handle_button)

        def handle_previous_unlabeled(_):
            self._decrement_frame_to_unlabeled()
            self._refresh_frame()

        self._previous_unlabeled_button = Button(
            description='Previous unlabeled')
        self._previous_unlabeled_button.on_click(handle_previous_unlabeled)

        def handle_previous(_):
            self._decrement_frame()
            self._refresh_frame()

        self._previous_button = Button(description='Previous')
        self._previous_button.on_click(handle_previous)

        def handle_next(_):
            self._increment_frame()
            self._refresh_frame()

        self._next_button = Button(description='Next')
        self._next_button.on_click(handle_next)

        def handle_next_unlabeled(_):
            self._increment_frame_to_unlabeled()
            self._refresh_frame()

        self._next_unlabeled_button = Button(description='Next unlabeled')
        self._next_unlabeled_button.on_click(handle_next_unlabeled)

    def display(self):
        """Draws the GUI onto the screen.

        Must be run from an IPython environment."""

        display(
            VBox([
                HBox([Label(value='Image Path:'), self._image_name]),
                HBox([Label(value='Label:'), self._image_label])
            ]))
        display(self._image)
        display(HBox(self._label_buttons))
        display(
            HBox([
                self._previous_unlabeled_button, self._previous_button,
                self._next_button, self._next_unlabeled_button
            ]))

    def _current_frame_filepath(self):
        return self._videos_to_frames[self._current_video()][
            self._current_frame_index]

    def _current_video(self):
        return self._videos[self._current_video_index]

    def _number_of_frames_in_current_video(self):
        return len(self._videos_to_frames[self._current_video()])

    def _label_current_frame(self, label):
        path = self._current_frame_filepath()
        self._frames_to_labels[path] = label
        self._db.execute('INSERT INTO labels VALUES (?, ?)', (path, label))
        self._db.commit()

    def _is_current_frame_labeled(self):
        return self._current_frame_filepath() in self._frames_to_labels

    def _label_for_current_frame(self):
        if not self._is_current_frame_labeled():
            return ''
        return self._frames_to_labels[self._current_frame_filepath()]

    def _on_first_frame(self):
        return self._current_frame_index == 0

    def _on_first_frame_of_first_video(self):
        return self._on_first_frame() and self._current_video_index == 0

    def _decrement_frame(self):
        if self._on_first_frame_of_first_video():
            return

        if self._on_first_frame():
            self._current_video_index -= 1
            self._current_frame_index = self._number_of_frames_in_current_video(
            ) - 1
        else:
            self._current_frame_index -= 1

    def _decrement_frame_to_unlabeled(self):
        self._decrement_frame()
        while self._is_current_frame_labeled(
        ) and not self._on_first_frame_of_first_video():
            self._decrement_frame()

    def _on_last_frame(self):
        return self._current_frame_index + 1 >= self._number_of_frames_in_current_video(
        )

    def _on_last_frame_of_last_video(self):
        return self._on_last_frame() and self._current_video_index + 1 >= len(
            self._videos)

    def _increment_frame(self):
        if self._on_last_frame_of_last_video():
            return

        if self._on_last_frame():
            self._current_frame_index = 0
            self._current_video_index += 1
        else:
            self._current_frame_index += 1

    def _increment_frame_to_unlabeled(self):
        self._increment_frame()
        while self._is_current_frame_labeled(
        ) and not self._on_last_frame_of_last_video():
            self._increment_frame()

    def _refresh_frame(self):
        self._image_name.value = self._current_frame_filepath()
        self._image_label.value = self._label_for_current_frame()
        with open(self._current_frame_filepath(), 'rb') as image:
            self._image.value = image.read()

    def _frames_to_labels_from_file(self):
        return dict(self._db.execute('SELECT path, label FROM labels'))


def _group_video_frames(directory_to_label):
    videos_to_frames = {}
    with os.scandir(directory_to_label) as files:
        for video in files:
            if not _is_video_frame_file(video.name):
                print('Skipping non-frame file: %s' % video.path)
                continue

            away, home, week, season, _ = _parse_filename_as_frame(video.name)
            key = _VideoKey(away, home, week, season)

            if key not in videos_to_frames:
                videos_to_frames[key] = []

            videos_to_frames[key].append(video.path)

    for frames in videos_to_frames.values():
        frames.sort(key=_frame_number_from_filepath)

    return videos_to_frames


def _is_video_frame_file(filename):
    return _FRAME_REGEX.match(filename) is not None


def _parse_filename_as_frame(filename):
    match = _FRAME_REGEX.match(filename)
    if match is None:
        raise RuntimeError('tried to parse non-frame filename %s' % filename)
    return match.group(1, 2, 3, 4, 5)


def _frame_number_from_filepath(filepath):
    path = pathlib.Path(filepath)
    _, _, _, _, frame = _parse_filename_as_frame(path.name)
    return int(frame)


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
