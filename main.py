import sqlite3
import networkx
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
                "</style>", "#loadingBar{display:none!important}</style>", 1
            )
        )


if __name__ == "__main__":
    main()
