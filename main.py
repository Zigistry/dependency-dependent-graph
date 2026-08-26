import sqlite3
import networkx
import json
from pyvis.network import Network


def main():
    connection = sqlite3.connect("zigistry.db")
    cursor = connection.cursor()
    cursor.execute("SELECT repo_id, dependent FROM repo_dependents")

    repo2repo_connection = cursor.fetchall()

    graph_builder = networkx.DiGraph()

    for repo_1, repo_2 in repo2repo_connection:
        graph_builder.add_edge(repo_2, repo_1)

    print(graph_builder)

    graph_data = {"nodes": [], "edges": []}

    for node in graph_builder.nodes():
        graph_data["nodes"].append(
            {
                "id": node,
                "label": str(node),
            }
        )

    for source, target in graph_builder.edges():
        graph_data["edges"].append({"from": source, "to": target})

    with open("./graph.json", "w", encoding="utf-8") as json_file:
        json.dump(graph_data, json_file, indent=0)

    net = Network(
        width="100%",
        height="90vh",
        bgcolor="#1e1e1e",
        font_color="white",
        directed=True,
        # I am adding this because it was unnesecarily generating lib/ folder.
        cdn_resources="remote",
    )

    net.from_nx(graph_builder)

    net.add_node(
        "zigister",
        shape="image",
        image="zigister-finds-repos.svg",
        size=200,
        x=100,
        y=0,
        fixed=False,
        mass=5,
    )

    net.force_atlas_2based()

    net.options.physics.stabilization = False
    net.write_html("graph.html")

    with open("graph.html", "r+") as file:
        content = file.read()
        file.seek(0)
        file.write(
            content.replace(
                "</style>", "#loadingBar{display:none!important}\nhtml, body {padding:0; margin:0;}</style>", 1
            )
        )


if __name__ == "__main__":
    main()
