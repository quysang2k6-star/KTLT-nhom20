from strutures import LinkedList
from models import Diem, Sinhvien, Monhoc, LopHocPhan

# ====================================================================
# NHÓM 1: HÀM TIỆN ÍCH TÍNH TOÁN (dùng chung CLI + GUI)
# ====================================================================

def chuyen_diem_he_4(diem_10):
    """Quy đổi điểm hệ 10 sang hệ 4 theo chuẩn đại học"""
    if diem_10 >= 8.5: return 4.0
    elif diem_10 >= 8.0: return 3.5
    elif diem_10 >= 7.0: return 3.0
    elif diem_10 >= 6.5: return 2.5
    elif diem_10 >= 5.5: return 2.0
    elif diem_10 >= 5.0: return 1.5
    elif diem_10 >= 4.0: return 1.0
    else: return 0.0

def quy_doi_xep_loai(cpa_4):
    """Xếp loại bằng cấp dựa trên CPA hệ 4"""
    if cpa_4 >= 3.6: return "Xuất sắc"
    elif cpa_4 >= 3.2: return "Giỏi"
    elif cpa_4 >= 2.5: return "Khá"
    elif cpa_4 >= 2.0: return "Trung bình"
    else: return "Yếu/Kém"

def tinh_cpa(mssv, ds_monhoc, ds_diem):
    """Tính tổng tín chỉ + CPA hệ 10 + CPA hệ 4 của một sinh viên."""
    tong_tc = 0
    tong_he10 = 0.0
    tong_he4 = 0.0
    ds_diem_sv = ds_diem.find_all("mssv", mssv)
    current = ds_diem_sv.head
    while current is not None:
        d = current.data
        mon = ds_monhoc.find("ma_mon", d.ma_mon)
        if mon is not None:
            tk10 = d.tinh_tong_ket(mon.ty_le_qt)
            tk4 = chuyen_diem_he_4(tk10)
            tong_tc += mon.so_tin_chi
            tong_he10 += tk10 * mon.so_tin_chi
            tong_he4 += tk4 * mon.so_tin_chi
        current = current.next
    cpa_10 = (tong_he10 / tong_tc) if tong_tc > 0 else 0.0
    cpa_4 = (tong_he4 / tong_tc) if tong_tc > 0 else 0.0
    return tong_tc, cpa_10, cpa_4


# ====================================================================
# NHÓM 2: HÀM TRUY XUẤT DỮ LIỆU (trả về list[dict] cho GUI)
# ====================================================================

def dem_so_node(ll):
    """Đếm số phần tử trong LinkedList."""
    n = 0
    cur = ll.head
    while cur is not None:
        n += 1
        cur = cur.next
    return n

def lay_danh_sach_sinhvien(ds_sinhvien):
    """Trả về list[dict] thông tin sinh viên cho GUI."""
    rows = []
    cur = ds_sinhvien.head
    while cur is not None:
        sv = cur.data
        rows.append({
            "MSSV": sv.mssv,
            "Họ và tên": sv.hoten,
            "Giới tính": sv.gioitinh,
            "Lớp": sv.lop,
            "Ngày sinh": sv.ngaysinh,
        })
        cur = cur.next
    return rows

def lay_danh_sach_monhoc(ds_monhoc):
    """Trả về list[dict] thông tin môn học cho GUI."""
    rows = []
    cur = ds_monhoc.head
    while cur is not None:
        mh = cur.data
        rows.append({
            "Mã môn": mh.ma_mon,
            "Tên môn": mh.ten_mon,
            "Tín chỉ": mh.so_tin_chi,
            "Khoa/Viện": mh.khoa_vien,
            "Tỉ lệ QT (%)": mh.ty_le_qt,
            "Tỉ lệ CK (%)": 100 - mh.ty_le_qt,
        })
        cur = cur.next
    return rows

def lay_danh_sach_lhp(ds_lhp):
    """Trả về list[dict] thông tin lớp học phần cho GUI."""
    rows = []
    cur = ds_lhp.head
    while cur is not None:
        l = cur.data
        rows.append({
            "Mã LHP": l.ma_lhp,
            "Mã môn": l.ma_mon,
            "Học kỳ": l.hoc_ky,
            "Giảng viên": l.giang_vien,
        })
        cur = cur.next
    return rows

def lay_thanh_vien_lhp(ma_lhp, ds_diem, ds_sinhvien):
    """Trả về list[dict] danh sách sinh viên đã đăng ký một LHP (sắp xếp theo tên)."""
    ket_qua = []
    ds_diem_lhp = ds_diem.find_all("ma_lhp", ma_lhp)
    ds_diem_lhp.sort_theo_ten()
    cur = ds_diem_lhp.head
    stt = 0
    while cur is not None:
        d = cur.data
        stt += 1
        sv = ds_sinhvien.find("mssv", d.mssv)
        ket_qua.append({
            "STT": stt,
            "MSSV": d.mssv,
            "Họ và tên": d.hoten,
            "Giới tính": sv.gioitinh if sv else "N/A",
            "Lớp sinh hoạt": sv.lop if sv else "N/A",
        })
        cur = cur.next
    return ket_qua

def lay_bang_diem_lhp(ma_lhp, ds_lhp, ds_monhoc, ds_diem):
    """
    Trả về (list[dict] bảng điểm, dtb: float, si_so: int) cho một LHP.
    Trả về (None, 0, 0) nếu LHP hoặc Môn học không tồn tại.
    """
    lhp = ds_lhp.find("ma_lhp", ma_lhp)
    if lhp is None:
        return None, 0, 0
    mon = ds_monhoc.find("ma_mon", lhp.ma_mon)
    if mon is None:
        return None, 0, 0

    ds_diem_lhp = ds_diem.find_all("ma_lhp", ma_lhp)
    rows = []
    tong_diem = 0.0
    si_so = 0
    cur = ds_diem_lhp.head
    while cur is not None:
        d = cur.data
        si_so += 1
        tk = d.tinh_tong_ket(mon.ty_le_qt)
        rows.append({
            "STT": si_so,
            "MSSV": d.mssv,
            "Họ và tên": d.hoten,
            "Điểm QT": d.diem_qt,
            "Điểm CK": d.diem_ck,
            "Tổng kết": round(tk, 2),
        })
        tong_diem += tk
        cur = cur.next

    dtb = tong_diem / si_so if si_so > 0 else 0.0
    return rows, dtb, si_so

def lay_bang_diem_ca_nhan(mssv, ds_sinhvien, ds_monhoc, ds_diem):
    """
    Trả về dict gồm:
      - sv: object Sinhvien (hoặc None)
      - diem_theo_hk: dict{hoc_ky -> list[dict]}
      - tong_tc, cpa_10, cpa_4
    """
    sv = ds_sinhvien.find("mssv", mssv)
    if sv is None:
        return {"sv": None, "diem_theo_hk": {}, "tong_tc": 0, "cpa_10": 0.0, "cpa_4": 0.0}

    ds_diem_sv = ds_diem.find_all("mssv", mssv)
    diem_theo_hk = {}
    cur = ds_diem_sv.head
    while cur is not None:
        d = cur.data
        mon = ds_monhoc.find("ma_mon", d.ma_mon)
        hk = d.hoc_ky
        if hk not in diem_theo_hk:
            diem_theo_hk[hk] = []
        tk10 = d.tinh_tong_ket(mon.ty_le_qt) if mon else 0.0
        diem_theo_hk[hk].append({
            "Mã LHP": d.ma_lhp,
            "Mã môn": d.ma_mon,
            "Tên môn": mon.ten_mon if mon else "N/A",
            "TC": mon.so_tin_chi if mon else 0,
            "Điểm QT": d.diem_qt,
            "Điểm CK": d.diem_ck,
            "Hệ 10": round(tk10, 2),
            "Hệ 4": round(chuyen_diem_he_4(tk10), 2) if mon else 0.0,
        })
        cur = cur.next

    tong_tc, cpa_10, cpa_4 = tinh_cpa(mssv, ds_monhoc, ds_diem)
    return {"sv": sv, "diem_theo_hk": diem_theo_hk, "tong_tc": tong_tc, "cpa_10": cpa_10, "cpa_4": cpa_4}

def lay_bang_xep_hang(ds_sinhvien, ds_monhoc, ds_diem):
    """Trả về list[dict] xếp hạng toàn sinh viên theo CPA hệ 4 giảm dần."""
    bang = []
    cur = ds_sinhvien.head
    while cur is not None:
        sv = cur.data
        tong_tc, cpa_10, cpa_4 = tinh_cpa(sv.mssv, ds_monhoc, ds_diem)
        bang.append({
            "Hạng": 0,
            "MSSV": sv.mssv,
            "Họ tên": sv.hoten,
            "TC tích lũy": tong_tc,
            "CPA Hệ 10": round(cpa_10, 2),
            "CPA Hệ 4": round(cpa_4, 2),
            "Xếp loại": quy_doi_xep_loai(cpa_4) if tong_tc > 0 else "Chưa có điểm",
        })
        cur = cur.next
    bang.sort(key=lambda x: x["CPA Hệ 4"], reverse=True)
    for i, row in enumerate(bang):
        row["Hạng"] = i + 1
    return bang

def lay_danh_sach_chon_sv(ds_sinhvien):
    """Trả về list[str] dạng 'MSSV - Họ tên' cho selectbox."""
    result = []
    cur = ds_sinhvien.head
    while cur is not None:
        sv = cur.data
        result.append(f"{sv.mssv} - {sv.hoten}")
        cur = cur.next
    return result

def lay_danh_sach_chon_lhp(ds_lhp):
    """Trả về list[str] dạng 'MaLHP - MaMon (HocKy)' cho selectbox."""
    result = []
    cur = ds_lhp.head
    while cur is not None:
        l = cur.data
        result.append(f"{l.ma_lhp} - {l.ma_mon} ({l.hoc_ky})")
        cur = cur.next
    return result

def lay_diem_hien_tai(mssv, ma_lhp, ds_diem):
    """Trả về object Diem hiện tại của sv trong lhp, hoặc None nếu chưa có."""
    ds_diem_sv = ds_diem.find_all("mssv", mssv)
    cur = ds_diem_sv.head
    while cur is not None:
        if cur.data.ma_lhp == ma_lhp:
            return cur.data
        cur = cur.next
    return None

def lay_thong_tin_lhp_va_mon(ma_lhp, ds_lhp, ds_monhoc):
    """Trả về (lhp, mon) hoặc (lhp, None) hoặc (None, None)."""
    lhp = ds_lhp.find("ma_lhp", ma_lhp)
    if lhp is None:
        return None, None
    mon = ds_monhoc.find("ma_mon", lhp.ma_mon)
    return lhp, mon


# ====================================================================
# NHÓM 3: HÀM GHI DỮ LIỆU (thêm / sửa / xóa - dùng cho GUI)
# ====================================================================

def them_sinhvien(ds_sinhvien, mssv, hoten, gioitinh, lop, ngaysinh_str):
    """
    Thêm sinh viên mới.
    Trả về (True, hoten) hoặc (False, thông báo lỗi).
    """
    if ds_sinhvien.find("mssv", mssv.strip()) is not None:
        return False, f"MSSV [{mssv}] đã tồn tại trên hệ thống!"
    try:
        sv_moi = Sinhvien(mssv, hoten, gioitinh, lop, ngaysinh_str)
        ds_sinhvien.insert(sv_moi)
        return True, sv_moi.hoten
    except ValueError as e:
        return False, str(e)

def cap_nhat_sinhvien(ds_sinhvien, ds_diem, mssv, new_hoten, new_gioitinh, new_lop, new_ngaysinh_str):
    """
    Cập nhật thông tin sinh viên và đồng bộ tên sang bảng điểm.
    Trả về (True, "") hoặc (False, thông báo lỗi).
    """
    sv = ds_sinhvien.find("mssv", mssv)
    if sv is None:
        return False, f"Không tìm thấy sinh viên MSSV [{mssv}]!"
    backup = (sv.hoten, sv.gioitinh, sv.lop, sv.ngaysinh)
    ds_sinhvien.remove("mssv", mssv)
    try:
        sv.hoten = new_hoten
        sv.gioitinh = new_gioitinh
        sv.lop = new_lop
        sv.ngaysinh = new_ngaysinh_str
        ds_sinhvien.insert(sv)
        ds_diem.update(lambda x: x.mssv == mssv, hoten=sv.hoten)
        return True, ""
    except ValueError as e:
        sv.hoten, sv.gioitinh, sv.lop, sv.ngaysinh = backup
        ds_sinhvien.insert(sv)
        return False, str(e)

def xoa_sinhvien_cascade(ds_sinhvien, ds_diem, mssv):
    """Xóa sinh viên và toàn bộ điểm liên quan (cascade delete)."""
    ds_diem.remove_all_general("mssv", mssv)
    ds_sinhvien.remove("mssv", mssv)
    return True

def them_monhoc(ds_monhoc, ma_mon, ten_mon, so_tin_chi, khoa_vien, ty_le_qt):
    """
    Thêm môn học mới.
    Trả về (True, ten_mon) hoặc (False, thông báo lỗi).
    """
    if ds_monhoc.find("ma_mon", ma_mon.strip().upper()) is not None:
        return False, f"Mã môn [{ma_mon.upper()}] đã tồn tại!"
    try:
        ds_monhoc.append(Monhoc(ma_mon, ten_mon, so_tin_chi, khoa_vien, ty_le_qt))
        return True, ten_mon
    except ValueError as e:
        return False, str(e)

def them_lhp(ds_lhp, ds_monhoc, ma_lhp, ma_mon, hoc_ky, giang_vien):
    """
    Thêm lớp học phần mới, kiểm tra mã môn tồn tại trước.
    Trả về (True, ma_lhp) hoặc (False, thông báo lỗi).
    """
    if ds_lhp.find("ma_lhp", ma_lhp.strip()) is not None:
        return False, f"Mã LHP [{ma_lhp}] đã tồn tại!"
    if ds_monhoc.find("ma_mon", ma_mon.strip().upper()) is None:
        return False, f"Mã môn [{ma_mon}] không tồn tại trong danh mục môn học!"
    ds_lhp.append(LopHocPhan(ma_lhp, ma_mon, hoc_ky, giang_vien))
    return True, ma_lhp

def luu_diem(ds_sinhvien, ds_lhp, ds_monhoc, ds_diem, mssv, ma_lhp, diem_qt, diem_ck):
    """
    Thêm mới hoặc ghi đè điểm.
    Trả về (True, "them_moi" | "cap_nhat") hoặc (False, thông báo lỗi).
    """
    sv = ds_sinhvien.find("mssv", mssv)
    if sv is None:
        return False, f"Không tìm thấy sinh viên MSSV [{mssv}]!"
    lhp, mon = lay_thong_tin_lhp_va_mon(ma_lhp, ds_lhp, ds_monhoc)
    if lhp is None:
        return False, f"Lớp học phần [{ma_lhp}] không tồn tại!"
    if mon is None:
        return False, f"Môn học [{lhp.ma_mon}] của lớp này không có trong danh mục!"
    diem_cu = lay_diem_hien_tai(mssv, ma_lhp, ds_diem)
    try:
        if diem_cu is not None:
            ds_diem.update(
                lambda x: x.mssv == mssv and x.ma_lhp == ma_lhp,
                diem_qt=float(diem_qt), diem_ck=float(diem_ck),
            )
            return True, "cap_nhat"
        else:
            ds_diem.append(Diem(mssv, sv.hoten, mon.ma_mon, ma_lhp, lhp.hoc_ky, float(diem_qt), float(diem_ck)))
            return True, "them_moi"
    except ValueError as e:
        return False, str(e)


# ====================================================================
# NHÓM 4: HÀM CLI (giữ nguyên cho main.py / app.py terminal)
# ====================================================================

def themdiem(ds_sinhvien, ds_monhoc, ds_lhp, ds_diem):
    print("\n--- NHẬP ĐIỂM SỐ THEO LỚP HỌC PHẦN ---")
    mssv = input("Nhập MSSV: ").strip()
    sv = ds_sinhvien.find("mssv", mssv)
    if sv is None:
        print("Lỗi: Không tồn tại sinh viên này trên hệ thống!")
        return
    ma_lhp = input("Nhập Mã Lớp Học Phần (VD: 158241): ").strip()
    lhp = ds_lhp.find("ma_lhp", ma_lhp)
    if lhp is None:
        print(f"Lỗi: Lớp học phần [{ma_lhp}] không tồn tại!")
        return
    mon = ds_monhoc.find("ma_mon", lhp.ma_mon)
    if mon is None:
        print(f"Lỗi: Môn học [{lhp.ma_mon}] không tìm thấy!")
        return
    diem_cu_list = ds_diem.find_all("mssv", mssv)
    diem_cu = None
    current = diem_cu_list.head
    while current is not None:
        if current.data.ma_lhp == ma_lhp:
            diem_cu = current.data
            break
        current = current.next
    print(f"\n> Đang vào điểm cho sinh viên: {sv.hoten}")
    print(f"> Môn: {mon.ten_mon} | Học kỳ: {lhp.hoc_ky}")
    print(f"> Tỉ lệ Quá trình - Cuối kì = {mon.ty_le_qt}% - {100 - mon.ty_le_qt}%")
    if diem_cu is not None:
        print(f"\nSinh viên đã có điểm lớp này (QT: {diem_cu.diem_qt} | CK: {diem_cu.diem_ck}).")
        chon = input("Bạn có muốn GHI ĐÈ điểm mới không? (y/n): ").strip().lower()
        if chon != 'y':
            print("Đã hủy cập nhật.")
            return
    qt_input = input("Nhập điểm Quá trình (0-10): ").strip()
    ck_input = input("Nhập điểm Cuối kì (0-10): ").strip()
    try:
        if diem_cu is not None:
            ds_diem.update(lambda x: x.mssv == mssv and x.ma_lhp == ma_lhp, diem_qt=float(qt_input), diem_ck=float(ck_input))
            print("Đã cập nhật điểm thành công!")
        else:
            ds_diem.append(Diem(mssv, sv.hoten, mon.ma_mon, ma_lhp, lhp.hoc_ky, float(qt_input), float(ck_input)))
            print("Đã vào điểm mới thành công!")
    except ValueError as e:
        print(f"Lỗi dữ liệu: {e}")

def xuat_bang_diem_ca_nhan(mssv, ds_sinhvien, ds_monhoc, ds_diem):
    sv = ds_sinhvien.find("mssv", mssv)
    if sv is None:
        print(f"Không tìm thấy sinh viên có MSSV: {mssv}")
        return
    ds_diem_sv = ds_diem.find_all("mssv", mssv)
    if ds_diem_sv.head is None:
        print(f"Sinh viên {sv.hoten} chưa có điểm môn học nào.")
        return
    diem_theo_hk = {}
    current = ds_diem_sv.head
    while current is not None:
        d = current.data
        if d.hoc_ky not in diem_theo_hk:
            diem_theo_hk[d.hoc_ky] = []
        diem_theo_hk[d.hoc_ky].append(d)
        current = current.next
    print(f"\n{'='*20} BẢNG ĐIỂM CÁ NHÂN {'='*20}")
    print(f"Họ tên: {sv.hoten} | MSSV: {sv.mssv}")
    for hk in sorted(diem_theo_hk.keys()):
        print(f"\n--- HỌC KỲ: {hk} ---")
        for d in diem_theo_hk[hk]:
            mon = ds_monhoc.find("ma_mon", d.ma_mon)
            tc = mon.so_tin_chi if mon else 0
            ten_mon = mon.ten_mon if mon else "N/A"
            tk = d.tinh_tong_ket(mon.ty_le_qt) if mon else 0
            print(f"{d.ma_mon:<10} | {ten_mon:<20} | {tc:<3} | {d.diem_qt:<4} | {d.diem_ck:<4} | {tk:<4.1f}")
    tc, cpa10, cpa4 = tinh_cpa(mssv, ds_monhoc, ds_diem)
    print(f"Tổng TC: {tc} | CPA hệ 10: {cpa10:.2f} | CPA hệ 4: {cpa4:.2f} | Xếp loại: {quy_doi_xep_loai(cpa4)}")

def xuat_danh_sach_diem_lop_hoc_phan(ds_lhp, ds_monhoc, ds_diem):
    print("\n--- XUẤT BẢNG ĐIỂM LỚP HỌC PHẦN ---")
    ma_lhp = input("Nhập Mã Lớp học phần: ").strip()
    lhp = ds_lhp.find("ma_lhp", ma_lhp)
    if lhp is None:
        print(f"Lỗi: Không tồn tại lớp học phần mã [{ma_lhp}]!")
        return
    mon = ds_monhoc.find("ma_mon", lhp.ma_mon)
    if mon is None:
        print(f"Lỗi dữ liệu: Môn [{lhp.ma_mon}] không tồn tại!")
        return
    rows, dtb, si_so = lay_bang_diem_lhp(ma_lhp, ds_lhp, ds_monhoc, ds_diem)
    if not rows:
        print("Hiện chưa có sinh viên nào có điểm trong LHP này.")
        return
    print(f"Sĩ số có điểm: {si_so} | Điểm trung bình LHP: {dtb:.2f}")
    for r in rows:
        print(f"{r['STT']:<4} | {r['MSSV']:<12} | {r['Họ và tên']:<25} | {r['Điểm QT']:<4} | {r['Điểm CK']:<4} | {r['Tổng kết']:<5.2f}")

def xuat_danh_sach_sinh_vien_lhp(ds_lhp, ds_sinhvien, ds_diem):
    print("\n--- XUẤT DANH SÁCH SINH VIÊN THEO LỚP HỌC PHẦN ---")
    ma_lhp = input("Nhập Mã Lớp học phần: ").strip()
    lhp = ds_lhp.find("ma_lhp", ma_lhp)
    if lhp is None:
        print(f"Lỗi: Không tồn tại lớp học phần mã [{ma_lhp}]!")
        return
    rows = lay_thanh_vien_lhp(ma_lhp, ds_diem, ds_sinhvien)
    if not rows:
        print(f"Chưa có sinh viên nào đăng ký Lớp học phần [{ma_lhp}].")
        return
    for r in rows:
        print(f"{r['STT']:<4} | {r['MSSV']:<12} | {r['Họ và tên']:<25} | {r['Giới tính']:<10} | {r['Lớp sinh hoạt']}")

def xuat_xep_hang_gpa(ds_sinhvien, ds_monhoc, ds_diem):
    print("\n--- BẢNG XẾP HẠNG SINH VIÊN THEO GPA TÍCH LŨY ---")
    bang = lay_bang_xep_hang(ds_sinhvien, ds_monhoc, ds_diem)
    if not bang:
        print("Danh sách sinh viên đang trống!")
        return
    for r in bang:
        print(f"{r['Hạng']:<5} | {r['MSSV']:<12} | {r['Họ tên']:<25} | {r['TC tích lũy']:<4} | {r['CPA Hệ 10']:<6.2f} | {r['CPA Hệ 4']:<5.2f} | {r['Xếp loại']}")
