"""
src/app/domain/workflow/mappers.py

Converts between the domain Graph object and the plain dict shape
stored in workflow_versions.graph (JSONB). This is the one place that
knows about BOTH representations - kept in domain since it has no
actual infrastructure dependency, just dict<->dataclass translation.
"""
from app.domain.workflow.entities import Edge, Graph, Node, Position


def graph_to_dict(graph: Graph) -> dict:
    return {
        "nodes": [
            {
                "id": n.id,
                "type": n.type,
                "position": {"x": n.position.x, "y": n.position.y},
                "data": n.data,
            }
            for n in graph.nodes
        ],
        "edges": [
            {
                "id": e.id,
                "source": e.source,
                "target": e.target,
                **({"sourceHandle": e.source_handle} if e.source_handle is not None else {}),
                **({"targetHandle": e.target_handle} if e.target_handle is not None else {}),
            }
            for e in graph.edges
        ],
    }


def dict_to_graph(data: dict) -> Graph:
    nodes = [
        Node(
            id=n["id"],
            type=n["type"],
            position=Position(x=n["position"]["x"], y=n["position"]["y"]),
            data=n.get("data", {}),
        )
        for n in data.get("nodes", [])
    ]
    edges = [
        Edge(
            id=e["id"],
            source=e["source"],
            target=e["target"],
            source_handle=e.get("sourceHandle"),
            target_handle=e.get("targetHandle"),
        )
        for e in data.get("edges", [])
    ]
    return Graph(nodes=nodes, edges=edges)