from datetime import datetime
class Sinhvien:
    def __init__ (self,mssv,hoten,gioitinh,lop,ngaysinh):
      self.mssv=mssv
      self.hoten=hoten
      self.gioitinh=gioitinh
      self.lop=lop
      self.ngaysinh=ngaysinh
    
    @property
    def mssv(self): return self._mssv
   
    @mssv.setter
    def mssv(self,value):
        value = str(value).strip()
        if len(value) == 0: raise ValueError("Lỗi: Mã sinh viên không được để trống!")
        self._mssv = value

    @property
    def hoten(self): return self._hoten

    @hoten.setter
    def hoten(self, value):
        value = str(value).strip()
        if len(value) == 0: raise ValueError("Lỗi: Họ tên sinh viên không được để trống!")
        self._hoten = value.title()
    @property
    def ngaysinh(self): return self._ngaysinh
    
    @ngaysinh.setter
    def ngaysinh(self, value):
        value = str(value).strip()
        if len(value) == 0:
            raise ValueError("Lỗi: Ngày sinh không được để trống!") 
            
        # 📌 MỚI: Ép buộc ngày sinh phải đúng định dạng và có thật trên đời
        try:
            # Nếu nhập 31/02/2006 máy sẽ báo lỗi ngay vì tháng 2 không có ngày 31
            datetime.strptime(value, "%d/%m/%Y")
            self._ngaysinh = value
        except ValueError:
            raise ValueError("Lỗi: Ngày sinh phải đúng định dạng dd/mm/yyyy và phải là ngày hợp lệ!")
      
    def __str__(self):
        return f"{self.mssv:<12} | {self.hoten:<25} | {self.gioitinh:<10} | {self.lop:<15} | {self.ngaysinh:<15}"

class Monhoc:
    def __init__(self, ma_mon, ten_mon, so_tin_chi, khoa_vien, ty_le_qt):
        self.ma_mon = ma_mon
        self.ten_mon = ten_mon
        self.so_tin_chi = so_tin_chi
        self.khoa_vien = khoa_vien
        self.ty_le_qt = ty_le_qt

    @property
    def ma_mon(self): return self._ma_mon

    @ma_mon.setter
    def ma_mon(self, value):
        value = str(value).strip().upper()
        if len(value) == 0: raise ValueError("Lỗi: Mã môn học không được để trống!")
        self._ma_mon = value

    @property
    def ten_mon(self): return self._ten_mon

    @ten_mon.setter
    def ten_mon(self, value):
        value = str(value).strip()
        if len(value) == 0: raise ValueError("Lỗi: Tên môn học không được để trống!")
        self._ten_mon = value

    @property
    def so_tin_chi(self): return self._so_tin_chi

    @so_tin_chi.setter
    def so_tin_chi(self, value):
        try: value = int(value)
        except ValueError: raise ValueError("Lỗi: Số tín chỉ phải là một số nguyên!")
        if value <= 0: raise ValueError("Lỗi: Số tín chỉ phải lớn hơn 0!")
        self._so_tin_chi = value

    @property
    def khoa_vien(self): return self._khoa_vien

    @khoa_vien.setter
    def khoa_vien(self, value):
        value = str(value).strip()
        if len(value) == 0: raise ValueError("Lỗi: Tên Khoa/Viện không được để trống!")
        self._khoa_vien = value

    @property
    def ty_le_qt(self): return self._ty_le_qt

    @ty_le_qt.setter
    def ty_le_qt(self, value):
        try: value = int(value)
        except (ValueError, TypeError): raise ValueError("Lỗi: Tỉ lệ điểm quá trình phải là số nguyên!")
        if value < 0 or value > 100: raise ValueError("Lỗi: Tỉ lệ điểm quá trình phải từ 0-100!")
        self._ty_le_qt = value

    def __str__(self):
        return (f"Mã môn học: {self.ma_mon:<8} | Tên môn: {self.ten_mon:<25} | "
                f"TC: {self.so_tin_chi} | Tỉ lệ QT/CK: {self.ty_le_qt}%/{100 - self.ty_le_qt}%")

class LopHocPhan:
    def __init__(self, ma_lhp, ma_mon, hoc_ky, giang_vien=""):
        self.ma_lhp = str(ma_lhp).strip()
        self.ma_mon = str(ma_mon).strip().upper()
        self.hoc_ky = str(hoc_ky).strip()
        self.giang_vien = str(giang_vien).strip()

    def __str__(self):
        return f"Mã LHP: {self.ma_lhp:<8} | Môn: {self.ma_mon:<8} | Học kỳ: {self.hoc_ky:<8} | GV: {self.giang_vien}"

class Diem:
    # Đã sửa lỗi: Thêm ma_lhp và hoc_ky vào tham số __init__
    def __init__(self, mssv, hoten, ma_mon, ma_lhp, hoc_ky, diem_qt, diem_ck):
        self.mssv = mssv
        self.hoten = hoten
        self.ma_mon = ma_mon
        self.ma_lhp = str(ma_lhp).strip()
        self.hoc_ky = str(hoc_ky).strip()
        self.diem_qt = diem_qt
        self.diem_ck = diem_ck

    @property
    def mssv(self): return self._mssv
    @mssv.setter
    def mssv(self, value):
        value = str(value).strip()
        if len(value) == 0: raise ValueError("Lỗi: MSSV không được để trống!")
        self._mssv = value

    @property
    def hoten(self): return self._hoten
    @hoten.setter
    def hoten(self, value):
        value = str(value).strip()
        if len(value) == 0: raise ValueError("Lỗi: Họ tên không được để trống!")
        self._hoten = value.title()

    @property
    def ma_mon(self): return self._ma_mon
    @ma_mon.setter
    def ma_mon(self, value):
        value = str(value).strip().upper()
        if len(value) == 0: raise ValueError("Lỗi: Mã môn học không được để trống!")
        self._ma_mon = value

    @property
    def diem_qt(self): return self._diem_qt
    @diem_qt.setter
    def diem_qt(self, value):
        self._diem_qt = self._kiem_tra_diem(value, "Điểm quá trình")

    @property
    def diem_ck(self): return self._diem_ck
    @diem_ck.setter
    def diem_ck(self, value):
        self._diem_ck = self._kiem_tra_diem(value, "Điểm cuối kì")

    @staticmethod
    def _kiem_tra_diem(value, ten_diem):
        try: value = float(value)
        except (ValueError, TypeError): raise ValueError(f"Lỗi: {ten_diem} phải là một con số!")
        if value < 0 or value > 10: raise ValueError(f"Lỗi: {ten_diem} ({value}) không hợp lệ. Điểm từ 0-10!")
        return value

    def tinh_tong_ket(self, ty_le_qt):
        ty_le_ck = 100 - ty_le_qt
        return (self.diem_qt * ty_le_qt + self.diem_ck * ty_le_ck) / 100

    def __str__(self):
        return (f"{self.mssv:<10} | {self.hoten:<22} | LHP: {self.ma_lhp:<7} | "
                f"HK: {self.hoc_ky:<6} | QT: {self.diem_qt:<4} | CK: {self.diem_ck:<4}")