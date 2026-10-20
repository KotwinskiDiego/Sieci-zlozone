import networkx as nx



def wczytaj_graf_mtx(sciezka_do_pliku):
    G = nx.Graph()

    with open(sciezka_do_pliku, "r") as f:
        naglowek_przeczytany = False
        for line in f:
            line = line.strip()
            if line.startswith("%") or not line:
                continue

            czesci = line.split()


            if not naglowek_przeczytany and len(czesci) == 3:
                num_nodes_x, num_nodes_y, num_edges = map(int, czesci)
                print(
                    f"Nagłówek: {num_nodes_x} wierzchołków, {num_edges} krawędzi."
                )
                naglowek_przeczytany = True
                continue


            if len(czesci) >= 2:
                u, v = int(czesci[0]), int(czesci[1])
                if u != v:
                    G.add_edge(u, v)

    print(
        f"Wczytano graf: {G.number_of_nodes()} wierzchołków, {G.number_of_edges()} krawędzi."
    )
    return G



def najkrotsza_sciezka(G, start, stop):
    if start not in G or stop not in G:
        print("Błąd: Jednego z wierzchołków nie ma w grafie.")
        return

    if not nx.has_path(G, start, stop):
        print(f"Brak ścieżki między wierzchołkami {start} a {stop}.")
        return

    path = nx.shortest_path(G, source=start, target=stop)
    dlugosc = len(path) - 1
    print(
        f"\n[Najkrótsza Ścieżka] Między {start} a {stop} (długość: {dlugosc}):"
    )
    print(" -> ".join(map(str, path)))



def analiza_eulerowska(G):
    print("\n--- ANALIZA EULEROWSKA ---")


    is_eul = nx.is_eulerian(G)
    print(f"Czy cały graf jest eulerowski? {is_eul}")

    if not is_eul:
        print("Powód: Niektóre wierzchołki mają nieparzyste stopnie.")
        print(
            "Wyciąganie eulerowskiego podgrafu (zgodnie z treścią zadania)..."
        )


        even_degree_nodes = [node for node, deg in G.degree() if deg % 2 == 0]
        subgraph = G.subgraph(even_degree_nodes).copy()


        subgraph.remove_nodes_from(list(nx.isolates(subgraph)))


        if len(subgraph) > 0:
            largest_cc = max(nx.connected_components(subgraph), key=len)
            euler_subgraph = subgraph.subgraph(largest_cc).copy()

            if nx.is_eulerian(euler_subgraph):
                print(
                    f"Znaleziono eulerowski podgraf! ({euler_subgraph.number_of_nodes()} wierzchołków, {euler_subgraph.number_of_edges()} krawędzi)"
                )
                euler_circuit = list(nx.eulerian_circuit(euler_subgraph))
                print(
                    f"Przykładowa ścieżka/cykl eulerowski w podgrafie (pierwsze 5 kroków): {euler_circuit[:5]}..."
                )
            else:
                print("Podgraf po redukcji nie spełnia warunków spójności.")



def maksymalny_przeplyw(G, source, target):
    if source not in G or target not in G:
        print("Błąd: Wskazane wierzchołki nie istnieją w grafie.")
        return


    G_directed = G.to_directed()
    for u, v in G_directed.edges():
        G_directed[u][v]["capacity"] = 1

    try:
        flow_value, flow_dict = nx.maximum_flow(
            G_directed, source, target, flow_func=nx.algorithms.flow.edmonds_karp
        )
        print(f"\n[Maksymalny Przepływ] Między {source} a {target}: {flow_value}")
    except nx.NetworkXUnreachable:
        print(
            f"Wierzchołki {source} i {target} nie są połączone – przepływ wynosi 0."
        )



if __name__ == "__main__":
    PLIK = "ca-GrQc.mtx"


    graf = wczytaj_graf_mtx(PLIK)


    najkrotsza_sciezka(graf, start=1, stop=100)


    analiza_eulerowska(graf)


    maksymalny_przeplyw(graf, source=1, target=100)