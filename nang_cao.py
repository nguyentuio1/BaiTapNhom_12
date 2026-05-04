# nang_cao.py - Binh An (leader) phu trach
# Yeu cau 7.3 (Ford-Fulkerson) + 7.4 (Fleury) + 7.5 (Hierholzer)
# 3 thuat toan nay kho cai tay -> dung ham co san cua NetworkX

import networkx as nx
from ve import ve_do_thi


def ford_fulkerson(g, nguon, dich):
    """Tim luong cuc dai tu nguon den dich.
    Dung ham nx.maximum_flow co san cua NetworkX (cai dat Edmonds-Karp).
    Tra ve (max_flow, flow_dict).
    flow_dict[u][v] = luong qua canh u->v.
    """
    # Goi ham co san cua NetworkX
    max_flow, flow_dict = nx.maximum_flow(g, nguon, dich, capacity='weight')

    # Chuan bi nhan canh dang "luong/dung_luong" va to mau canh co luong
    nhan_canh = {}
    mau_canh = {}
    for u in flow_dict:
        for v in flow_dict[u]:
            f = flow_dict[u][v]
            if f > 0 and g.has_edge(u, v):
                cap = g[u][v]['weight']
                nhan_canh[(u, v)] = f"{f}/{cap}"
                mau_canh[(u, v)] = 'blue'

    # Ve ket qua
    ve_do_thi(g,
              mau_canh=mau_canh,
              tieu_de=f"Max flow {nguon} -> {dich} = {max_flow}")

    return max_flow, flow_dict


def fleury(g, nguon=None):
    """Tim duong di Euler bang Fleury (dung NetworkX).
    Tra ve list canh [(u, v), ...] theo thu tu di. None neu khong co.
    """
    # Kiem tra dieu kien co duong Euler
    if not nx.has_eulerian_path(g):
        ve_do_thi(g, tieu_de="Khong co duong di Euler")
        return None

    # Lay duong di Euler
    duong = list(nx.eulerian_path(g, source=nguon))

    # Lay tat ca dinh trong duong
    cac_dinh = set()
    for u, v in duong:
        cac_dinh.add(u)
        cac_dinh.add(v)

    # To mau xanh la cho cac canh va dinh trong duong
    mau_canh = {(u, v): 'green' for u, v in duong}
    mau_dinh = {d: 'green' for d in cac_dinh}

    ve_do_thi(g,
              mau_dinh=mau_dinh,
              mau_canh=mau_canh,
              tieu_de=f"Duong di Euler: {len(duong)} canh")

    return duong


def hierholzer(g, nguon=None):
    """Tim chu trinh Euler bang Hierholzer (dung NetworkX).
    Tra ve list canh [(u, v), ...] theo thu tu chu trinh. None neu khong co.
    """
    # Kiem tra dieu kien co chu trinh Euler
    if not nx.is_eulerian(g):
        ve_do_thi(g, tieu_de="Khong co chu trinh Euler")
        return None

    # Lay chu trinh Euler
    chu_trinh = list(nx.eulerian_circuit(g, source=nguon))

    # To mau xanh la cho cac canh va dinh
    mau_canh = {(u, v): 'green' for u, v in chu_trinh}
    cac_dinh = set()
    for u, v in chu_trinh:
        cac_dinh.add(u)
        cac_dinh.add(v)
    mau_dinh = {d: 'green' for d in cac_dinh}

    ve_do_thi(g,
              mau_dinh=mau_dinh,
              mau_canh=mau_canh,
              tieu_de=f"Chu trinh Euler: {len(chu_trinh)} canh")

    return chu_trinh


# ===== TEST =====
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import networkx as nx_test
    from do_thi import doc_tu_file

    # Test Ford-Fulkerson tren do thi co huong
    print("=== Ford-Fulkerson ===")
    g = doc_tu_file('samples/dothi2.txt')
    plt.figure()
    flow, _ = ford_fulkerson(g, 0, 3)
    print("Max flow 0 -> 3:", flow)

    # Test Fleury va Hierholzer tren do thi co chu trinh Euler
    # (bowtie: 2 tam giac chia chung 1 dinh)
    print("\n=== Fleury & Hierholzer ===")
    g_euler = nx_test.Graph()
    g_euler.add_edges_from([(0, 1), (1, 2), (2, 0),
                             (2, 3), (3, 4), (4, 2)])

    plt.figure()
    duong = fleury(g_euler, 0)
    print("Fleury:", duong)

    plt.figure()
    chu_trinh = hierholzer(g_euler, 0)
    print("Hierholzer:", chu_trinh)

    plt.show()
