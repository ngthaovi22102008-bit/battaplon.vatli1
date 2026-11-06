import math
import sympy as sp
import matplotlib.pyplot as plt

def tinh_luc_he_dien_tich(danh_sach_dien_tich):
    n = len(danh_sach_dien_tich)
    k_sym = sp.Symbol('k')
    k_val = 9e9
    ket_qua = {}
    
    for i in range(n):
        q_i = danh_sach_dien_tich[i]['q']
        x_i = danh_sach_dien_tich[i]['x']
        y_i = danh_sach_dien_tich[i]['y']
        
        Fx_expr, Fy_expr = 0, 0
        Fx_val, Fy_val = 0.0, 0.0
        
        for j in range(n):
            if i == j:
                continue
            q_j = danh_sach_dien_tich[j]['q']
            x_j = danh_sach_dien_tich[j]['x']
            y_j = danh_sach_dien_tich[j]['y']
            
            dx = x_i - x_j
            dy = y_i - y_j
            r2 = dx**2 + dy**2
            
            if r2 > 0:
                r = math.sqrt(r2)
                r3 = r2 * r
                
                # Giá trị số
                f_x = k_val * (q_i * q_j * dx) / r3
                f_y = k_val * (q_i * q_j * dy) / r3
                Fx_val += f_x
                Fy_val += f_y
                
                # Biểu thức SymPy
                Fx_expr += k_sym * (q_i * q_j * dx) / (r2 ** sp.Rational(3, 2))
                Fy_expr += k_sym * (q_i * q_j * dy) / (r2 ** sp.Rational(3, 2))
        
        F_total = math.hypot(Fx_val, Fy_val)
        goc_do = math.degrees(math.atan2(Fy_val, Fx_val)) % 360

        ket_qua[i + 1] = {
            'Fx_expr': sp.simplify(Fx_expr),
            'Fy_expr': sp.simplify(Fy_expr),
            'Fx_val': Fx_val,
            'Fy_val': Fy_val,
            'F_total': F_total,
            'goc_do': goc_do
        }
        
    return ket_qua

# ==========================================
# HÀM VẼ ĐỒ THỊ VECTƠ LỰC
# ==========================================
def ve_so_do_dien_tich(danh_sach, ket_qua):
    plt.figure(figsize=(8, 8))
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    
    # Tìm lực tổng đại diện để chuẩn hóa chiều dài mũi tên vẽ
    max_F = max([item['F_total'] for item in ket_qua.values()])
    scale_length = 1.0  # Độ dài mũi tên trên đồ thị
    
    for i, dt in enumerate(danh_sach):
        q, x, y = dt['q'], dt['x'], dt['y']
        dt_id = i + 1
        luc = ket_qua[dt_id]
        
        # 1. Vẽ vị trí điện tích (Dương: Đỏ, Âm: Xanh)
        color = 'red' if q > 0 else 'blue'
        symbol = '+' if q > 0 else '-'
        plt.scatter(x, y, color=color, s=400, zorder=3, edgecolors='black')
        plt.text(x, y, f"$q_{{{dt_id}}}$\n({symbol})", color='white', weight='bold', 
                 fontsize=9, ha='center', va='center', zorder=4)
        
        # 2. Vẽ Vectơ Tổng lực F tác dụng lên điện tích
        if luc['F_total'] > 0 and max_F > 0:
            # Chuẩn hóa độ dài mũi tên để không bị quá dài/ngắn trên tọa độ
            dx_vec = (luc['Fx_val'] / max_F) * scale_length
            dy_vec = (luc['Fy_val'] / max_F) * scale_length
            
            plt.quiver(x, y, dx_vec, dy_vec, angles='xy', scale_units='xy', scale=1, 
                       color='darkgreen', width=0.008, zorder=5)
            
            # Ghi chú thích tổng lực F cạnh mũi tên
            plt.text(x + dx_vec * 1.15, y + dy_vec * 1.15, 
                     f"$\vec{{F}}_{{{dt_id}}}$ = {luc['F_total']:.2e} N", 
                     color='darkgreen', fontsize=10, weight='bold')

    plt.grid(True, linestyle=':', alpha=0.6)
    plt.xlabel('Tọa độ X (m)')
    plt.ylabel('Tọa độ Y (m)')
    plt.title('SƠ ĐỒ HỆ ĐIỆN TÍCH VÀ VECTƠ TỔNG LỰC CÂN BẰNG', fontsize=12, weight='bold')
    plt.axis('equal')  # Giữ tỉ lệ 1:1 cho trục X và Y
    plt.show()

# ==========================================
# CHƯƠNG TRÌNH CHÍNH
# ==========================================
def nhap_du_lieu_mau():
    # Dữ liệu mẫu (3 điện tích xếp thành tam giác) để test nhanh
    return [
        {'q': 2e-6,  'x': 0.0, 'y': 0.0},   # q1 dương ở gốc tọa độ
        {'q': -4e-6, 'x': 3.0, 'y': 0.0},   # q2 âm ở (3, 0)
        {'q': 3e-6,  'x': 1.5, 'y': 2.0}    # q3 dương ở (1.5, 2)
    ]

if __name__ == "__main__":
    print("Đang chạy tính toán với dữ liệu hệ 3 điện tích mẫu...")
    he_dien_tich = nhap_du_lieu_mau()
    
    ket_qua_tinh = tinh_luc_he_dien_tich(he_dien_tich)

    # In thông số số liệu
    for dt_id, luc in ket_qua_tinh.items():
        print(f"q{dt_id}: Fx = {luc['Fx_val']:.4e} N | Fy = {luc['Fy_val']:.4e} N | F_tổng = {luc['F_total']:.4e} N")

    # Gọi hàm vẽ hình
    ve_so_do_dien_tich(he_dien_tich, ket_qua_tinh)
