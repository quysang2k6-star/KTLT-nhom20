class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None  # Ban đầu danh sách rỗng (chưa có toa nào)
    def append(self, data):
        new_node = Node(data)
        # Nếu danh sách đang trống, phần tử mới chính là điểm bắt đầu (head)
        if self.head is None:
            self.head = new_node
            return   
        # Nếu danh sách đã có phần tử, dùng vòng lặp đi tìm phần tử cuối cùng
        current = self.head
        while current.next is not None:
            current = current.next    
        # Móc phần tử mới vào phía sau phần tử cuối cùng
        current.next = new_node
    def insert(self, new_sinhvien):
        """Thuật toán: Chèn sinh viên mới vào đúng vị trí bảng chữ cái ngay khi thêm"""
        new_node = Node(new_sinhvien)
        
        # Lấy tên của sinh viên mới để đem đi so sánh
        ten_moi = new_sinhvien.hoten.split()[-1]

        # TRƯỜNG HỢP 1: Danh sách trống HOẶC sinh viên mới đứng trước cả đầu tàu
        if self.head is None or self.head.data.hoten.split()[-1] > ten_moi:
            new_node.next = self.head
            self.head = new_node
            return

        # TRƯỜNG HỢP 2: Đi tìm vị trí thích hợp ở thân hoặc đuôi tàu
        current = self.head
        
        # Vòng lặp dừng lại khi: 
        # - Hoặc đã đến toa cuối cùng (current.next is None)
        # - Hoặc toa tiếp theo có tên đứng sau sinh viên mới
        while current.next is not None and current.next.data.hoten.split()[-1] < ten_moi:
            current = current.next

        # Thực hiện hành động chen vào giữa (hoặc nối vào cuối)
        new_node.next = current.next
        current.next = new_node
    def remove(self,thuoc_tinh,data):
        if thuoc_tinh == "mssv":
            tien_to = "sinh viên có MSSV"
        elif thuoc_tinh == "ma_mon":
            tien_to = "môn học có mã"
        else:
            tien_to = f"đối tượng có {thuoc_tinh}"
        if self.head is None:
            print('Lỗi: Danh sách trống, không có dữ liệu để xóa!')
            return
        if getattr(self.head.data, thuoc_tinh) == data:
            self.head= self.head.next
            print(f"Đã xóa thành công {tien_to}: {data}")
            return
        current=self.head
        prev=None
        while current is not None and getattr(current.data, thuoc_tinh) !=data:
            prev=current
            current=current.next
        if current is None:
            print(f'Lỗi: Không tìm thấy {tien_to}: {data} để xóa!')
            return
        prev.next=current.next 
        print(f'Đã xóa thành công {tien_to}: {data}')
    def remove_all_general(self, thuoc_tinh, data):
        """Hàm càn quét đa năng: Xóa sạch mọi node có thuộc tính trùng khớp"""
        # Xử lý dứt điểm khu vực đầu tàu
        while self.head is not None and getattr(self.head.data, thuoc_tinh) == data:
            self.head = self.head.next

        if self.head is None:
            return

        # Tuần tra khu vực thân và đuôi tàu
        current = self.head
        while current.next is not None:
            if getattr(current.next.data,thuoc_tinh) == data:
                current.next = current.next.next  # Bẻ liên kết
            else:
                current = current.next
    def find(self,thuoc_tinh, data):
        current=self.head
        while current is not None:
            if getattr(current.data, thuoc_tinh)==data:
                return current.data
            current=current.next
        return None
    def find_all(self, thuoc_tinh, data):
    # Dùng self.__class__() để tự động gọi class hiện tại mà không bị IDE bắt bẻ
        ketqua = LinkedList() 
        current = self.head
        while current is not None:
            if getattr(current.data,thuoc_tinh) == data:
                ketqua.append(current.data)  # Vẫn dùng append bình thường
            current = current.next     
        return ketqua
    def update(self, condition_func, **kwargs):
        current = self.head
        found = False  # 🚩 Bước 1: Khởi tạo cờ hiệu là False
        while current is not None:
            if condition_func(current.data): 
                for field, value in kwargs.items():
                    if hasattr(current.data, field):
                        setattr(current.data, field, value)
                print(f"-> Đã cập nhật thành công: {current.data}")
                found = True  # 🚩 Bước 2: Phất cờ lên khi có ít nhất một phần tử được sửa
            current = current.next
        # 🚩 Bước 3: ĐI HẾT đoàn tàu RỒI mới kiểm tra cờ (khối này nằm NGOÀI while)
        if not found:
            print("-> Lỗi: Không tìm thấy đối tượng khớp điều kiện.")
            return False
        return True
    def sort_general(self,thuoc_tinh, tang_dan=True):
        if self.head is None or self.head.next is None:
            return
        swapped = True
        while swapped:
            swapped = False
            current = self.head 
            while current.next is not None:
            
                val_hien_tai = getattr(current.data, thuoc_tinh)
                val_ke_tiep = getattr(current.next.data,thuoc_tinh)
                dieu_kien_doi = (val_hien_tai > val_ke_tiep) if tang_dan else (val_hien_tai < val_ke_tiep)
                if dieu_kien_doi:
                    current.data, current.next.data = current.next.data, current.data
                    swapped = True
                
                current = current.next
    def sort_theo_ten(self):
        """Sắp xếp theo TÊN (từ cuối của họ tên) - đồng nhất với thứ tự khi insert"""
        if self.head is None or self.head.next is None:
            return
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current.next is not None:
                if current.data.hoten.split()[-1] > current.next.data.hoten.split()[-1]:
                    current.data, current.next.data = current.next.data, current.data
                    swapped = True
                current = current.next

    def display(self):
        """Thuật toán: Duyệt và in toàn bộ danh sách ra màn hình"""
        current = self.head
        
        if current is None:
            print("Danh sách đang trống!")
            return
            
        while current is not None:
            print(current.data)  # Tự động gọi hàm __str__ của đối tượng bên trong
            current = current.next