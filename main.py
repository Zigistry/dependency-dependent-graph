import sqlite3
import networkx


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

if __name__ == "__main__":
    main()
