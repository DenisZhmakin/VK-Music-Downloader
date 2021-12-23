from dataclasses import dataclass
from pathlib import Path

@dataclass
class VkAlbum:
    artist: str
    title: str
    genre: str
    year: int
    cover_path: Path
    album_path: Path
    album_id: int
    owner_id: int
    access_hash: str