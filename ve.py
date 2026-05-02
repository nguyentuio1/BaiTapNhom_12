import matplotlib.pyplot as plt
import networkx as nx

# Biến global lưu vị trí đỉnh
_vi_tri = None


def reset_vi_tri():
    global _vi_tri
    _vi_tri = None


def ve_do_thi(g, mau_dinh=None, mau_canh=None, tieu_de=""):
    global _vi_tri

    # Nếu không truyền màu thì dùng dict rỗng
    mau_dinh = mau_dinh or {}
    mau_canh = mau_canh or {}

    # Tạo vị trí đỉnh (cố định)
    if _vi_tri is None or set(_vi_tri.keys()) != set(g.nodes()):
        _vi_tri = nx.spring_layout(g, seed=42)

    # Màu đỉnh
    danh_sach_mau_dinh = [
        mau_dinh.get(node, "lightgray")
        for node in g.nodes()
    ]

    # Màu cạnh
    danh_sach_mau_canh = []
    for u, v in g.edges():
        danh_sach_mau_canh.append(
            mau_canh.get((u, v), mau_canh.get((v, u), "gray"))
        )

    # ===== VẼ ĐỒ THỊ =====
    if g.is_directed():
        nx.draw(
            g,
            _vi_tri,
            with_labels=True,
            node_color=danh_sach_mau_dinh,
            edge_color=danh_sach_mau_canh,
            node_size=800,
            font_weight="bold",
            width=2,
            arrows=True,
            arrowsize=20
        )
    else:
        nx.draw(
            g,
            _vi_tri,
            with_labels=True,
            node_color=danh_sach_mau_dinh,
            edge_color=danh_sach_mau_canh,
            node_size=800,
            font_weight="bold",
            width=2
        )

    # Hiển thị trọng số nếu có
    weights = nx.get_edge_attributes(g, "weight")
    if weights:
        nx.draw_networkx_edge_labels(
            g,
            _vi_tri,
            edge_labels=weights
        )

    # Tiêu đề
    plt.title(tieu_de)

    # Tắt trục
    plt.axis("off")

    # Pause để hỗ trợ animation
    plt.pause(1.0)