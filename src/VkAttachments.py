from dataclasses import dataclass, field


@dataclass
class VkAttachments:
    photos: list[str] = field(default_factory=list)
    jokes: list[str] = field(default_factory=list)
    quotes: list[str] = field(default_factory=list)
    audios: list[str] = field(default_factory=list)
    mix: list[str] = field(default_factory=list)
    horny_photos: list[str] = field(default_factory=list)
    horny_jokes: list[str] = field(default_factory=list)
