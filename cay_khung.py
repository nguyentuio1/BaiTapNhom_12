# File: cay_khung.py
# Chức năng:
# - Tìm cây khung nhỏ nhất bằng Prim
# - Tìm cây khung nhỏ nhất bằng Kruskal
# - Trả về từng bước để app trực quan hóa thuật toán
def prim(vertices, edges, start):
    visited = set()
    mst = []
    steps = []
    total_weight = 0

    if not vertices:
        return [], 0, [], "Đồ thị chưa có đỉnh."

    if not edges:
        return [], 0, [], "Đồ thị chưa có cạnh."

    if start not in vertices:
        return [], 0, [], "Đỉnh bắt đầu không tồn tại trong đồ thị."

    visited.add(start)

    steps.append({
        "mo_ta": f"Bắt đầu thuật toán Prim từ đỉnh {start}",
        "mst": mst.copy(),
        "visited": visited.copy(),
        "total_weight": total_weight
    })

    while len(visited) < len(vertices):
        min_edge = None
        min_weight = float("inf")

        for u, v, w in edges:
            if u in visited and v not in visited:
                if w < min_weight:
                    min_weight = w
                    min_edge = (u, v, w)

            elif v in visited and u not in visited:
                if w < min_weight:
                    min_weight = w
                    min_edge = (v, u, w)

        if min_edge is None:
            return mst, total_weight, steps, "Đồ thị không liên thông nên không có cây khung nhỏ nhất."

        mst.append(min_edge)
        total_weight += min_edge[2]
        visited.add(min_edge[1])

        steps.append({
            "mo_ta": f"Chọn cạnh {min_edge[0]} - {min_edge[1]} có trọng số {min_edge[2]}",
            "mst": mst.copy(),
            "visited": visited.copy(),
            "total_weight": total_weight
        })

    return mst, total_weight, steps, "Prim chạy thành công."


def find(parent, vertex):
    if parent[vertex] != vertex:
        parent[vertex] = find(parent, parent[vertex])
    return parent[vertex]


def union(parent, u, v):
    root_u = find(parent, u)
    root_v = find(parent, v)

    if root_u != root_v:
        parent[root_v] = root_u


def kruskal(vertices, edges):
    mst = []
    steps = []
    total_weight = 0

    if not vertices:
        return [], 0, [], "Đồ thị chưa có đỉnh."

    if not edges:
        return [], 0, [], "Đồ thị chưa có cạnh."

    parent = {}

    for vertex in vertices:
        parent[vertex] = vertex

    edges_sorted = sorted(edges, key=lambda edge: edge[2])

    steps.append({
        "mo_ta": "Sắp xếp các cạnh theo trọng số tăng dần.",
        "mst": mst.copy(),
        "total_weight": total_weight
    })

    for u, v, w in edges_sorted:
        root_u = find(parent, u)
        root_v = find(parent, v)

        if root_u != root_v:
            mst.append((u, v, w))
            total_weight += w
            union(parent, u, v)

            steps.append({
                "mo_ta": f"Chọn cạnh {u} - {v} có trọng số {w}",
                "mst": mst.copy(),
                "total_weight": total_weight
            })

        else:
            steps.append({
                "mo_ta": f"Bỏ cạnh {u} - {v} vì nếu chọn sẽ tạo chu trình.",
                "mst": mst.copy(),
                "total_weight": total_weight
            })

        if len(mst) == len(vertices) - 1:
            break

    if len(mst) != len(vertices) - 1:
        return mst, total_weight, steps, "Đồ thị không liên thông nên không có cây khung nhỏ nhất."

    return mst, total_weight, steps, "Kruskal chạy thành công."