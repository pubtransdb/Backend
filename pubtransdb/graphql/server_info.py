import strawberry

from pubtransdb import __version__


@strawberry.type
class ServerInfo:
    @strawberry.field
    def version(self) -> str:
        return __version__
