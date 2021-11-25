from dataclasses import dataclass


@dataclass
class VkAlbum:
    artist: str
    title: str
    album_id: int
    owner_id: int
    access_hash: str