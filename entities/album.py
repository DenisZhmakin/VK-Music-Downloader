from dataclasses import dataclass


@dataclass
class VkAlbum:
    artist: str
    title: str
    cover: str
    genre: str
    year: str
    album_id: int
    owner_id: int
    access_hash: str