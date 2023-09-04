from __future__ import annotations

from dataclasses import dataclass, field, asdict

from prose.domain.clazz import Class
from prose.domain.method import Method

@dataclass
class File:
    name: str
    path: str
    clazz: Class | None = None
    methods: list[Method] = field(default_factory=list)

    @staticmethod
    def of(data: dict) -> File:
        file = File(**data)
        file.clazz = Class(**data["clazz"])
        file.methods = [Method(**x) for x in data["methods"]]
        return file

    def asdict(self) -> File:
        return asdict(self)
