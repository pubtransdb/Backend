from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint
from typing_extensions import LiteralString


class IDTypePrefixConstraint(CheckConstraint):
    def __init__(self, hex_char: LiteralString, **kwargs: Any) -> None:
        """Construct a CHECK constraint on the `id` field of the table.

        It requires the `UUID` to start with a 'type prefix' (provided as a hex character).
        This allows type information to be extracted from the UUID.
        """
        if hex_char not in tuple("0123456789abcdef"):
            raise ValueError(f"'{hex_char}' is not a hex character")
        sqltext = f"CAST(id AS char(1)) = '{hex_char}'"
        name = "id_startswith_type_prefix"
        super().__init__(sqltext, name, **kwargs)


class TypedUUIDFactory:
    def __init__(self, type_hex_char: str) -> None:
        if type_hex_char not in tuple("0123456789abcdef"):
            raise ValueError(f"'{type_hex_char}' is not a hex character")
        self.type_hex_char = type_hex_char

    def __call__(self) -> UUID:
        value = uuid4()
        res_hex = self.type_hex_char + value.hex[1:]
        return UUID(hex=res_hex)


def convert_table_name_char(ch: str):
    if ch.islower():
        return ch
    elif ch.isupper():
        return "_" + ch.lower()
    else:
        raise ValueError("Prohibited character in table's name", ch)
