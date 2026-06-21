import os
import json
from models import Diem, Sinhvien, Monhoc, LopHocPhan

# 1. QUẢN LÝ SINH VIÊN
def save_sinhvien(ds_sinhvien, filename="sinhvien.json"):
    data = []
    current = ds_sinhvien.head
    while current is not None:
        sv = current.data
        data.append({"mssv": sv.mssv, "hoten": sv.hoten, "gioitinh": sv.gioitinh, "lop": sv.lop, "ngaysinh": sv.ngaysinh})
        current = current.next
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_sinhvien(ds_sinhvien, filename="sinhvien.json"):
    if not os.path.exists(filename): return
    with open(filename, "r", encoding="utf-8") as f:
        try: data = json.load(f)
        except json.JSONDecodeError: return
    for item in data:
        sv = Sinhvien(item["mssv"], item["hoten"], item["gioitinh"], item["lop"], item["ngaysinh"])
        ds_sinhvien.insert(sv)

# 2. QUẢN LÝ MÔN HỌC
def save_monhoc(ds_monhoc, filename="monhoc.json"):
    data = []
    current = ds_monhoc.head
    while current is not None:
        mh = current.data
        data.append({"ma_mon": mh.ma_mon, "ten_mon": mh.ten_mon, "so_tin_chi": mh.so_tin_chi, "khoa_vien": mh.khoa_vien, "ty_le_qt": mh.ty_le_qt})
        current = current.next
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_monhoc(ds_monhoc, filename="monhoc.json"):
    if not os.path.exists(filename): return
    with open(filename, "r", encoding="utf-8") as f:
        try: data = json.load(f)
        except json.JSONDecodeError: return
    for item in data:
        mh = Monhoc(item["ma_mon"], item["ten_mon"], item["so_tin_chi"], item["khoa_vien"], item.get("ty_le_qt", 30))
        ds_monhoc.append(mh)

# 3. QUẢN LÝ LỚP HỌC PHẦN (MỚI THÊM)
def save_lophocphan(ds_lhp, filename="lophocphan.json"):
    data = []
    current = ds_lhp.head
    while current is not None:
        l = current.data
        data.append({"ma_lhp": l.ma_lhp, "ma_mon": l.ma_mon, "hoc_ky": l.hoc_ky, "giang_vien": l.giang_vien})
        current = current.next
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_lophocphan(ds_lhp, filename="lophocphan.json"):
    if not os.path.exists(filename): return
    with open(filename, "r", encoding="utf-8") as f:
        try: data = json.load(f)
        except json.JSONDecodeError: return
    for item in data:
        ds_lhp.append(LopHocPhan(item["ma_lhp"], item["ma_mon"], item["hoc_ky"], item["giang_vien"]))

# 4. QUẢN LÝ ĐIỂM
def save_diem(ds_diem, filename="diem.json"):
    data = []
    current = ds_diem.head
    while current is not None:
        d = current.data
        data.append({
            "mssv": d.mssv, "hoten": d.hoten, "ma_mon": d.ma_mon, 
            "ma_lhp": d.ma_lhp, "hoc_ky": d.hoc_ky, 
            "diem_qt": d.diem_qt, "diem_ck": d.diem_ck
        })
        current = current.next
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_diem(ds_diem, filename="diem.json"):
    if not os.path.exists(filename): return
    with open(filename, "r", encoding="utf-8") as f:
        try: data = json.load(f)
        except json.JSONDecodeError: return
    for item in data:
        # Xử lý tương thích ngược nếu đọc nhầm file cũ
        ma_lhp = item.get("ma_lhp", "UNKNOWN")
        hoc_ky = item.get("hoc_ky", "UNKNOWN")
        diem_qt = item.get("diem_qt", item.get("diem_so", 0))
        diem_ck = item.get("diem_ck", item.get("diem_so", 0))
        d = Diem(item["mssv"], item["hoten"], item["ma_mon"], ma_lhp, hoc_ky, diem_qt, diem_ck)
        ds_diem.append(d)

# TRUNG TÂM ĐIỀU PHỐI TỔNG LỰC
def load_all_data(ds_sinhvien, ds_monhoc, ds_lhp, ds_diem):
    load_sinhvien(ds_sinhvien)
    load_monhoc(ds_monhoc)
    load_lophocphan(ds_lhp)
    load_diem(ds_diem)
    print("💾 [Hệ thống] Đã đồng bộ dữ liệu từ file JSON lên RAM thành công!")

def save_all_data(ds_sinhvien, ds_monhoc, ds_lhp, ds_diem, im_lang=False):
    save_sinhvien(ds_sinhvien)
    save_monhoc(ds_monhoc)
    save_lophocphan(ds_lhp)
    save_diem(ds_diem)
    if not im_lang:
        print("💾 [Hệ thống] Đã đóng gói và lưu an toàn toàn bộ dữ liệu xuống file JSON!")