# duong_di.py - Bao (Dijkstra) + Quoc An (Bipartite)
# Yeu cau 3 (Tim duong di ngan nhat) + Yeu cau 5 (Kiem tra do thi 2 phia)

import heapq
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


# ===== TEST =====
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from do_thi import doc_tu_file

    g = doc_tu_file('samples/dothi1.txt')
    plt.figure()
    duong, kc = dijkstra(g, 0, 4)
    plt.show()
    print("Duong:", duong)
    print("Do dai:", kc)
