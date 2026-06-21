"""
app.py — Lớp giao diện thuần túy (View Layer).
Không chứa bất kỳ logic nghiệp vụ nào.
Toàn bộ xử lý dữ liệu được ủy quyền sang services.py và strutures.py.
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from strutures import LinkedList
from iohandler import load_all_data, save_all_data
import services as svc  # Toàn bộ nghiệp vụ nằm trong services

# ============================================================
# CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="BK-CORE | Quản lý Sinh viên",
    page_icon="🎓",
    layout="wide",
)

# ============================================================
# QUẢN LÝ PHIÊN VÀ DỮ LIỆU
# ============================================================
def _nap_du_lieu_moi():
    """Khởi tạo 4 LinkedList rỗng rồi nạp dữ liệu từ file JSON."""
    ds_sv = LinkedList()
    ds_mh = LinkedList()
    ds_lhp = LinkedList()
    ds_diem = LinkedList()
    load_all_data(ds_sv, ds_mh, ds_lhp, ds_diem)
    return ds_sv, ds_mh, ds_lhp, ds_diem

# Chỉ nạp lại từ đĩa khi không có thay đổi đang chờ lưu
if "da_thay_doi" not in st.session_state:
    st.session_state.da_thay_doi = False

if "ds_sinhvien" not in st.session_state or not st.session_state.da_thay_doi:
    (
        st.session_state.ds_sinhvien,
        st.session_state.ds_monhoc,
        st.session_state.ds_lhp,
        st.session_state.ds_diem,
    ) = _nap_du_lieu_moi()

# Shortcut cục bộ để code ngắn gọn hơn
ds_sv   = st.session_state.ds_sinhvien
ds_mh   = st.session_state.ds_monhoc
ds_lhp  = st.session_state.ds_lhp
ds_diem = st.session_state.ds_diem


def _luu_xuong_dia():
    """Ghi toàn bộ dữ liệu trong bộ nhớ xuống file JSON."""
    save_all_data(ds_sv, ds_mh, ds_lhp, ds_diem, im_lang=True)
    st.session_state.da_thay_doi = False


def _danh_dau_co_thay_doi():
    """Đánh dấu rằng dữ liệu trong RAM đã thay đổi, chưa lưu xuống đĩa."""
    st.session_state.da_thay_doi = True


# ============================================================
# SIDEBAR — ĐIỀU HƯỚNG VÀ LƯU/TẢI
# ============================================================
st.sidebar.title("🎓 BK-CORE")
st.sidebar.caption("Hệ thống Quản lý Đào tạo")

if st.session_state.da_thay_doi:
    st.sidebar.warning("⚠️ Có thay đổi chưa lưu!")
else:
    st.sidebar.success("✅ Dữ liệu đã đồng bộ")

col_save, col_reload = st.sidebar.columns(2)
if col_save.button("💾 Lưu", use_container_width=True, type="primary"):
    _luu_xuong_dia()
    st.sidebar.success("Đã lưu!")
    st.rerun()
if col_reload.button("🔄 Tải lại", use_container_width=True):
    st.session_state.da_thay_doi = False
    st.rerun()

st.sidebar.divider()

menu = st.sidebar.radio(
    "PHÂN KHU CHỨC NĂNG",
    [
        "🏠 Tổng quan",
        "👨‍🎓 Sinh viên",
        "📚 Môn học & LHP",
        "📝 Điểm số & Học lực",
    ],
)

st.sidebar.divider()
st.sidebar.caption(
    f"SV: **{svc.dem_so_node(ds_sv)}** | "
    f"Môn: **{svc.dem_so_node(ds_mh)}** | "
    f"LHP: **{svc.dem_so_node(ds_lhp)}** | "
    f"Điểm: **{svc.dem_so_node(ds_diem)}**"
)


# ============================================================
# TRANG 1 — TỔNG QUAN
# ============================================================
if menu == "🏠 Tổng quan":
    st.title("🏛️ HỆ THỐNG QUẢN LÝ ĐÀO TẠO BK-CORE")
    st.write("Giao diện web đồng bộ cùng cơ sở dữ liệu với bản CLI (`main.py`).")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👨‍🎓 Sinh viên",        svc.dem_so_node(ds_sv))
    c2.metric("📖 Môn học",           svc.dem_so_node(ds_mh))
    c3.metric("🏫 Lớp học phần",      svc.dem_so_node(ds_lhp))
    c4.metric("📝 Đầu điểm số",       svc.dem_so_node(ds_diem))

    if svc.dem_so_node(ds_sv) > 0:
        st.divider()
        st.subheader("🏆 Top 5 sinh viên có GPA cao nhất")
        bang = svc.lay_bang_xep_hang(ds_sv, ds_mh, ds_diem)
        if bang:
            top5 = [r for r in bang if r["TC tích lũy"] > 0][:5]
            if top5:
                st.dataframe(pd.DataFrame(top5), use_container_width=True, hide_index=True)
            else:
                st.info("Chưa có sinh viên nào có điểm để xếp hạng.")


# ============================================================
# TRANG 2 — QUẢN LÝ SINH VIÊN
# ============================================================
elif menu == "👨‍🎓 Sinh viên":
    st.title("👨‍🎓 Quản lý Thông tin Sinh viên")

    tab_xem, tab_them, tab_sua_xoa = st.tabs([
        "🔍 Danh sách",
        "➕ Thêm mới",
        "⚙️ Sửa & Xóa",
    ])

    # ── Tab: Xem danh sách ──────────────────────────────────
    with tab_xem:
        rows = svc.lay_danh_sach_sinhvien(ds_sv)
        if not rows:
            st.info("Danh sách sinh viên đang trống.")
        else:
            sap_xep = st.selectbox(
                "Sắp xếp theo:",
                ["Mặc định (A-Z theo tên)", "MSSV", "Lớp sinh hoạt"],
                key="sort_sv",
            )
            df = pd.DataFrame(rows)
            if sap_xep == "MSSV":
                df = df.sort_values("MSSV")
            elif sap_xep == "Lớp sinh hoạt":
                df = df.sort_values("Lớp")
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Tổng cộng: {len(rows)} sinh viên")

    # ── Tab: Thêm sinh viên ─────────────────────────────────
    with tab_them:
        with st.form("form_them_sv", clear_on_submit=True):
            c1, c2 = st.columns(2)
            inp_mssv    = c1.text_input("Mã số sinh viên (MSSV) *")
            inp_hoten   = c2.text_input("Họ và tên *")
            inp_gt      = c1.selectbox("Giới tính", ["Nam", "Nữ", "Khác"])
            inp_lop     = c2.text_input("Lớp sinh hoạt")
            inp_ns      = c1.date_input(
                "Ngày sinh",
                min_value=datetime(1990, 1, 1),
                value=datetime(2006, 1, 1),
            )
            submitted = st.form_submit_button("➕ Thêm vào hệ thống", type="primary")

        if submitted:
            if not inp_mssv or not inp_hoten:
                st.error("Vui lòng điền đầy đủ MSSV và Họ tên.")
            else:
                ok, msg = svc.them_sinhvien(
                    ds_sv, inp_mssv, inp_hoten, inp_gt, inp_lop,
                    inp_ns.strftime("%d/%m/%Y"),
                )
                if ok:
                    _danh_dau_co_thay_doi()
                    st.success(f"✅ Đã thêm sinh viên: **{msg}** (chưa lưu file)")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    # ── Tab: Sửa & Xóa ─────────────────────────────────────
    with tab_sua_xoa:
        ds_chon = svc.lay_danh_sach_chon_sv(ds_sv)
        if not ds_chon:
            st.info("Chưa có dữ liệu sinh viên.")
        else:
            chon = st.selectbox("Chọn sinh viên cần thao tác:", ds_chon, key="sel_sua_sv")
            mssv_chon = chon.split(" - ")[0]
            sv_obj = ds_sv.find("mssv", mssv_chon)

            if sv_obj:
                st.markdown("#### 📝 Cập nhật thông tin")
                try:
                    ns_hien = datetime.strptime(sv_obj.ngaysinh, "%d/%m/%Y")
                except ValueError:
                    ns_hien = datetime(2006, 1, 1)

                with st.form("form_sua_sv"):
                    new_ht  = st.text_input("Họ và tên", value=sv_obj.hoten)
                    new_gt  = st.selectbox(
                        "Giới tính", ["Nam", "Nữ", "Khác"],
                        index=["Nam", "Nữ", "Khác"].index(sv_obj.gioitinh)
                        if sv_obj.gioitinh in ["Nam", "Nữ", "Khác"] else 0,
                    )
                    new_lop = st.text_input("Lớp sinh hoạt", value=sv_obj.lop)
                    new_ns  = st.date_input("Ngày sinh", value=ns_hien, min_value=datetime(1990, 1, 1))
                    btn_sua = st.form_submit_button("💾 Lưu thay đổi", type="primary")

                if btn_sua:
                    ok, msg = svc.cap_nhat_sinhvien(
                        ds_sv, ds_diem,
                        mssv_chon, new_ht, new_gt, new_lop,
                        new_ns.strftime("%d/%m/%Y"),
                    )
                    if ok:
                        _danh_dau_co_thay_doi()
                        st.success("✅ Đã cập nhật thông tin! (chưa lưu file)")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

                st.divider()
                st.markdown("#### 🚨 Vùng nguy hiểm")
                st.warning(
                    f"Xóa **{sv_obj.hoten}** sẽ đồng thời xóa toàn bộ điểm "
                    f"liên quan (cascade delete). Thao tác không thể hoàn tác!"
                )
                if st.button("🗑️ Xóa sinh viên và toàn bộ điểm liên quan", type="secondary"):
                    svc.xoa_sinhvien_cascade(ds_sv, ds_diem, mssv_chon)
                    _danh_dau_co_thay_doi()
                    st.warning(f"Đã xóa sinh viên **{mssv_chon}**. (chưa lưu file)")
                    st.rerun()


# ============================================================
# TRANG 3 — MÔN HỌC & LỚP HỌC PHẦN
# ============================================================
elif menu == "📚 Môn học & LHP":
    st.title("📚 Danh mục Đào tạo")

    tab_mh, tab_lhp, tab_tv = st.tabs([
        "📖 Môn học",
        "🏫 Lớp Học Phần",
        "👥 Thành viên LHP",
    ])

    # ── Tab: Môn học ────────────────────────────────────────
    with tab_mh:
        rows_mh = svc.lay_danh_sach_monhoc(ds_mh)
        if rows_mh:
            st.dataframe(pd.DataFrame(rows_mh), use_container_width=True, hide_index=True)
        else:
            st.info("Chưa có môn học nào.")

        st.divider()
        with st.expander("➕ Thêm môn học mới"):
            with st.form("form_them_mh", clear_on_submit=True):
                c1, c2 = st.columns(2)
                inp_ma  = c1.text_input("Mã môn *")
                inp_ten = c2.text_input("Tên môn *")
                inp_tc  = c1.number_input("Số tín chỉ", min_value=1, step=1, value=3)
                inp_kv  = c2.text_input("Khoa/Viện")
                inp_tl  = c1.number_input("Tỉ lệ điểm Quá trình (%)", min_value=0, max_value=100, step=5, value=30)
                btn_mh  = st.form_submit_button("Thêm môn học", type="primary")

            if btn_mh:
                if not inp_ma or not inp_ten:
                    st.error("Vui lòng điền đầy đủ Mã môn và Tên môn.")
                else:
                    ok, msg = svc.them_monhoc(ds_mh, inp_ma, inp_ten, inp_tc, inp_kv, inp_tl)
                    if ok:
                        _danh_dau_co_thay_doi()
                        st.success(f"✅ Đã thêm môn: **{msg}** (chưa lưu file)")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

    # ── Tab: Lớp học phần ───────────────────────────────────
    with tab_lhp:
        rows_lhp = svc.lay_danh_sach_lhp(ds_lhp)
        if rows_lhp:
            st.dataframe(pd.DataFrame(rows_lhp), use_container_width=True, hide_index=True)
        else:
            st.info("Chưa có lớp học phần nào.")

        st.divider()
        with st.expander("➕ Thêm Lớp Học Phần mới"):
            ds_ma_mon = [r["Mã môn"] for r in svc.lay_danh_sach_monhoc(ds_mh)]
            with st.form("form_them_lhp", clear_on_submit=True):
                c1, c2 = st.columns(2)
                inp_ma_lhp = c1.text_input("Mã LHP *")
                if ds_ma_mon:
                    inp_ma_mon = c2.selectbox("Mã môn học *", ds_ma_mon)
                else:
                    inp_ma_mon = c2.text_input("Mã môn học * (chưa có danh mục)")
                inp_hk  = c1.text_input("Học kỳ (VD: 2024.1) *")
                inp_gv  = c2.text_input("Giảng viên phụ trách")
                btn_lhp = st.form_submit_button("Thêm Lớp Học Phần", type="primary")

            if btn_lhp:
                if not inp_ma_lhp or not inp_ma_mon or not inp_hk:
                    st.error("Vui lòng điền đầy đủ Mã LHP, Mã môn và Học kỳ.")
                else:
                    ok, msg = svc.them_lhp(ds_lhp, ds_mh, inp_ma_lhp, inp_ma_mon, inp_hk, inp_gv)
                    if ok:
                        _danh_dau_co_thay_doi()
                        st.success(f"✅ Đã thêm LHP: **{msg}** (chưa lưu file)")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

    # ── Tab: Thành viên LHP ─────────────────────────────────
    with tab_tv:
        ds_chon_lhp = svc.lay_danh_sach_chon_lhp(ds_lhp)
        if not ds_chon_lhp:
            st.info("Chưa có lớp học phần nào.")
        else:
            chon_lhp = st.selectbox("Chọn Lớp Học Phần:", ds_chon_lhp, key="sel_tv_lhp")
            ma_lhp_chon = chon_lhp.split(" - ")[0]
            rows_tv = svc.lay_thanh_vien_lhp(ma_lhp_chon, ds_diem, ds_sv)
            if not rows_tv:
                st.warning("Chưa có sinh viên nào đăng ký lớp học phần này.")
            else:
                st.dataframe(pd.DataFrame(rows_tv), use_container_width=True, hide_index=True)
                st.caption(f"📌 Tổng sĩ số: **{len(rows_tv)}** sinh viên")


# ============================================================
# TRANG 4 — ĐIỂM SỐ & HỌC LỰC
# ============================================================
elif menu == "📝 Điểm số & Học lực":
    st.title("📝 Quản lý Điểm số & Học lực")

    tab_nhap, tab_ca_nhan, tab_lhp_bd, tab_xephang = st.tabs([
        "🎯 Nhập / Cập nhật Điểm",
        "🔍 Bảng điểm Cá nhân",
        "📋 Bảng điểm Lớp Học Phần",
        "🏆 Xếp hạng GPA",
    ])

    # ── Tab: Nhập điểm ──────────────────────────────────────
    with tab_nhap:
        ds_chon_sv  = svc.lay_danh_sach_chon_sv(ds_sv)
        ds_chon_lhp = svc.lay_danh_sach_chon_lhp(ds_lhp)

        if not ds_chon_sv or not ds_chon_lhp:
            st.warning("Cần có ít nhất một sinh viên và một lớp học phần để nhập điểm.")
        else:
            c_sv  = st.selectbox("Sinh viên:", ds_chon_sv, key="nhap_sv")
            c_lhp = st.selectbox("Lớp Học Phần:", ds_chon_lhp, key="nhap_lhp")

            mssv_sel   = c_sv.split(" - ")[0]
            ma_lhp_sel = c_lhp.split(" - ")[0]

            # Lấy thông tin LHP và môn — gọi service, không tự truy xuất
            lhp_obj, mon_obj = svc.lay_thong_tin_lhp_va_mon(ma_lhp_sel, ds_lhp, ds_mh)

            if mon_obj is None:
                lhp_str = f"[{ma_lhp_sel}]"
                st.error(f"❌ Lỗi dữ liệu: LHP {lhp_str} không tìm thấy môn học tương ứng!")
            else:
                # Hiển thị thông tin tham chiếu
                st.info(
                    f"📌 Môn: **{mon_obj.ten_mon}** | "
                    f"Học kỳ: **{lhp_obj.hoc_ky}** | "
                    f"Tỉ lệ QT/CK: **{mon_obj.ty_le_qt}%/{100 - mon_obj.ty_le_qt}%**"
                )

                # Lấy điểm hiện tại (nếu đã có)
                diem_cu = svc.lay_diem_hien_tai(mssv_sel, ma_lhp_sel, ds_diem)
                if diem_cu:
                    st.warning(
                        f"Sinh viên đã có điểm tại LHP này "
                        f"(QT: **{diem_cu.diem_qt}** | CK: **{diem_cu.diem_ck}**). "
                        f"Lưu sẽ **ghi đè**."
                    )

                v_qt = float(diem_cu.diem_qt) if diem_cu else 0.0
                v_ck = float(diem_cu.diem_ck) if diem_cu else 0.0

                with st.form("form_nhap_diem"):
                    c1, c2 = st.columns(2)
                    d_qt = c1.number_input("Điểm Quá trình (0–10)", min_value=0.0, max_value=10.0, value=v_qt, step=0.1)
                    d_ck = c2.number_input("Điểm Cuối kỳ (0–10)",   min_value=0.0, max_value=10.0, value=v_ck, step=0.1)
                    btn_luu = st.form_submit_button("💾 Lưu kết quả điểm", type="primary")

                if btn_luu:
                    ok, msg = svc.luu_diem(ds_sv, ds_lhp, ds_mh, ds_diem, mssv_sel, ma_lhp_sel, d_qt, d_ck)
                    if ok:
                        _danh_dau_co_thay_doi()
                        action = "Thêm mới" if msg == "them_moi" else "Cập nhật"
                        st.success(f"✅ {action} điểm thành công! (chưa lưu file)")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

    # ── Tab: Bảng điểm cá nhân ──────────────────────────────
    with tab_ca_nhan:
        ds_chon_sv2 = svc.lay_danh_sach_chon_sv(ds_sv)
        if not ds_chon_sv2:
            st.info("Chưa có sinh viên nào.")
        else:
            chon_sv2 = st.selectbox("Tra cứu sinh viên:", ds_chon_sv2, key="sel_bd_sv")
            mssv_bd  = chon_sv2.split(" - ")[0]

            # Lấy toàn bộ dữ liệu bảng điểm qua service
            bd = svc.lay_bang_diem_ca_nhan(mssv_bd, ds_sv, ds_mh, ds_diem)

            if bd["sv"] is None:
                st.error("Không tìm thấy sinh viên.")
            elif not bd["diem_theo_hk"]:
                st.info(f"Sinh viên **{bd['sv'].hoten}** chưa có điểm môn học nào.")
            else:
                sv_bd = bd["sv"]
                st.markdown(f"### {sv_bd.hoten} — MSSV: `{sv_bd.mssv}` | Lớp: {sv_bd.lop}")

                # Hiển thị từng học kỳ
                for hk in sorted(bd["diem_theo_hk"].keys()):
                    rows_hk = bd["diem_theo_hk"][hk]
                    st.markdown(f"**Học kỳ {hk}**")
                    df_hk = pd.DataFrame(rows_hk)
                    st.dataframe(df_hk, use_container_width=True, hide_index=True)

                # Tổng kết tích lũy
                st.divider()
                c1, c2, c3 = st.columns(3)
                c1.metric("Tổng TC tích lũy", bd["tong_tc"])
                c2.metric("CPA (Hệ 4)",       f"{bd['cpa_4']:.2f}", help=f"Hệ 10: {bd['cpa_10']:.2f}")
                c3.metric("Xếp loại",         svc.quy_doi_xep_loai(bd["cpa_4"]) if bd["tong_tc"] > 0 else "Chưa có điểm")

    # ── Tab: Bảng điểm LHP ──────────────────────────────────
    with tab_lhp_bd:
        ds_chon_lhp2 = svc.lay_danh_sach_chon_lhp(ds_lhp)
        if not ds_chon_lhp2:
            st.info("Chưa có lớp học phần nào.")
        else:
            chon_lhp2   = st.selectbox("Chọn Lớp Học Phần:", ds_chon_lhp2, key="sel_bd_lhp")
            ma_lhp_bd   = chon_lhp2.split(" - ")[0]

            rows_bd, dtb, si_so = svc.lay_bang_diem_lhp(ma_lhp_bd, ds_lhp, ds_mh, ds_diem)

            if rows_bd is None:
                st.error("❌ Lỗi dữ liệu: Không tìm thấy LHP hoặc môn học tương ứng.")
            elif not rows_bd:
                st.info("Lớp học phần này chưa có điểm.")
            else:
                sort_bd = st.radio(
                    "Sắp xếp theo:",
                    ["MSSV", "Tổng kết (cao → thấp)", "Tên sinh viên"],
                    horizontal=True,
                    key="sort_bd_lhp",
                )
                df_bd = pd.DataFrame(rows_bd)
                if sort_bd == "MSSV":
                    df_bd = df_bd.sort_values("MSSV")
                elif sort_bd == "Tổng kết (cao → thấp)":
                    df_bd = df_bd.sort_values("Tổng kết", ascending=False)
                elif sort_bd == "Tên sinh viên":
                    df_bd = df_bd.sort_values("Họ và tên")
                df_bd = df_bd.reset_index(drop=True)
                df_bd["STT"] = df_bd.index + 1

                st.dataframe(df_bd, use_container_width=True, hide_index=True)
                st.caption(f"Sĩ số có điểm: **{si_so}** | Điểm trung bình LHP: **{dtb:.2f}**")

    # ── Tab: Xếp hạng GPA ───────────────────────────────────
    with tab_xephang:
        st.subheader("🏆 Bảng xếp hạng học lực theo CPA tích lũy")
        if svc.dem_so_node(ds_sv) == 0:
            st.info("Danh sách sinh viên đang trống.")
        else:
            bang_xh = svc.lay_bang_xep_hang(ds_sv, ds_mh, ds_diem)
            if bang_xh:
                df_xh = pd.DataFrame(bang_xh)
                st.dataframe(df_xh, use_container_width=True, hide_index=True)
            else:
                st.info("Chưa có dữ liệu để xếp hạng.")
