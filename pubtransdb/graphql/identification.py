from typing import Generic, Sequence, TypeVar
from uuid import UUID

import strawberry


@strawberry.type(description="An entity with a unique id.")
class Node:
    id: UUID


_NodeType = TypeVar("_NodeType", bound=Node)


@strawberry.type(description="An edge connecting a node to another node.")
class Edge(Generic[_NodeType]):
    node: _NodeType


@strawberry.type(description="A collection of edges to other nodes.")
class Connection(Generic[_NodeType]):
    total_count: int
    edges: Sequence[Edge[_NodeType]]

    @strawberry.field
    def nodes(self) -> Sequence[_NodeType]:
        return [edge.node for edge in self.edges]
