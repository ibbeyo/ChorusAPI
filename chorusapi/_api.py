from ._models import AdvancedSearch, Song
from ._consts import CHORUS_API_BASE_URL

from pathlib import Path

import httpx
import re

__all__ = ['count', 'latest', 'search', 'random', 'download']

def count() -> int:
    response = __call('/count')
    return int(response.text)

def latest(count: int = 1) -> list[Song]:
    latest = list()
    if count < 1 :
        return latest
    for n in range(0, count, 20):
        songs = __get_songs('/latest', params={'from': n})
        latest.extend(songs)
    return latest[:count]

def search(query: str | AdvancedSearch) -> list[Song]:
    if isinstance(query, AdvancedSearch):
        query = query._as_search_value()
    return __get_songs('/search', params={'query': query})

def random() -> list[Song]:
    return __get_songs('/random')

def download(songs: Song | list[Song], savedir: str | Path) -> None:
    _savedir = Path(savedir) if isinstance(savedir, str) else savedir
    assert _savedir.is_dir()

    if isinstance(songs, Song):
        songs = [songs]

    for song in songs:
        if archive := song.direct_links.archive:
            __get_chart(archive, _savedir)
        else:
            folder = song.artist + ' - ' + song.name
            newdir = _savedir.joinpath(folder)
            for link in song.direct_links.model_dump(exclude_none=True).values():
                __get_chart(link, newdir)

def __call(endpoint: str, *args, **kwargs) -> httpx.Response:
        url = CHORUS_API_BASE_URL + endpoint
        return httpx.get(url, *args, **kwargs)

def __get_songs(endpoint: str, *args, **kwargs) -> list[Song]:
        response = __call(endpoint, *args, **kwargs)
        songs = response.json()['songs']
        return [Song.model_validate(song) for song in songs]

def __get_chart(url: str, savedir: Path) -> Path:
    savedir.mkdir(parents=True, exist_ok=True)
    with httpx.stream('GET', url , follow_redirects=True) as response:
        content_disposition = response.headers['content-disposition']
        filename = re.findall("filename=\"(.+)\";", content_disposition)[0]
        savedir = savedir.joinpath(filename)
        with open(savedir, 'wb') as fs:
            for chunk in response.aiter_bytes(chunk_size=128):
                fs.write(chunk)
        return savedir