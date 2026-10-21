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

    # 1. Sprawdzenie całego grafu
    is_eul = nx.is_eulerian(G)
    print(f"Czy cały graf jest eulerowski? {is_eul}")

    if is_eul:
        euler_subgraph = G
    else:

        # Pobranie bazy cykli z grafu
        cycles = nx.cycle_basis(G)

        # Wybieramy najdłuższy cykl
        longest_cycle = max(cycles, key=len)

        # Tworzymy listę krawędzi tworzących ten cykl
        edges = [
            (longest_cycle[i], longest_cycle[(i + 1) % len(longest_cycle)])
            for i in range(len(longest_cycle))
        ]

        # Tworzymy podgraf zawierający tylko te krawędzie
        euler_subgraph = G.edge_subgraph(edges).copy()

    # 2. Wyznaczenie ścieżki / cyklu Eulera
    if euler_subgraph and nx.is_eulerian(euler_subgraph):
        print("\n[SUKCES] Wyznaczono podgraf eulerowski:")
        print(f" - Liczba wierzchołków: {euler_subgraph.number_of_nodes()}")
        print(f" - Liczba krawędzi: {euler_subgraph.number_of_edges()}")

        circuit = list(nx.eulerian_circuit(euler_subgraph))
        print(f" - Długość cyklu Eulera: {len(circuit)} kroków")
        print(f" - Przykładowe kroki ścieżki: {circuit[:5]}")
        return euler_subgraph
    else:
        print("Nie udało się wyznaczyć podgrafu eulerowskiego.")
        return None


def maksymalny_przeplyw(G, source, target):
    if source not in G or target not in G:
        print("Błąd: Wskazane wierzchołki nie istnieją w grafie.")
        return


    G_directed = G.to_directed()
    for u, v in G_directed.edges():
        G_directed[u][v]["capacity"] = 1


    flow_value, flow_dict = nx.maximum_flow(
        G_directed, source, target, flow_func=nx.algorithms.flow.edmonds_karp
    )
    print(f"\n[Maksymalny Przepływ] Między {source} a {target}: {flow_value}")



if __name__ == "__main__":
    PLIK = "ca-GrQc.mtx"


    graf = wczytaj_graf_mtx(PLIK)

    start = int(input("podaj start najdłuższej ścieżki: "))
    stop = int(input("podaj koniec do najkrótszej scieżki: "))
    najkrotsza_sciezka(graf, start=start, stop=stop)


    analiza_eulerowska(graf)

    source = int(input("podaj początek maksymalnego przepływu: "))
    target = int(input("podaj koniec maksymalnego przepływu: "))
    maksymalny_przeplyw(graf, source=source, target=target)