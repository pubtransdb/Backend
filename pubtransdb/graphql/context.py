from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session
from strawberry.fastapi import BaseContext
from strawberry.types import Info


@dataclass
class Context(BaseContext):
    db_session: Session

    @staticmethod
    def from_info(info: Info) -> Context:
        return info.context
