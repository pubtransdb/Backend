import strawberry

from .server_info import ServerInfo


@strawberry.type
class Query:
    @strawberry.field
    def server_info(self) -> ServerInfo:
        return ServerInfo()
