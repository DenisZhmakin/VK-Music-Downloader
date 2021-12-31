from dataclasses import dataclass
from pathlib import Path


@dataclass
class VkSong:
    track_num: int
    artist: str
    album: str
    title: str
    track_code: str
    genre: str
    year: int
    url: str
