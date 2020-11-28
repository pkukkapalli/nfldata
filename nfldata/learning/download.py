"""Downloads videos from a YouTube playlist for analysis."""

import os
import subprocess


def download_playlist(playlist_url, output_directory):
    """Downloads all of the videos from playlist_url into output_directory."""

    output_file_format = os.path.join(output_directory, '%(title)s.%(ext)s')
    subprocess.run([
        'youtube-dl', '-f', '(mp4)[height<=480]', '-o', output_file_format,
        playlist_url
    ],
                   check=True)
