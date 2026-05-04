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


# ============================================================
# YEU CAU 6 (BO SUNG): CHUYEN DOI QUA LAI 3 BIEU DIEN
# Ho tro ca do thi vo huong va co huong
# ============================================================

def tu_ma_tran(labels, ma_tran, co_huong=False):
    """Tao do thi tu ma tran ke."""
    g = tao_do_thi(co_huong)
    n = len(labels)
    for ten in labels:
        g.add_node(ten)
    for i in range(n):
        # Vo huong: chi duyet tam giac tren de tranh trung
        if co_huong:
            j_range = range(n)
        else:
            j_range = range(i + 1, n)
        for j in j_range:
            w = ma_tran[i][j]
            if w != 0:
                g.add_edge(labels[i], labels[j], weight=w)
    return g


def tu_danh_sach_ke(adj, co_huong=False):
    """Tao do thi tu danh sach ke.
    adj: dict {dinh: [(hang_xom, trong_so), ...]}
    """
    g = tao_do_thi(co_huong)
    for u in adj:
        g.add_node(u)
    da_co = set()
    for u, list_ke in adj.items():
        for v, w in list_ke:
            if v not in g.nodes():
                g.add_node(v)
            if not co_huong:
                khoa = tuple(sorted([u, v]))
                if khoa in da_co:
                    continue
                da_co.add(khoa)
            g.add_edge(u, v, weight=w)
    return g


def tu_danh_sach_canh(canh, co_huong=False):
    """Tao do thi tu danh sach canh.
    canh: list [(u, v, w), ...]
    """
    g = tao_do_thi(co_huong)
    for edge in canh:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) >= 3 else 1
        if u not in g.nodes():
            g.add_node(u)
        if v not in g.nodes():
            g.add_node(v)
        g.add_edge(u, v, weight=w)
    return g


# ===== 6 ham chuyen doi truc tiep giua 3 bieu dien =====

def chuyen_ma_tran_sang_danh_sach_ke(labels, ma_tran, co_huong=False):
    """Ma tran ke -> Danh sach ke."""
    n = len(labels)
    ket_qua = {labels[i]: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            w = ma_tran[i][j]
            if w != 0:
                ket_qua[labels[i]].append((labels[j], w))
    return ket_qua


def chuyen_ma_tran_sang_danh_sach_canh(labels, ma_tran, co_huong=False):
    """Ma tran ke -> Danh sach canh."""
    n = len(labels)
    ket_qua = []
    for i in range(n):
        if co_huong:
            j_range = range(n)
        else:
            j_range = range(i + 1, n)
        for j in j_range:
            w = ma_tran[i][j]
            if w != 0:
                ket_qua.append((labels[i], labels[j], w))
    return ket_qua


def chuyen_danh_sach_ke_sang_ma_tran(adj, co_huong=False):
    """Danh sach ke -> Ma tran ke."""
    labels = sorted(adj.keys())
    n = len(labels)
    idx = {labels[i]: i for i in range(n)}
    ma_tran = [[0] * n for _ in range(n)]
    for u, list_ke in adj.items():
        for v, w in list_ke:
            if v in idx:
                ma_tran[idx[u]][idx[v]] = w
                if not co_huong:
                    ma_tran[idx[v]][idx[u]] = w
    return labels, ma_tran


def chuyen_danh_sach_ke_sang_danh_sach_canh(adj, co_huong=False):
    """Danh sach ke -> Danh sach canh."""
    ket_qua = []
    da_co = set()
    for u, list_ke in adj.items():
        for v, w in list_ke:
            if not co_huong:
                khoa = tuple(sorted([u, v]))
                if khoa in da_co:
                    continue
                da_co.add(khoa)
            ket_qua.append((u, v, w))
    return ket_qua


def chuyen_danh_sach_canh_sang_ma_tran(canh, co_huong=False, danh_sach_dinh=None):
    """Danh sach canh -> Ma tran ke.
    Neu khong cho danh_sach_dinh thi tu suy ra tu cac canh.
    """
    if danh_sach_dinh is None:
        all_dinh = set()
        for edge in canh:
            all_dinh.add(edge[0])
            all_dinh.add(edge[1])
        labels = sorted(all_dinh, key=lambda x: str(x))
    else:
        labels = list(danh_sach_dinh)
    n = len(labels)
    idx = {labels[i]: i for i in range(n)}
    ma_tran = [[0] * n for _ in range(n)]
    for edge in canh:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) >= 3 else 1
        ma_tran[idx[u]][idx[v]] = w
        if not co_huong:
            ma_tran[idx[v]][idx[u]] = w
    return labels, ma_tran


def chuyen_danh_sach_canh_sang_danh_sach_ke(canh, co_huong=False):
    """Danh sach canh -> Danh sach ke."""
    ket_qua = {}
    for edge in canh:
        u, v = edge[0], edge[1]
        w = edge[2] if len(edge) >= 3 else 1
        if u not in ket_qua:
            ket_qua[u] = []
        if v not in ket_qua:
            ket_qua[v] = []
        ket_qua[u].append((v, w))
        if not co_huong:
            ket_qua[v].append((u, w))
    return ket_qua


# ===== Cac ham parse text (cho UI nhap tay) =====

def parse_ma_tran(text):
    """Parse text dang ma tran (co header hoac khong) -> (labels, ma_tran)."""
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    if not lines:
        return [], []

    first = lines[0].split()

    # Kiem tra dong dau co phai labels (chu) hay so
    def la_so(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    co_header = not all(la_so(t) for t in first)

    if co_header:
        labels = first
        matrix_lines = lines[1:]
        ma_tran = []
        for ln in matrix_lines:
            parts = ln.split()
            # Neu so phan tu = n + 1 thi co label dau dong, bo phan tu dau
            if len(parts) == len(labels) + 1:
                parts = parts[1:]
            ma_tran.append([float(x) for x in parts])
    else:
        n = len(first)
        labels = [str(i) for i in range(n)]
        ma_tran = [[float(x) for x in ln.split()] for ln in lines]

    # Convert int-like floats to int cho dep
    ma_tran = [[int(v) if float(v).is_integer() else v for v in row]
               for row in ma_tran]
    return labels, ma_tran


def parse_danh_sach_ke(text):
    """Parse text dang 'A: B(5), C(2)' -> dict {u: [(v, w), ...]}."""
    adj = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        parts = line.split(':', 1)
        u = parts[0].strip()
        rest = parts[1].strip()
        adj[u] = []
        if not rest:
            continue
        for item in rest.split(','):
            item = item.strip()
            if not item:
                continue
            # Co the co dang "v(w)" hoac chi "v"
            if '(' in item and ')' in item:
                v_part = item.split('(')
                v = v_part[0].strip()
                w_str = v_part[1].rstrip(')').strip()
                try:
                    w = float(w_str)
                    if w == int(w):
                        w = int(w)
                except ValueError:
                    w = 1
            else:
                v = item
                w = 1
            adj[u].append((v, w))
    return adj


def parse_danh_sach_canh(text):
    """Parse text dang 'A -- B (w=5)' hoac 'A B 5' -> list [(u, v, w), ...]."""
    canh = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Bo cac dau --, ->, (w=, )
        line = line.replace("->", " ").replace("--", " ")
        line = line.replace("(w=", " ").replace(")", " ")
        parts = line.split()
        if len(parts) < 2:
            continue
        u = parts[0]
        v = parts[1]
        if len(parts) >= 3:
            try:
                w = float(parts[2])
                if w == int(w):
                    w = int(w)
            except ValueError:
                w = 1
        else:
            w = 1
        canh.append((u, v, w))
    return canh


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
