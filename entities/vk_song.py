from dataclasses import dataclass


@dataclass
class VkSong:
    number: int
    cover: str
    track_code: str
    artist: str
    album: str
    title: str
    genre: str
    year: int
    url: str