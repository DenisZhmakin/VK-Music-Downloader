from dataclasses import dataclass


@dataclass
class VkAlbum:
    artist: str
    title: str
    genre: str
    year: str
    cover_url: str
    cover_path: Path
    album_path: Path
    album_id: int
    owner_id: int
    access_hash: str