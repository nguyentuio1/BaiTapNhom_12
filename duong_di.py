# duong_di.py - Bao (Dijkstra) + Quoc An (Bipartite)
# Yeu cau 3 (Tim duong di ngan nhat) + Yeu cau 5 (Kiem tra do thi 2 phia)

import heapq
from collections import deque
from ve import ve_do_thi


def dijkstra(g, nguon, dich):
    """Tim duong di ngan nhat tu nguon den dich bang thuat toan Dijkstra.
    Tra ve (duong_di, do_dai).
    Neu khong co duong: tra ve (None, float('inf')).
    """
    # Khoi tao khoang cach: tat ca = vo cuc, rieng nguon = 0
    khoang_cach = {n: float('inf') for n in g.nodes()}
    khoang_cach[nguon] = 0

    # Dict luu dinh truoc do (de truy nguoc duong di)
    truoc = {}

    # Priority queue: (khoang_cach, dinh)
    pq = [(0, nguon)]
    da_xet = set()

    while pq:
        d, u = heapq.heappop(pq)

        # Neu da xet roi thi bo qua
        if u in da_xet:
            continue
        da_xet.add(u)

        # To vang cac dinh da xet de hien thi animation
        ve_do_thi(g,
                  mau_dinh={n: 'yellow' for n in da_xet},
                  tieu_de=f"Dijkstra - dang xet dinh {u} (d={d})")

        # Neu den dich roi thi dung
        if u == dich:
            break

        # Cap nhat khoang cach cho cac dinh ke
        for v in g.neighbors(u):
            if v in da_xet:
                continue
            w = g[u][v].get('weight', 1)
            kc_moi = khoang_cach[u] + w
            if kc_moi < khoang_cach[v]:
                khoang_cach[v] = kc_moi
                truoc[v] = u
                heapq.heappush(pq, (kc_moi, v))

    # Neu khong co duong den dich
    if khoang_cach[dich] == float('inf'):
        ve_do_thi(g, tieu_de=f"Khong co duong tu {nguon} den {dich}")
        return None, float('inf')

    # Truy nguoc duong di tu dich ve nguon
    duong = []
    cur = dich
    while cur != nguon:
        duong.append(cur)
        cur = truoc[cur]
    duong.append(nguon)
    duong.reverse()

    # To duong di mau xanh la
    canh_duong = {}
    for i in range(len(duong) - 1):
        canh_duong[(duong[i], duong[i + 1])] = 'green'

    ve_do_thi(g,
              mau_dinh={d: 'green' for d in duong},
              mau_canh=canh_duong,
              tieu_de=f"Duong ngan nhat {nguon} -> {dich}: {khoang_cach[dich]}")

    return duong, khoang_cach[dich]


def kiem_tra_2_phia(g):
    """Kiem tra do thi co phai la do thi 2 phia hay khong.
    BFS tu moi thanh phan lien thong, to mau xen ke 2 mau (0, 1).
    Neu gap 2 dinh ke cung mau -> KHONG la 2 phia.
    Tra ve True/False.
    """
    # Dict luu mau cua moi dinh: 0 hoac 1
    mau = {}

    # Duyet tat ca dinh (de xu ly do thi co nhieu thanh phan lien thong)
    for dinh_bat_dau in g.nodes():
        if dinh_bat_dau in mau:
            continue

        # BFS tu dinh chua duoc to mau
        mau[dinh_bat_dau] = 0
        hang_doi = deque([dinh_bat_dau])

        while hang_doi:
            u = hang_doi.popleft()
            for v in g.neighbors(u):
                if v not in mau:
                    # To mau nguoc voi mau cua u
                    mau[v] = 1 - mau[u]
                    hang_doi.append(v)
                elif mau[v] == mau[u]:
                    # Mau thuan: 2 dinh ke cung mau -> KHONG la 2 phia
                    ve_do_thi(g,
                              mau_dinh={u: 'red', v: 'red'},
                              tieu_de=f"Mau thuan tai canh ({u},{v}) - KHONG la 2 phia")
                    return False

    # Thanh cong: to mau ket qua (skyblue cho nhom 0, orange cho nhom 1)
    mau_dinh = {}
    for n in mau:
        if mau[n] == 0:
            mau_dinh[n] = 'skyblue'
        else:
            mau_dinh[n] = 'orange'

    ve_do_thi(g,
              mau_dinh=mau_dinh,
              tieu_de="LA do thi 2 phia (xanh = nhom 1, cam = nhom 2)")
    return True


# ===== TEST =====
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import networkx as nx
    from do_thi import doc_tu_file

    # Test Dijkstra
    g = doc_tu_file('samples/dothi1.txt')
    plt.figure()
    duong, kc = dijkstra(g, 0, 4)
    print("Duong:", duong)
    print("Do dai:", kc)

    # Test 2 phia: chu trinh chan -> True
    g1 = nx.Graph()
    g1.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
    plt.figure()
    print("Do thi chu trinh chan:", kiem_tra_2_phia(g1))

    # Test 2 phia: chu trinh le -> False
    g2 = nx.Graph()
    g2.add_edges_from([(0, 1), (1, 2), (2, 0)])
    plt.figure()
    print("Do thi chu trinh le:", kiem_tra_2_phia(g2))

    plt.show()
