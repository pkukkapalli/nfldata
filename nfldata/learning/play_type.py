"""Creates a model for learning to distinguish play types."""

import os
import pathlib
import random
import sqlite3

from fastai.data.block import DataBlock, CategoryBlock
from fastai.data.transforms import FuncSplitter
from fastai.metrics import error_rate
from fastai.vision.augment import Resize, aug_transforms
from fastai.vision.data import ImageBlock
from fastai.vision.learner import cnn_learner
from fastai.vision.models import resnet18
from nfldata.learning.video import video_from_frame_filename


def learn_play_type(labels_file,
                    epochs,
                    augment=False,
                    model=resnet18,
                    exclude_labels=None):
    """Creates a learner that learns how to recognize play types given a SQLite file holding labeled
    data."""

    if exclude_labels is None:
        exclude_labels = {}

    labels_database = sqlite3.connect(labels_file)

    batch_tfms = aug_transforms() if augment else None
    data_block = DataBlock(
        blocks=(ImageBlock, CategoryBlock),
        get_items=_get_items_function_factory(exclude_labels),
        splitter=FuncSplitter(_splitter_function_factory(labels_database)),
        get_y=_get_y_function_factory(labels_database),
        item_tfms=Resize(128),
        batch_tfms=batch_tfms)

    dls = data_block.dataloaders(labels_database)

    learn = cnn_learner(dls, model, metrics=error_rate)
    learn.fit(epochs)

    return learn


def _splitter_function_factory(labels_database):
    labeled_videos = {
        video_from_frame_filename(path.name)
        for path in _image_paths_from_labels_database(labels_database)
    }
    validation_video = random.choice(tuple(labeled_videos))

    def _split(path):
        path = pathlib.Path(path)
        video = video_from_frame_filename(path.name)
        return video == validation_video

    return _split


def _get_y_function_factory(labels_database):
    labels = _load_labels(labels_database)
    return lambda o: labels[pathlib.Path(o)]


def _get_items_function_factory(exclude_labels):
    exclude_labels = set(exclude_labels)

    def get_items(labels_database):
        labels = _load_labels(labels_database)
        images = _image_paths_from_labels_database(labels_database)
        return [i for i in images if labels[i] not in exclude_labels]

    return get_items


def _image_paths_from_labels_database(labels_database):
    labels = _load_labels(labels_database)

    images = []
    for path in labels.keys():
        if not os.path.exists(path):
            print('%s does not exist' % path)
        images.append(path)

    return images


def _load_labels(labels_database):
    return {
        pathlib.Path(k): v
        for k, v in labels_database.execute('SELECT path, label FROM labels')
    }
