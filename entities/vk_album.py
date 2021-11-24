from dataclasses import dataclass


@dataclass
class VkAlbum:
    author: str
    title: str
    album_id: int
    owner_id: int
    access_hash: str