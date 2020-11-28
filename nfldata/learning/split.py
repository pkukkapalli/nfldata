"""Splits videos up into frames using a fixed FPS."""
import os
import re
import subprocess

_VIDEO_FILENAME_REGEX = re.compile(
    r'([A-Za-z0-9\s]+)\s+vs\.\s+([A-Za-z0-9\s]+)\s+Week\s+([0-9]+)\s+Highlights\s+\_\s+NFL\s+([0-9]+).mp4$'  # pylint: disable=line-too-long
)


def split_videos(video_directory, output_directory):
    """Reads all of the videos in video_directory and outputs the frames into output_directory.

    The file will be skipped if the filename cannot be parsed according to _VIDEO_FILENAME_REGEX."""

    os.makedirs(output_directory, exist_ok=True)
    with os.scandir(video_directory) as files:
        for video in files:
            if not _is_video_file(video.name):
                print('Skipping non-video file: %s' % video.path)
                continue

            away, home, week, season = _parse_filename_as_video(video.name)

            output_file_format = os.path.join(
                output_directory,
                '{}_{}_{}_{}_%d.png'.format(away, home, week, season))

            print('Splitting %s' % video.path)
            subprocess.run([
                'ffmpeg', '-i', video.path, '-vf', 'fps=1', output_file_format
            ],
                           check=True)


def _is_video_file(filename):
    return _VIDEO_FILENAME_REGEX.match(filename) is not None


def _parse_filename_as_video(filename):
    match = _VIDEO_FILENAME_REGEX.match(filename)
    if match is None:
        raise RuntimeError('tried to parse non-video filename %s' % filename)
    return match.group(1, 2, 3, 4)
