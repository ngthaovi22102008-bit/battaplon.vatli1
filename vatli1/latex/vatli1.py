import math
from pathlib import Path
import sympy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.transforms import blended_transform_factory
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
        Fx_components = []
        Fy_components = []
        
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
                fx_component = k_sym * (q_i * q_j * dx) / (r2 ** sp.Rational(3, 2))
                fy_component = k_sym * (q_i * q_j * dy) / (r2 ** sp.Rational(3, 2))
                Fx_expr += fx_component
                Fy_expr += fy_component
                component_id = len(Fx_components) + 1
                Fx_components.append({
                    'name': f'Fx{component_id}',
                    'source_id': j + 1,
                    'expr': sp.simplify(fx_component),
                    'value': f_x,
                    'vector_x': f_x,
                    'vector_y': f_y
                })
                Fy_components.append({
                    'name': f'Fy{component_id}',
                    'source_id': j + 1,
                    'expr': sp.simplify(fy_component),
                    'value': f_y
                })
        
        F_total = math.hypot(Fx_val, Fy_val)
        goc_do = math.degrees(math.atan2(Fy_val, Fx_val)) % 360

        ket_qua[i + 1] = {
            'Fx_expr': sp.simplify(Fx_expr),
            'Fy_expr': sp.simplify(Fy_expr),
            'Fx_components': Fx_components,
            'Fy_components': Fy_components,
            'Fx_val': Fx_val,
            'Fy_val': Fy_val,
            'F_total': F_total,
            'goc_do': goc_do
        }
        
    return ket_qua

# ==========================================
# HÀM VẼ ĐỒ THỊ VECTƠ LỰC
# ==========================================
def ve_so_do_dien_tich(danh_sach, ket_qua, ten_tep='so_do_dien_tich.png'):
    fig, ax = plt.subplots(figsize=(20, 12))
    
    x_values = [dt['x'] for dt in danh_sach]
    y_values = [dt['y'] for dt in danh_sach]
    plot_span = max(
        max(x_values + [0]) - min(x_values + [0]),
        max(y_values + [0]) - min(y_values + [0])
    )
    if plot_span == 0:
        plot_span = 1.0
    max_vector_F = max(
        [
            item['F_total']
            for item in ket_qua.values()
        ] + [
            math.hypot(component['vector_x'], component['vector_y'])
            for item in ket_qua.values()
            for component in item['Fx_components']
        ],
        default=0.0
    )
    nearest_distances = []
    for i, dt in enumerate(danh_sach):
        distances = [
            math.hypot(dt['x'] - other['x'], dt['y'] - other['y'])
            for j, other in enumerate(danh_sach)
            if i != j and math.hypot(dt['x'] - other['x'], dt['y'] - other['y']) > 0
        ]
        if distances:
            nearest_distances.append(min(distances))
    typical_spacing = (
        sorted(nearest_distances)[len(nearest_distances) // 2]
        if nearest_distances else plot_span
    )
    arrow_length = min(plot_span * 0.4, typical_spacing * 0.6)
    force_scale = arrow_length / max_vector_F if max_vector_F > 0 else 0.0
    arrow_endpoints = []

    for i, dt in enumerate(danh_sach):
        for dt_ke in danh_sach[i + 1:]:
            plt.plot(
                [dt['x'], dt_ke['x']],
                [dt['y'], dt_ke['y']],
                color='gray',
                linestyle='--',
                linewidth=0.8,
                alpha=0.55,
                zorder=1
            )
    
    for i, dt in enumerate(danh_sach):
        q, x, y = dt['q'], dt['x'], dt['y']
        dt_id = i + 1
        luc = ket_qua[dt_id]

        scaled_components = [
            (
                component,
                component['vector_x'] * force_scale,
                component['vector_y'] * force_scale
            )
            for component in luc['Fx_components']
        ]
        resultant_dx = sum(dx for _, dx, _ in scaled_components)
        resultant_dy = sum(dy for _, _, dy in scaled_components)
        resultant_endpoint = (
            x + resultant_dx,
            y + resultant_dy
        )

        if len(scaled_components) == 2:
            component_endpoints = []
            for component, dx_component, dy_component in scaled_components:
                endpoint = (x + dx_component, y + dy_component)
                component_endpoints.append(endpoint)
                arrow_endpoints.append(endpoint)
                plt.quiver(
                    x, y, dx_component, dy_component,
                    angles='xy', scale_units='xy', scale=1,
                    color='#c2410c', alpha=0.9, width=0.0022,
                    headwidth=4, headlength=5, headaxislength=4, zorder=2
                )
            for endpoint in component_endpoints:
                plt.plot(
                    [endpoint[0], resultant_endpoint[0]],
                    [endpoint[1], resultant_endpoint[1]],
                    color='#c2410c',
                    linestyle=':',
                    linewidth=0.9,
                    alpha=0.7,
                    zorder=1
                )
        else:
            polygon_x, polygon_y = x, y
            for component, dx_component, dy_component in scaled_components:
                next_x = polygon_x + dx_component
                next_y = polygon_y + dy_component
                arrow_endpoints.append((next_x, next_y))
                plt.quiver(
                    polygon_x, polygon_y, dx_component, dy_component,
                    angles='xy', scale_units='xy', scale=1,
                    color='#c2410c', alpha=0.9, width=0.0022,
                    headwidth=4, headlength=5, headaxislength=4, zorder=2
                )
                polygon_x, polygon_y = next_x, next_y
            if len(scaled_components) > 2:
                plt.plot(
                    [polygon_x, x],
                    [polygon_y, y],
                    color='#c2410c',
                    linestyle=':',
                    linewidth=0.9,
                    alpha=0.7,
                    zorder=1
                )
        
        # 1. Vẽ vị trí điện tích (Dương: Đỏ, Âm: Xanh)
        color = 'red' if q > 0 else 'blue'
        plt.scatter(x, y, color=color, s=120, zorder=3, edgecolors='black', linewidths=0.8)
        plt.annotate(
            f"({x:g}; {y:g})",
            xy=(x, y),
            xytext=(0, 13),
            textcoords='offset points',
            ha='center',
            va='bottom',
            fontsize=10,
            color='black'
        )
        plt.annotate(
            rf"$q_{{{dt_id}}}$",
            xy=(x, y),
            xytext=(10, -5),
            textcoords='offset points',
            ha='left',
            va='top',
            fontsize=10,
            color=color
        )
        
        # 2. Vẽ Vectơ Tổng lực F tác dụng lên điện tích
        if math.hypot(resultant_dx, resultant_dy) > 0 and force_scale > 0:
            fy_operator = '+' if luc['Fy_val'] >= 0 else '-'
            dx_vec = resultant_dx
            dy_vec = resultant_dy
            arrow_endpoints.append((x + dx_vec, y + dy_vec))
            
            plt.quiver(
                x, y, dx_vec, dy_vec,
                angles='xy', scale_units='xy', scale=1,
                color='darkgreen', width=0.0028,
                headwidth=4, headlength=5, headaxislength=4, zorder=5
            )
            
            # Ghi chú thích tổng lực F cạnh mũi tên
            plt.annotate(
                rf"$\vec{{F}}_{{{dt_id}}}$",
                xy=(x + dx_vec, y + dy_vec),
                xytext=(12 if dx_vec >= 0 else -12, 12 if dy_vec >= 0 else -12),
                textcoords='offset points',
                ha='left' if dx_vec >= 0 else 'right',
                va='bottom' if dy_vec >= 0 else 'top',
                color='darkgreen',
                fontsize=9,
                weight='normal',
                bbox={'facecolor': 'white', 'edgecolor': 'none', 'alpha': 0.8, 'pad': 1.5},
                annotation_clip=False
            )

    plt.grid(True, linestyle=':', alpha=0.6)
    plt.xlabel('Tọa độ X (m)')
    plt.ylabel('Tọa độ Y (m)')
    ax.set_title(
        'SƠ ĐỒ HỆ ĐIỆN TÍCH VÀ VECTƠ TỔNG LỰC\n'
        '(Cam: lực thành phần; xanh lá: lực tổng hợp; nét đứt: nối điện tích)',
        fontsize=12,
        weight='bold'
    )
    ax.legend(
        handles=[
            Line2D([0], [0], color='#c2410c', linewidth=1.2, label='F nguồn→đích (ví dụ F₂→₁: q₂ tác dụng lên q₁)'),
            Line2D([0], [0], color='darkgreen', linewidth=1.2, label='Lực tổng hợp')
        ],
        loc='upper right',
        fontsize=9
    )
    all_x = [0] + x_values + [point[0] for point in arrow_endpoints]
    all_y = [0] + y_values + [point[1] for point in arrow_endpoints]
    padding = plot_span * 0.3
    x_min, x_max = min(all_x) - padding, max(all_x) + padding
    y_min, y_max = min(all_y) - padding, max(all_y) + padding
    y_span = y_max - y_min
    ax.set_position([0.05, 0.1, 0.68, 0.82])
    min_x_span = y_span * 1.4
    x_center = (x_min + x_max) / 2
    if x_max - x_min < min_x_span:
        x_min = x_center - min_x_span / 2
        x_max = x_center + min_x_span / 2
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal', adjustable='box')
    ax.axhline(0, color='black', linewidth=1.1, zorder=3)
    ax.axvline(0, color='black', linewidth=1.1, zorder=3)
    x_axis_transform = blended_transform_factory(ax.transAxes, ax.transData)
    y_axis_transform = blended_transform_factory(ax.transData, ax.transAxes)
    ax.annotate(
        '',
        xy=(1, 0),
        xytext=(0, 0),
        xycoords=x_axis_transform,
        textcoords=x_axis_transform,
        arrowprops={'arrowstyle': '->', 'color': 'black', 'linewidth': 1.2},
    )
    ax.annotate(
        '',
        xy=(0, 1),
        xytext=(0, 0),
        xycoords=y_axis_transform,
        textcoords=y_axis_transform,
        arrowprops={'arrowstyle': '->', 'color': 'black', 'linewidth': 1.2},
    )
    ax.annotate('x', xy=(1, 0), xycoords=x_axis_transform, xytext=(-5, 8),
                textcoords='offset points', ha='right', va='bottom', fontsize=12, weight='bold')
    ax.annotate('y', xy=(0, 1), xycoords=y_axis_transform, xytext=(8, -5),
                textcoords='offset points', ha='left', va='top', fontsize=12, weight='bold')
    fig.text(0.75, 0.88, 'LỰC TỔNG HỢP', fontsize=14, weight='bold', color='darkgreen')
    row_height = min(0.19, 0.7 / max(len(ket_qua), 1))
    for row, (dt_id, luc) in enumerate(ket_qua.items()):
        fy_operator = '+' if luc['Fy_val'] >= 0 else '-'
        component_sources = ', '.join(
            rf"$F_{{{c['source_id']}\to{dt_id}}}$"
            for c in luc['Fx_components']
        ) or 'Không có thành phần lực'
        y_text = 0.82 - row * row_height
        fig.text(
            0.75, y_text,
            f"q{dt_id} chịu các lực màu cam:\n{component_sources}",
            fontsize=11,
            color='#c2410c',
            va='top'
        )
        fig.text(
            0.75, y_text - 0.045,
            rf"$\vec{{F}}_{{{dt_id}}}=({luc['Fx_val']:.2e})\vec{{i}}"
            rf"{fy_operator}({abs(luc['Fy_val']):.2e})\vec{{j}}$",
            fontsize=11,
            color='darkgreen',
            va='top',
            bbox={'facecolor': 'white', 'edgecolor': 'none', 'alpha': 0.8, 'pad': 1}
        )
    output_path = Path(__file__).resolve().with_name(ten_tep)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Đã lưu hình tại: {output_path}")
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

# ==========================================
# NHẬP DỮ LIỆU TỪ NGƯỜI DÙNG
# ==========================================
def nhap_du_lieu():
    danh_sach = []
    print("=== CHƯƠNG TRÌNH TÍNH LỰC TƯƠNG TÁC TĨNH ĐIỆN ===")
    while True:
        try:
            n_nhap = float(input("Nhập số lượng điện tích trong hệ: ").strip().replace(",", "."))
            if not n_nhap.is_integer():
                print("Số lượng điện tích phải là số nguyên, ví dụ 3.")
                continue
            n = int(n_nhap)
            break
        except ValueError:
            print("Vui lòng nhập số lượng bằng số, ví dụ 3.")

    if n < 2:
        print("Hệ thống cần ít nhất 2 điện tích để tính lực tương tác!")
        return []

    def nhap_so(prompt):
        while True:
            try:
                return float(input(prompt).strip().replace(",", "."))
            except ValueError:
                print("Giá trị chưa hợp lệ; vui lòng nhập lại bằng số.")

    for i in range(n):
        print(f"\n--- Nhập thông tin cho điện tích q{i+1} ---")
        q = nhap_so(f"  Nhập giá trị q{i+1} (Coulomb, ví dụ 2e-6 hoặc 0.000002): ")
        x = nhap_so(f"  Nhập tọa độ x{i+1} (mét): ")
        y = nhap_so(f"  Nhập tọa độ y{i+1} (mét): ")
        danh_sach.append({'q': q, 'x': x, 'y': y})

    return danh_sach

# Chạy chương trình
if __name__ == "__main__":
    he_dien_tich = nhap_du_lieu()
    
    if he_dien_tich:
        ket_qua_tinh = tinh_luc_he_dien_tich(he_dien_tich)

        print("\n====== CÔNG THỨC TÍNH ======")
        print("Với điện tích q_i chịu lực do từng điện tích q_j tác dụng (j ≠ i):")
        print("r_ij = √[(x_i - x_j)² + (y_i - y_j)²]")
        print("Fx_{j→i} = k·q_i·q_j·(x_i - x_j) / r_ij³")
        print("Fy_{j→i} = k·q_i·q_j·(y_i - y_j) / r_ij³")
        print("Fx_i = tổng các Fx_{j→i}; Fy_i = tổng các Fy_{j→i}")
        print("F = √(Fx² + Fy²)")
        print("Kết quả dưới đây đã cộng các thành phần và tính độ lớn lực.\n")

        print("====== KẾT QUẢ TÍNH LỰC ĐIỆN TÁC DỤNG TỪNG ĐIỆN TÍCH ======\n")
        for dien_tich_id, luc in ket_qua_tinh.items():
            print(f"--- Điện tích q{dien_tich_id} ---")
            for component in luc['Fx_components']:
                component_label = f"Fx{component['source_id']}→{dien_tich_id}"
                print(
                    f"{component_label} (q{component['source_id']} tác dụng lên q{dien_tich_id}): "
                    f"{component['value']:.4e} N"
                )
            fx_sum = " + ".join(
                f"Fx{c['source_id']}→{dien_tich_id}" for c in luc['Fx_components']
            ) or "0"
            print(f"Fx = {fx_sum} = {luc['Fx_val']:.4e} N")

            for component in luc['Fy_components']:
                component_label = f"Fy{component['source_id']}→{dien_tich_id}"
                print(
                    f"{component_label} (q{component['source_id']} tác dụng lên q{dien_tich_id}): "
                    f"{component['value']:.4e} N"
                )
            fy_sum = " + ".join(
                f"Fy{c['source_id']}→{dien_tich_id}" for c in luc['Fy_components']
            ) or "0"
            print(f"Fy = {fy_sum} = {luc['Fy_val']:.4e} N")
            print(
                f"F = {luc['F_total']:.4e} N\n"
            )

        ve_so_do_dien_tich(he_dien_tich, ket_qua_tinh)
