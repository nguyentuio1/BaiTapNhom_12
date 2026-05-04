# main.py - Binh An (leader) phu trach
# Tich hop tat ca cac module thanh ung dung Tkinter

import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

from do_thi import (
    doc_tu_file, luu_ra_file,
    sang_ma_tran, sang_danh_sach_ke, sang_danh_sach_canh,
)
from duyet import bfs, dfs
from duong_di import dijkstra, kiem_tra_2_phia
from cay_khung import prim, kruskal
from nang_cao import ford_fulkerson, fleury, hierholzer
from ve import ve_do_thi, reset_vi_tri


# Bien toan cuc luu do thi hien tai
g = None


def kiem_tra_do_thi():
    """Kiem tra co do thi chua, neu chua bao loi."""
    if g is None:
        messagebox.showwarning("Loi", "Hay mo file do thi truoc")
        return False
    return True


def lay_dinh(entry):
    """Lay so tu o nhap, hien bao loi neu khong phai so."""
    try:
        return int(entry.get())
    except ValueError:
        messagebox.showwarning("Loi", "Dinh phai la so nguyen")
        return None


# ===== Cac ham xu ly file =====

def mo_file():
    global g
    path = filedialog.askopenfilename(
        title="Chon file do thi",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not path:
        return
    try:
        g = doc_tu_file(path)
        reset_vi_tri()
        plt.figure()
        ve_do_thi(g, tieu_de="Do thi da mo")
        plt.show(block=False)
        messagebox.showinfo("OK", f"Da mo do thi co {g.number_of_nodes()} dinh, {g.number_of_edges()} canh")
    except Exception as e:
        messagebox.showerror("Loi doc file", str(e))


def luu_file():
    if not kiem_tra_do_thi():
        return
    path = filedialog.asksaveasfilename(
        title="Luu do thi",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if not path:
        return
    try:
        luu_ra_file(g, path)
        messagebox.showinfo("OK", f"Da luu vao:\n{path}")
    except Exception as e:
        messagebox.showerror("Loi luu file", str(e))


def hien_bieu_dien():
    if not kiem_tra_do_thi():
        return

    # Ma tran
    dinh, mt = sang_ma_tran(g)
    chuoi_mt = "MA TRAN KE:\n"
    chuoi_mt += "Dinh: " + str(dinh) + "\n"
    for hang in mt:
        chuoi_mt += str(hang) + "\n"

    # Danh sach ke
    chuoi_dsk = "\nDANH SACH KE:\n"
    adj = sang_danh_sach_ke(g)
    for u in adj:
        chuoi_dsk += f"  {u}: {adj[u]}\n"

    # Danh sach canh
    chuoi_dsc = "\nDANH SACH CANH:\n"
    for canh in sang_danh_sach_canh(g):
        chuoi_dsc += f"  {canh}\n"

    messagebox.showinfo("Bieu dien do thi", chuoi_mt + chuoi_dsk + chuoi_dsc)


# ===== Cac ham thuat toan =====

def chay_bfs():
    if not kiem_tra_do_thi():
        return
    nguon = lay_dinh(entry_nguon)
    if nguon is None:
        return
    if nguon not in g.nodes():
        messagebox.showwarning("Loi", f"Dinh {nguon} khong ton tai")
        return
    plt.figure()
    thu_tu = bfs(g, nguon)
    plt.show(block=False)
    messagebox.showinfo("BFS", f"Thu tu duyet: {thu_tu}")


def chay_dfs():
    if not kiem_tra_do_thi():
        return
    nguon = lay_dinh(entry_nguon)
    if nguon is None:
        return
    if nguon not in g.nodes():
        messagebox.showwarning("Loi", f"Dinh {nguon} khong ton tai")
        return
    plt.figure()
    thu_tu = dfs(g, nguon)
    plt.show(block=False)
    messagebox.showinfo("DFS", f"Thu tu duyet: {thu_tu}")


def chay_dijkstra():
    if not kiem_tra_do_thi():
        return
    nguon = lay_dinh(entry_nguon)
    dich = lay_dinh(entry_dich)
    if nguon is None or dich is None:
        return
    if nguon not in g.nodes() or dich not in g.nodes():
        messagebox.showwarning("Loi", "Dinh khong ton tai")
        return
    plt.figure()
    duong, kc = dijkstra(g, nguon, dich)
    plt.show(block=False)
    if duong:
        messagebox.showinfo("Dijkstra",
                            f"Duong ngan nhat:\n{duong}\nDo dai: {kc}")
    else:
        messagebox.showinfo("Dijkstra", "Khong co duong di")


def chay_2_phia():
    if not kiem_tra_do_thi():
        return
    plt.figure()
    ket_qua = kiem_tra_2_phia(g)
    plt.show(block=False)
    if ket_qua:
        messagebox.showinfo("Kiem tra 2 phia", "LA do thi 2 phia")
    else:
        messagebox.showinfo("Kiem tra 2 phia", "KHONG la do thi 2 phia")


def chay_prim():
    if not kiem_tra_do_thi():
        return
    nguon = lay_dinh(entry_nguon)
    if nguon is None:
        return
    if nguon not in g.nodes():
        messagebox.showwarning("Loi", f"Dinh {nguon} khong ton tai")
        return
    plt.figure()
    canh, tong = prim(g, nguon)
    plt.show(block=False)
    chuoi = "Canh trong MST:\n"
    for c in canh:
        chuoi += f"  {c}\n"
    chuoi += f"\nTong trong so: {tong}"
    messagebox.showinfo("Prim", chuoi)


def chay_kruskal():
    if not kiem_tra_do_thi():
        return
    plt.figure()
    canh, tong = kruskal(g)
    plt.show(block=False)
    chuoi = "Canh trong MST:\n"
    for c in canh:
        chuoi += f"  {c}\n"
    chuoi += f"\nTong trong so: {tong}"
    messagebox.showinfo("Kruskal", chuoi)


def chay_ford_fulkerson():
    if not kiem_tra_do_thi():
        return
    nguon = lay_dinh(entry_nguon)
    dich = lay_dinh(entry_dich)
    if nguon is None or dich is None:
        return
    if nguon not in g.nodes() or dich not in g.nodes():
        messagebox.showwarning("Loi", "Dinh khong ton tai")
        return
    if not g.is_directed():
        messagebox.showwarning("Loi", "Ford-Fulkerson can do thi co huong")
        return
    plt.figure()
    try:
        max_flow, _ = ford_fulkerson(g, nguon, dich)
        plt.show(block=False)
        messagebox.showinfo("Ford-Fulkerson", f"Max flow {nguon} -> {dich} = {max_flow}")
    except Exception as e:
        messagebox.showerror("Loi", str(e))


def chay_fleury():
    if not kiem_tra_do_thi():
        return
    plt.figure()
    duong = fleury(g)
    plt.show(block=False)
    if duong:
        messagebox.showinfo("Fleury", f"Duong di Euler ({len(duong)} canh):\n{duong}")
    else:
        messagebox.showinfo("Fleury", "Do thi khong co duong di Euler")


def chay_hierholzer():
    if not kiem_tra_do_thi():
        return
    plt.figure()
    chu_trinh = hierholzer(g)
    plt.show(block=False)
    if chu_trinh:
        messagebox.showinfo("Hierholzer", f"Chu trinh Euler ({len(chu_trinh)} canh):\n{chu_trinh}")
    else:
        messagebox.showinfo("Hierholzer", "Do thi khong co chu trinh Euler")


# ===== Tao giao dien Tkinter =====

root = tk.Tk()
root.title("Ung dung Do thi - Nhom 12")
root.geometry("400x650")

# Tieu de
tk.Label(root, text="UNG DUNG DO THI",
         font=("Arial", 14, "bold")).pack(pady=8)

# Khu vuc file
khung_file = tk.Frame(root)
khung_file.pack(pady=4)
tk.Button(khung_file, text="Mo file", command=mo_file, width=12).pack(side=tk.LEFT, padx=2)
tk.Button(khung_file, text="Luu file", command=luu_file, width=12).pack(side=tk.LEFT, padx=2)
tk.Button(khung_file, text="Hien bieu dien", command=hien_bieu_dien, width=14).pack(side=tk.LEFT, padx=2)

# Khu vuc nhap dinh
khung_nhap = tk.Frame(root)
khung_nhap.pack(pady=8)
tk.Label(khung_nhap, text="Dinh nguon:").grid(row=0, column=0, padx=4, pady=2)
entry_nguon = tk.Entry(khung_nhap, width=10)
entry_nguon.grid(row=0, column=1, padx=4, pady=2)
tk.Label(khung_nhap, text="Dinh dich:").grid(row=1, column=0, padx=4, pady=2)
entry_dich = tk.Entry(khung_nhap, width=10)
entry_dich.grid(row=1, column=1, padx=4, pady=2)

# Tieu de phan thuat toan
tk.Label(root, text="--- THUAT TOAN ---",
         font=("Arial", 10, "bold")).pack(pady=4)

# Cac nut thuat toan
danh_sach_thuat_toan = [
    ("BFS (duyet rong)", chay_bfs),
    ("DFS (duyet sau)", chay_dfs),
    ("Dijkstra (duong ngan nhat)", chay_dijkstra),
    ("Kiem tra do thi 2 phia", chay_2_phia),
    ("Prim (cay khung nho nhat)", chay_prim),
    ("Kruskal (cay khung nho nhat)", chay_kruskal),
    ("Ford-Fulkerson (luong cuc dai)", chay_ford_fulkerson),
    ("Fleury (duong Euler)", chay_fleury),
    ("Hierholzer (chu trinh Euler)", chay_hierholzer),
]

for ten, ham in danh_sach_thuat_toan:
    tk.Button(root, text=ten, command=ham, width=32).pack(pady=2)

# Chay vong lap su kien
root.mainloop()
