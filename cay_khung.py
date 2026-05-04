# cay_khung.py - Bao phu trach
# Yeu cau 7.1 (Prim) + Yeu cau 7.2 (Kruskal)

import heapq
from ve import ve_do_thi


def prim(g, dinh_bat_dau):
    """Tim cay khung nho nhat (MST) bang thuat toan Prim.
    Tra ve (list_canh_MST, tong_trong_so).
    list_canh_MST dang [(u, v, w), ...].
    """
    # Tap dinh da co trong cay (bat dau voi dinh_bat_dau)
    trong_cay = {dinh_bat_dau}
    canh_mst = []
    tong = 0

    # Priority queue: (trong_so, u, v) - cac canh tu trong_cay ra ngoai
    pq = []
    for v in g.neighbors(dinh_bat_dau):
        w = g[dinh_bat_dau][v].get('weight', 1)
        heapq.heappush(pq, (w, dinh_bat_dau, v))

    # Hien thi trang thai ban dau
    ve_do_thi(g,
              mau_dinh={dinh_bat_dau: 'green'},
              tieu_de=f"Prim - bat dau tu dinh {dinh_bat_dau}")

    # Lap den khi tat ca dinh deu trong cay
    while pq and len(trong_cay) < g.number_of_nodes():
        w, u, v = heapq.heappop(pq)

        # Neu v da trong cay roi thi bo qua canh nay
        if v in trong_cay:
            continue

        # Them canh (u, v) vao MST
        trong_cay.add(v)
        canh_mst.append((u, v, w))
        tong += w

        # To mau xanh la cho cac dinh va canh trong MST
        mau_canh = {(a, b): 'green' for a, b, _ in canh_mst}
        ve_do_thi(g,
                  mau_dinh={d: 'green' for d in trong_cay},
                  mau_canh=mau_canh,
                  tieu_de=f"Prim - them canh ({u},{v}) trong so {w}, tong = {tong}")

        # Push tat ca canh tu v ra ngoai cay
        for nb in g.neighbors(v):
            if nb not in trong_cay:
                wt = g[v][nb].get('weight', 1)
                heapq.heappush(pq, (wt, v, nb))

    return canh_mst, tong


# === DSU (Disjoint Set Union) cho Kruskal ===

def _tim(cha, x):
    """Tim goc cua tap chua x (co path compression)."""
    while cha[x] != x:
        cha[x] = cha[cha[x]]
        x = cha[x]
    return x


def _gop(cha, a, b):
    """Gop 2 tap. Tra ve True neu thanh cong, False neu da cung tap."""
    ra = _tim(cha, a)
    rb = _tim(cha, b)
    if ra == rb:
        return False
    cha[ra] = rb
    return True


def kruskal(g):
    """Tim cay khung nho nhat (MST) bang thuat toan Kruskal.
    Tra ve (list_canh_MST, tong_trong_so).
    """
    # Khoi tao DSU: moi dinh la 1 tap rieng
    cha = {n: n for n in g.nodes()}

    # Sap xep tat ca canh theo trong so tang dan
    danh_sach_canh = []
    for u, v in g.edges():
        w = g[u][v].get('weight', 1)
        danh_sach_canh.append((u, v, w))
    danh_sach_canh.sort(key=lambda e: e[2])

    canh_mst = []
    tong = 0

    # Hien thi trang thai ban dau
    ve_do_thi(g, tieu_de=f"Kruskal - sap xep {len(danh_sach_canh)} canh tang dan")

    # Duyet tung canh, neu khong tao chu trinh thi them vao MST
    for u, v, w in danh_sach_canh:
        if _gop(cha, u, v):
            # Khong tao chu trinh -> them vao MST
            canh_mst.append((u, v, w))
            tong += w
            mau_canh = {(a, b): 'green' for a, b, _ in canh_mst}
            ve_do_thi(g,
                      mau_canh=mau_canh,
                      tieu_de=f"Kruskal - them canh ({u},{v}) trong so {w}, tong = {tong}")
        else:
            # Tao chu trinh -> bo qua, to do tam thoi
            mau_canh = {(a, b): 'green' for a, b, _ in canh_mst}
            mau_canh[(u, v)] = 'red'
            ve_do_thi(g,
                      mau_canh=mau_canh,
                      tieu_de=f"Kruskal - bo canh ({u},{v}) vi tao chu trinh")

    return canh_mst, tong


# ===== TEST =====
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from do_thi import doc_tu_file

    g = doc_tu_file('samples/dothi1.txt')

    plt.figure()
    canh, tong = prim(g, 0)
    print("Prim:", canh)
    print("Tong:", tong)

    plt.figure()
    canh, tong = kruskal(g)
    print("Kruskal:", canh)
    print("Tong:", tong)

    plt.show()
