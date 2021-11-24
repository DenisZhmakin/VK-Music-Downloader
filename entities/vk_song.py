from dataclasses import dataclass


@dataclass
class VkSong:
    number: int
    artist: str
    album: str
    title: str
    url: str