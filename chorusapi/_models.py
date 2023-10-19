from ._types import TierType, DifficultyType

from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class DirectLinks(BaseModel):
    ini: str | None = None
    chart: str | None = None
    song_mp3: str | None = Field(None, alias='song.mp3')
    song_ogg: str | None = Field(None, alias='song.ogg')
    album_jpg: str | None = Field(None, alias='album.jpg')
    archive: str | None = None

class Tiers(BaseModel):
    tier_band: int | None = None
    tier_guitar: int | None = None
    tier_bass: int | None = None
    tier_rhythm: int | None = None
    tier_drums: int | None = None
    tier_vocals: int | None = None
    tier_keys: int | None = None
    tier_guitargh1: int | None = None
    tier_bassgh1: int | None = None
        

class Difficulty(BaseModel):
    diff_guitar: int | None = None
    diff_bass: int | None = None
    diff_rhythm: int | None = None
    diff_drums: int | None = None
    diff_keys: int | None = None
    diff_guitargh1: int | None = None
    diff_bassgh1: int | None = None

class Has(BaseModel):
    has_forced: int | bool | None = Field(None, alias='hasForced')
    has_tap: int | bool | None = Field(None,alias='hasTap')
    has_sections: int | bool | None = Field(None,alias='hasSections')
    has_star_power: int | bool | None = Field(None,alias='hasStarPower')
    has_solo_sections: int | bool | None = Field(None,alias='hasSoloSections')
    has_stems: int | bool | None = Field(None,alias='hasStems')
    has_video: int | bool | None = Field(None,alias='hasVideo')
    has_lyrics: int | bool | None = Field(None,alias='hasLyrics')

class BaseSong(BaseModel):
    name: str | None = None
    artist: str | None = None
    album: str | None = None
    genre: str | None = None
    year: str | None = None
    charter: str | None = None 

class Song(BaseSong, Tiers, Difficulty, Has):
    id: int = Field(alias='id')
    length: int
    effective_length: int = Field(alias='effectiveLength')
    is_pack: bool = Field(alias='isPack')
    is_120: bool = Field(alias='is120')
    needs_renaming: bool = Field(alias='needsRenaming')
    is_folder: bool = Field(alias='isFolder')
    has_no_audio: bool = Field(alias='hasNoAudio')
    has_broken_notes: bool = Field(alias='hasBrokenNotes')
    has_background: bool = Field(alias='hasBackground')
    last_modified: datetime | None = Field(None, alias='lastModified')
    uploaded_at: datetime | None = Field(None, alias='uploadedAt')
    link: str
    direct_links: DirectLinks = Field(alias='directLinks', default_factory=DirectLinks)

class AdvancedSearch(BaseSong, Has):
    md5_checksum: str | None = Field(None, alias='md5')
    tier_band: TierType | None = None
    tier_guitar: TierType | None = None
    tier_bass: TierType | None = None
    tier_rhythm: TierType | None = None
    tier_drums: TierType | None = None
    tier_vocals: TierType | None = None
    tier_keys: TierType | None = None
    tier_guitargh1: TierType | None = None
    tier_bassgh1: TierType | None = None
    diff_guitar: list[DifficultyType] | int | None = None
    diff_bass: list[DifficultyType] | int | None = None
    diff_rhythm: list[DifficultyType] | int | None = None
    diff_drums: list[DifficultyType] | int | None = None
    diff_keys: list[DifficultyType] | int | None = None
    diff_guitargh1: list[DifficultyType] | int | None = None
    diff_bassgh1: list[DifficultyType] | int | None = None


    @field_validator('diff_guitar', 'diff_bass', 'diff_rhythm', 'diff_keys', 'diff_guitargh1', 'diff_bassgh1', mode='after')
    def validate_difficulties(cls, v: list[DifficultyType] | int | None) -> int:
        if isinstance(v, list) and v:
            return sum([difftype.value for difftype in v])
        elif isinstance(v, int):
            assert 1 <= v <= 15
            return v
        return None
    
    @field_validator('name', 'artist', 'album', 'genre', 'charter', 'md5_checksum')
    def _set_string_double_quote(cls, value: str) -> str:
        if value:
            value = f'"{value}"'
        return value

    def _as_search_value(self) -> str:
        as_dict = self.model_dump(exclude_defaults=True, by_alias=True)
        return ' '.join([f'{key}={value}' for key, value in as_dict.items()])