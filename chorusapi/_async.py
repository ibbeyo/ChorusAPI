from ._models import AdvancedSearch, Song
from ._consts import CHORUS_API_BASE_URL

from pathlib import Path

import httpx
import re
import asyncio


class Async:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=None)

    async def count(self) -> int:
        response = await self.__call('/count')
        return int(response.text)

    async def latest(self, count: int = 1) -> list[Song]:
        latest = list()
        if count < 1 :
            return latest
        for n in range(0, count, 20):
            songs = await self.__get_songs('/latest', params={'from': n})
            latest.extend(songs)
        return latest[:count]

    async def search(self, query: str | AdvancedSearch) -> list[Song]:
        if isinstance(query, AdvancedSearch):
            query = query._as_search_value()
        return await self.__get_songs('/search', params={'query': query})

    async def random(self) -> list[Song]:
        return await self.__get_songs('/random')

    async def download(self, songs: Song | list[Song], savedir: str | Path) -> None:
        _savedir = Path(savedir) if isinstance(savedir, str) else savedir
        assert _savedir.is_dir()

        if isinstance(songs, Song):
            songs = [songs]
        
        tasks = []
        for song in songs:
            if archive := song.direct_links.archive:
                tasks.append(self.__get_chart(archive, _savedir))
            else:
                folder = song.artist + ' - ' + song.name
                newdir = _savedir.joinpath(folder)
                for link in song.direct_links.model_dump(exclude_none=True).values():
                    tasks.append(self.__get_chart(link, newdir))
                    
        await asyncio.gather(*tasks)

    async def __call(self, endpoint: str, *args, **kwargs) -> httpx.Response:
        url = CHORUS_API_BASE_URL + endpoint
        return await self._client.get(url, *args, **kwargs)

    async def __get_songs(self, endpoint: str, *args, **kwargs) -> list[Song]:
        response = await self.__call(endpoint, *args, **kwargs)
        songs = response.json()['songs']
        return [Song.model_validate(song) for song in songs]

    async def __get_chart(self, url: str, savedir: Path) -> Path:
        savedir.mkdir(parents=True, exist_ok=True)
        response = await self._client.get(url, follow_redirects=True)
        async with self._client.stream('GET', response.url) as response:
            content_disposition = response.headers['content-disposition']
            filename = re.findall("filename=\"(.+)\";", content_disposition)[0]
            savedir = savedir.joinpath(filename)
            with open(savedir, 'wb') as fs:
                async for chunk in response.aiter_bytes(chunk_size=128):
                    fs.write(chunk)
        return savedir