from collections import deque
from ve import ve_do_thi


# BFS (duyet theo chieu rong)
def bfs(g, dinh_bat_dau):
    da_tham = set()        # luu cac dinh da tham
    hang_doi = deque()     # hang doi
    ket_qua = []           # ket qua

    hang_doi.append(dinh_bat_dau)
    da_tham.add(dinh_bat_dau)

    while hang_doi:
        dinh = hang_doi.popleft()
        ket_qua.append(dinh)

        # to do cac dinh da tham, hien thi dinh dang xet o tieu de
        ve_do_thi(g,
                  mau_dinh={d: 'red' for d in da_tham},
                  tieu_de=f"BFS - dang tham dinh {dinh}")

        # duyet cac dinh ke theo thu tu tang dan
        for ke in sorted(g.neighbors(dinh)):
            if ke not in da_tham:
                da_tham.add(ke)
                hang_doi.append(ke)

    return ket_qua


# DFS (duyet theo chieu sau - de quy)
def dfs(g, dinh_bat_dau):
    da_tham = set()
    ket_qua = []

    def de_quy(dinh):
        da_tham.add(dinh)
        ket_qua.append(dinh)

        ve_do_thi(g,
                  mau_dinh={d: 'red' for d in da_tham},
                  tieu_de=f"DFS - dang tham dinh {dinh}")

        for ke in sorted(g.neighbors(dinh)):
            if ke not in da_tham:
                de_quy(ke)

    de_quy(dinh_bat_dau)
    return ket_qua
