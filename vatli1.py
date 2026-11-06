import math
def tinh_luc_he_dien_tich(danh_sach_dien_tich):
    n = len(danh_sach_dien_tich)
    k_so = 9e9  # Hằng số Coulomb (N.m^2/C^2)
    ket_qua = {}
    
    for i in range(n):
        q_i = danh_sach_dien_tich[i]['q']
        x_i = danh_sach_dien_tich[i]['x']
        y_i = danh_sach_dien_tich[i]['y']
        
        Fx_so = 0.0
        Fy_so = 0.0
        
        # Tạo chuỗi biểu thức tượng trưng (giống phong cách sympy thu gọn)
        Fx_bieu_thuc_parts = []
        Fy_bieu_thuc_parts = []
        
        for j in range(n):
            if i == j:
                continue
            q_j = danh_sach_dien_tich[j]['q']
            x_j = danh_sach_dien_tich[j]['x']
            y_j = danh_sach_dien_tich[j]['y']
            
            # Khoảng cách và bình phương khoảng cách
            dx = x_i - x_j
            dy = y_i - y_j
            r2 = dx**2 + dy**2
            r3 = r2 * math.sqrt(r2) if r2 > 0 else 0
            
            # Thành phần lực theo phương x và y
            if r3 != 0:
                f_x = k_so * (q_i * q_j * dx) / r3
                f_y = k_so * (q_i * q_j * dy) / r3
                
                Fx_so += f_x
                Fy_so += f_y
                
                # Lưu chuỗi biểu thức minh họa
                Fx_bieu_thuc_parts.append(f"k*({q_i}*{q_j}*({dx}))/({r2})^(3/2)")
                Fy_bieu_thuc_parts.append(f"k*({q_i}*{q_j}*({dy}))/({r2})^(3/2)")
        
        Fx_str = " + ".join(Fx_bieu_thuc_parts) if Fx_bieu_thuc_parts else "0"
        Fy_str = " + ".join(Fy_bieu_thuc_parts) if Fy_bieu_thuc_parts else "0"
        
        ket_qua[i + 1] = {
            'Fx_txt': Fx_str,
            'Fy_txt': Fy_str,
            'Fx_val': Fx_so,
            'Fy_val': Fy_so
        }
        
    return ket_qua

# ==========================================
# NHẬP DỮ LIỆU TỪ NGƯỜI DÙNG
# ==========================================
def nhap_du_lieu():
    danh_sach = []
    print("=== CHƯƠNG TRÌNH TÍNH LỰC TƯƠNG TÁC TĨNH ĐIỆN ===")
    try:
        n = int(input("Nhập số lượng điện tích trong hệ: "))
        if n < 2:
            print("Hệ thống cần ít nhất 2 điện tích để tính lực tương tác!")
            return []
            
        for i in range(n):
            print(f"\n--- Nhập thông tin cho điện tích q{i+1} ---")
            q = float(input(f"  Nhập giá trị q{i+1} (Coulomb, ví dụ 2e-6 hoặc 0.000002): "))
            x = float(input(f"  Nhập tọa độ x{i+1} (mét): "))
            y = float(input(f"  Nhập tọa độ y{i+1} (mét): "))
            danh_sach.append({'q': q, 'x': x, 'y': y})
            
    except ValueError:
        print("Lỗi: Vui lòng nhập vào một số hợp lệ!")
        return []
        
    return danh_sach

# Chạy chương trình
if __name__ == "__main__":
    he_dien_tich = nhap_du_lieu()
    
    if he_dien_tich:
        ket_qua_tinh = tinh_luc_he_dien_tich(he_dien_tich)

        print("\n====== KẾT QUẢ TÍNH LỰC ĐIỆN TÁC DỤNG TỪNG ĐIỆN TÍCH ======\n")
        for dien_tich_id, luc in ket_qua_tinh.items():
            print(f"--- Điện tích q{dien_tich_id} ---")
            print(f"+ Biểu thức Fx = {luc['Fx_txt']}")
            print(f"+ Biểu thức Fy = {luc['Fy_txt']}")
            print(f"=> Giá trị số: Fx = {luc['Fx_val']:.4f} N | Fy = {luc['Fy_val']:.4f} N\n")
