# do_thi.py - Khanh An phu trach
# Yeu cau 2 (Luu do thi) + Yeu cau 6 (Chuyen doi 3 cach bieu dien)

import networkx as nx


def tao_do_thi(co_huong=False):
    """Tao do thi moi (rong).
    co_huong = True  -> do thi co huong (DiGraph)
    co_huong = False -> do thi vo huong (Graph)
    """
    if co_huong:
        return nx.DiGraph()
    return nx.Graph()


def doc_tu_file(duong_dan):
    """Doc do thi tu file ma tran ke.
    Dinh dang file:
        Dong 1: n co_huong   (vd: "5 0" -> 5 dinh, vo huong)
        n dong tiep theo: ma tran ke n x n, phan tu = trong so (0 = khong co canh)
    """
    with open(duong_dan, 'r') as f:
        # Doc dong dau: so dinh + co/khong co huong
        dong_dau = f.readline().split()
        n = int(dong_dau[0])
        co_huong = False
        if len(dong_dau) > 1 and dong_dau[1] == '1':
            co_huong = True

        # Tao do thi rong
        g = tao_do_thi(co_huong)

        # Them n dinh (danh so 0, 1, 2, ..., n-1)
        for i in range(n):
            g.add_node(i)

        # Doc ma tran ke va them canh
        for i in range(n):
            hang = f.readline().split()
            for j in range(n):
                trong_so = int(hang[j])
                if trong_so != 0:
                    g.add_edge(i, j, weight=trong_so)

        return g


def luu_ra_file(g, duong_dan):
    """Luu do thi ra file theo dinh dang ma tran ke."""
    danh_sach_dinh = list(g.nodes())
    n = len(danh_sach_dinh)
    co_huong = 1 if g.is_directed() else 0

    with open(duong_dan, 'w') as f:
        # Dong dau
        f.write(f"{n} {co_huong}\n")

        # n dong ma tran
        for i in range(n):
            hang = []
            for j in range(n):
                u = danh_sach_dinh[i]
                v = danh_sach_dinh[j]
                if g.has_edge(u, v):
                    w = g[u][v].get('weight', 1)
                    hang.append(str(w))
                else:
                    hang.append('0')
            f.write(' '.join(hang) + '\n')


def sang_ma_tran(g):
    """Tra ve (danh_sach_ten_dinh, ma_tran_2_chieu)."""
    danh_sach_dinh = list(g.nodes())
    n = len(danh_sach_dinh)

    # Khoi tao ma tran toan 0
    ma_tran = [[0] * n for _ in range(n)]

    # Duyet tung canh, dien trong so vao ma tran
    for u, v in g.edges():
        i = danh_sach_dinh.index(u)
        j = danh_sach_dinh.index(v)
        w = g[u][v].get('weight', 1)
        ma_tran[i][j] = w
        # Vo huong thi doi xung
        if not g.is_directed():
            ma_tran[j][i] = w

    return danh_sach_dinh, ma_tran


def sang_danh_sach_ke(g):
    """Tra ve dict {dinh: [(hang_xom, trong_so), ...]}."""
    ket_qua = {}
    for u in g.nodes():
        ds_hang_xom = []
        for v in g.neighbors(u):
            w = g[u][v].get('weight', 1)
            ds_hang_xom.append((v, w))
        ket_qua[u] = ds_hang_xom
    return ket_qua


def sang_danh_sach_canh(g):
    """Tra ve list [(u, v, trong_so), ...].
    Do thi vo huong: chi lay 1 chieu (khong trung).
    """
    ket_qua = []
    da_co = set()  # luu cac canh da them (cho do thi vo huong)

    for u, v in g.edges():
        if not g.is_directed():
            # Chuan hoa: cap dinh sap xep tang dan de tranh trung
            khoa = tuple(sorted([u, v]))
            if khoa in da_co:
                continue
            da_co.add(khoa)
        w = g[u][v].get('weight', 1)
        ket_qua.append((u, v, w))

    return ket_qua


# ===== TEST =====
# Chay file nay truc tiep de test: python do_thi.py
if __name__ == "__main__":
    g = doc_tu_file('samples/dothi1.txt')
    print("Dinh:", list(g.nodes()))
    print("Canh:", list(g.edges()))
    print()

    dinh, mt = sang_ma_tran(g)
    print("Ma tran ke:")
    print("Dinh:", dinh)
    for hang in mt:
        print(hang)
    print()

    print("Danh sach ke:")
    adj = sang_danh_sach_ke(g)
    for u in adj:
        print(f"  {u}: {adj[u]}")
    print()

    print("Danh sach canh:")
    for canh in sang_danh_sach_canh(g):
        print(f"  {canh}")
