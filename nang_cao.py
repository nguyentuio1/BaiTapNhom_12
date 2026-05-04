# nang_cao.py - Binh An (leader) phu trach
# Yeu cau 7.3 (Ford-Fulkerson) + 7.4 (Fleury) + 7.5 (Hierholzer)
# PHIEN BAN V2: tu code thuat toan, khong dung ham co san cua NetworkX

from collections import deque, defaultdict
from ve import ve_do_thi


# ============================================================
# 7.3 FORD-FULKERSON (BFS tim duong tang - thuc chat la Edmonds-Karp)
# ============================================================

def ford_fulkerson(g, nguon, dich):
    """Tim luong cuc dai tu nguon den dich.
    Cai dat thuat toan Ford-Fulkerson tu code:
    - Lap: BFS tim duong tang -> day bottleneck -> cong vao tong luong.
    - Dung khi khong tim duoc duong tang nua.
    Tra ve (max_flow, flow_dict).
    """
    if nguon not in g.nodes() or dich not in g.nodes():
        ve_do_thi(g, tieu_de="Dinh nguon hoac dich khong ton tai")
        return 0, {}

    # Buoc 1: Khoi tao dung luong cua tung canh
    # Vi do thi vo huong khong co thuc te trong bai toan luong,
    # nhung neu nguoi dung truyen vao thi van xu ly: them ca canh nguoc lai
    dung_luong = {}
    for u, v in g.edges():
        w = g[u][v].get('weight', 1)
        dung_luong[(u, v)] = w
        if not g.is_directed():
            dung_luong[(v, u)] = w

    # Luu luong qua tung canh (mac dinh = 0)
    luong = {}
    danh_sach_dinh = list(g.nodes())

    # Ham con: BFS tim duong tang tu nguon den dich
    def tim_duong_tang():
        truoc = {nguon: None}  # luu dinh truoc do trong duong di
        q = deque([nguon])
        while q:
            u = q.popleft()
            for v in danh_sach_dinh:
                if v in truoc:
                    continue
                # Dung luong con lai cua canh u->v
                cap = dung_luong.get((u, v), 0)
                f = luong.get((u, v), 0)
                con_lai = cap - f
                if con_lai > 0:
                    truoc[v] = u
                    if v == dich:
                        return truoc
                    q.append(v)
        return None  # khong tim thay duong tang

    tong_luong = 0
    so_lan = 0

    ve_do_thi(g, tieu_de="Bat dau Ford-Fulkerson")

    # Buoc 2: Lap tim va day duong tang
    while True:
        truoc = tim_duong_tang()
        if truoc is None:
            break  # khong con duong tang -> ket thuc

        so_lan += 1

        # Truy nguoc duong tu dich ve nguon
        duong = []
        cur = dich
        while cur is not None:
            duong.append(cur)
            cur = truoc[cur]
        duong.reverse()

        # Tim bottleneck = dung luong nho nhat tren duong
        bottleneck = float('inf')
        for i in range(len(duong) - 1):
            u, v = duong[i], duong[i + 1]
            con_lai = dung_luong[(u, v)] - luong.get((u, v), 0)
            if con_lai < bottleneck:
                bottleneck = con_lai

        # Hien thi duong tang vua tim
        mau_canh = {(duong[i], duong[i + 1]): 'yellow'
                    for i in range(len(duong) - 1)}
        ve_do_thi(g,
                  mau_canh=mau_canh,
                  tieu_de=f"Lan {so_lan}: duong tang {' -> '.join(map(str, duong))}, bottleneck = {bottleneck}")

        # Day bottleneck don vi luong qua duong nay
        # Dong thoi them luong nguoc lai (de lan sau co the "rut bot")
        for i in range(len(duong) - 1):
            u, v = duong[i], duong[i + 1]
            luong[(u, v)] = luong.get((u, v), 0) + bottleneck
            luong[(v, u)] = luong.get((v, u), 0) - bottleneck

        tong_luong += bottleneck

    # Buoc 3: Dong goi flow_dict (chi giu luong duong)
    flow_dict = {}
    for (u, v), f in luong.items():
        if f > 0 and g.has_edge(u, v):
            if u not in flow_dict:
                flow_dict[u] = {}
            flow_dict[u][v] = f

    # Hien thi ket qua cuoi cung
    mau_canh_cuoi = {(u, v): 'blue'
                     for u in flow_dict
                     for v in flow_dict[u]
                     if flow_dict[u][v] > 0}
    ve_do_thi(g,
              mau_canh=mau_canh_cuoi,
              tieu_de=f"KET QUA: Max flow {nguon} -> {dich} = {tong_luong}")

    return tong_luong, flow_dict


# ============================================================
# Ham phu cho Fleury: kiem tra 1 canh co phai la "cau" khong
# ============================================================

def _so_dinh_toi_duoc_tu(graph, dinh_bat_dau, bo_canh=None):
    """DFS dem so dinh toi duoc tu dinh_bat_dau.
    bo_canh = (u, v) -> bo qua canh nay khi DFS.
    """
    da_tham = set([dinh_bat_dau])
    stack = [dinh_bat_dau]
    while stack:
        u = stack.pop()
        for v in graph.neighbors(u):
            # Bo qua canh bo_canh (khong di qua no)
            if bo_canh is not None:
                if (u, v) == bo_canh or (v, u) == bo_canh:
                    continue
            if v not in da_tham:
                da_tham.add(v)
                stack.append(v)
    return len(da_tham)


def _la_cau(graph, u, v):
    """Kiem tra canh (u, v) co phai cau khong.
    Cau = canh ma neu xoa di se lam do thi mat lien thong.
    Cach kiem tra: dem so dinh toi duoc tu u truoc va sau khi xoa canh.
    """
    # Neu u chi co 1 lang gieng (la v) thi khong tinh la cau
    if len(list(graph.neighbors(u))) <= 1:
        return False
    truoc = _so_dinh_toi_duoc_tu(graph, u)
    sau = _so_dinh_toi_duoc_tu(graph, u, bo_canh=(u, v))
    return sau < truoc


# ============================================================
# 7.4 FLEURY (Duong di Euler)
# ============================================================

def fleury(g, nguon=None):
    """Tim duong di Euler bang Fleury (tu code, khong dung NetworkX).
    Quy tac: tai moi dinh, chon canh khong phai cau.
    Neu chi co canh la cau thi buoc phai chon.
    Tra ve list canh [(u, v), ...] hoac None neu khong co duong Euler.
    """
    # Buoc 1: Kiem tra dieu kien co duong Euler
    # - Khong co dinh bac le -> co chu trinh Euler (xuat phat tu dau cung duoc)
    # - Co dung 2 dinh bac le -> co duong Euler bat dau tu 1 trong 2
    # - Khac -> khong co
    dinh_bac_le = []
    for n in g.nodes():
        if len(list(g.neighbors(n))) % 2 == 1:
            dinh_bac_le.append(n)

    if len(dinh_bac_le) not in (0, 2):
        ve_do_thi(g, tieu_de=f"Co {len(dinh_bac_le)} dinh bac le -> KHONG co duong Euler")
        return None

    # Neu co 2 dinh bac le, phai bat dau tu 1 trong 2
    if len(dinh_bac_le) == 2:
        if nguon not in dinh_bac_le:
            nguon = dinh_bac_le[0]

    if nguon is None:
        ds = list(g.nodes())
        if not ds:
            return None
        nguon = ds[0]

    if nguon not in g.nodes():
        return None

    # Buoc 2: Copy do thi (vi se xoa canh khi di qua)
    g_copy = g.copy()

    duong = []        # luu cac canh da di
    cur = nguon       # dinh hien tai

    ve_do_thi(g, mau_dinh={cur: 'yellow'},
              tieu_de=f"Fleury: bat dau tu {cur}")

    # Buoc 3: Lap chon canh ke tiep theo quy tac Fleury
    while True:
        ke = list(g_copy.neighbors(cur))
        if not ke:
            break  # het canh -> ket thuc

        # Tim canh KHONG phai cau de uu tien
        chon = None
        for v in ke:
            if not _la_cau(g_copy, cur, v):
                chon = v
                break

        # Neu tat ca deu la cau thi danh phai chon 1
        if chon is None:
            chon = ke[0]

        # Di canh (cur, chon) - them vao duong, xoa khoi do thi tam
        duong.append((cur, chon))
        g_copy.remove_edge(cur, chon)

        # Hien thi
        mau_canh = {(u, v): 'green' for u, v in duong}
        cac_dinh = set([nguon])
        for u, v in duong:
            cac_dinh.add(u)
            cac_dinh.add(v)
        mau_dinh = {d: 'green' for d in cac_dinh}
        mau_dinh[chon] = 'yellow'
        ve_do_thi(g, mau_dinh=mau_dinh, mau_canh=mau_canh,
                  tieu_de=f"Fleury: di canh ({cur},{chon})")

        cur = chon

    if not duong:
        return None

    # Hien thi ket qua cuoi cung
    mau_canh = {(u, v): 'green' for u, v in duong}
    cac_dinh = set()
    for u, v in duong:
        cac_dinh.add(u)
        cac_dinh.add(v)
    ve_do_thi(g,
              mau_dinh={d: 'green' for d in cac_dinh},
              mau_canh=mau_canh,
              tieu_de=f"KET QUA Fleury: {len(duong)} canh")

    return duong


# ============================================================
# 7.5 HIERHOLZER (Chu trinh Euler)
# ============================================================

def hierholzer(g, nguon=None):
    """Tim chu trinh Euler bang Hierholzer (tu code, khong dung NetworkX).
    Y tuong: dung stack, khi mot dinh con canh thi day vao,
    khi het canh thi pop ra duong ket qua.
    Tra ve list canh [(u, v), ...] hoac None neu khong co.
    """
    # Buoc 1: Kiem tra dieu kien chu trinh Euler:
    # MOI dinh phai co bac chan
    for n in g.nodes():
        if len(list(g.neighbors(n))) % 2 == 1:
            ve_do_thi(g, tieu_de=f"Dinh {n} bac le -> KHONG co chu trinh Euler")
            return None

    if g.number_of_edges() == 0:
        return None

    if nguon is None:
        nguon = list(g.nodes())[0]
    if nguon not in g.nodes():
        return None

    # Buoc 2: Xay dung danh sach ke (mutable) tu cac canh
    # Dung defaultdict(list) de them/xoa nhanh
    ke = defaultdict(list)
    for u, v in g.edges():
        ke[u].append(v)
        if not g.is_directed():
            ke[v].append(u)

    ve_do_thi(g, mau_dinh={nguon: 'yellow'},
              tieu_de=f"Hierholzer: bat dau tu {nguon}")

    # Buoc 3: Vong lap stack
    stack = [nguon]
    duong_dinh = []  # chuoi dinh ket qua (se dao nguoc cuoi cung)

    so_buoc = 0

    while stack:
        u = stack[-1]  # xem dinh cuoi stack (khong pop)
        if ke[u]:
            # Con canh -> di tiep
            v = ke[u].pop()  # lay 1 lang gieng
            # Voi do thi vo huong, xoa canh nguoc lai
            if not g.is_directed():
                if u in ke[v]:
                    ke[v].remove(u)
            stack.append(v)

            so_buoc += 1
            if so_buoc % 2 == 0:  # ve 2 buoc 1 lan cho do giat
                ve_do_thi(g,
                          mau_dinh={n: 'yellow' for n in stack},
                          tieu_de=f"Hierholzer: day {v} vao stack")
        else:
            # Het canh -> dua dinh nay vao ket qua, pop khoi stack
            duong_dinh.append(stack.pop())

    duong_dinh.reverse()  # duong dung phai dao nguoc

    # Buoc 4: Chuyen tu list dinh sang list canh
    if len(duong_dinh) < 2:
        return None
    duong_canh = [(duong_dinh[i], duong_dinh[i + 1])
                  for i in range(len(duong_dinh) - 1)]

    # Hien thi ket qua cuoi cung
    mau_canh = {}
    for u, v in duong_canh:
        mau_canh[(u, v)] = 'green'
    cac_dinh = set(duong_dinh)
    ve_do_thi(g,
              mau_dinh={d: 'green' for d in cac_dinh},
              mau_canh=mau_canh,
              tieu_de=f"KET QUA Hierholzer: chu trinh {len(duong_canh)} canh")

    return duong_canh


# ===== TEST =====
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import networkx as nx_test  # chi dung de tao do thi mau test
    from do_thi import doc_tu_file

    # Test Ford-Fulkerson tren do thi co huong
    print("=== Ford-Fulkerson ===")
    g = doc_tu_file('samples/dothi2.txt')
    plt.figure()
    flow, _ = ford_fulkerson(g, 0, 3)
    print("Max flow 0 -> 3:", flow)

    # Test Fleury va Hierholzer tren do thi bowtie (2 tam giac chia chung 1 dinh)
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
