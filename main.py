import sqlite3
import networkx
from pyvis.network import Network


def main():
    connection = sqlite3.connect("zigistry.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT repo_id, dependent FROM repo_dependents"
    )

    repo2repo_connection = cursor.fetchall()

    graph_builder = networkx.DiGraph()

    for repo_1, repo_2 in repo2repo_connection:
        graph_builder.add_edge(repo_2, repo_1)

    print(graph_builder)

    net = Network()

    net.from_nx(graph_builder)

    net.write_html("graph.html")

if __name__ == "__main__":
    main()
