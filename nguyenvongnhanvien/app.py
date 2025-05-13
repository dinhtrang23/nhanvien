import streamlit as st
from openpyxl import Workbook

# Đọc mật khẩu admin từ file
def read_admin_password():
    try:
        with open("admin_password.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "admin123"  # Mặc định nếu không tìm thấy file

# Cập nhật mật khẩu admin vào file
def update_admin_password(new_password):
    with open("admin_password.txt", "w") as f:
        f.write(new_password)

# Thiết lập cấu hình trang
st.set_page_config(page_title="Đăng ký lịch làm việc", layout="centered")
st.title("📅 Đăng ký lịch làm việc theo tuần")

# Đọc danh sách nhân viên từ file nhan_vien.txt
try:
    with open("nhan_vien.txt", "r", encoding="utf-8") as f:
        danh_sach_nhan_vien = [ten.strip() for ten in f.readlines() if ten.strip()]
except FileNotFoundError:
    st.error("❌ Không tìm thấy file nhan_vien.txt. Vui lòng tạo file này trước.")
    st.stop()

# Cấu hình cơ bản
thu_trong_tuan = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
so_tuan = 4

# Dữ liệu lưu đăng ký
schedule_data = {}

# Giao diện đăng ký lịch làm việc cho nhân viên
st.header("📝 Chọn lịch làm việc")

# Chức năng cho nhân viên chọn lịch làm việc
for ten in danh_sach_nhan_vien:
    with st.expander(f"👤 {ten}"):
        lich = {}
        for tuan in range(1, so_tuan + 1):
            st.markdown(f"#### 📆 Tuần {tuan}")
            cols = st.columns(7)
            for i, thu in enumerate(thu_trong_tuan):
                with cols[i]:
                    gio_bat_dau = st.time_input(f"Bắt đầu {thu}", value=None, key=f"{ten}_T{tuan}_{thu}_start")
                    gio_ket_thuc = st.time_input(f"Kết thúc {thu}", value=None, key=f"{ten}_T{tuan}_{thu}_end")
                    
                    if gio_bat_dau and gio_ket_thuc:
                        # Nếu chọn giờ, đánh dấu là làm việc (L)
                        lich[f"Tuần {tuan} - {thu}"] = f"{gio_bat_dau} - {gio_ket_thuc}"
                    else:
                        # Nếu không chọn giờ thì mặc định là nghỉ (H)
                        lich[f"Tuần {tuan} - {thu}"] = "H"
        schedule_data[ten] = lich

# Chức năng admin cho phép chỉnh sửa lịch và trạng thái nghỉ việc đột xuất
admin_password = read_admin_password()
input_password = st.text_input("🔒 Mật khẩu Admin", type="password")

if input_password == admin_password:  # Kiểm tra mật khẩu Admin từ file
    st.success("Bạn đã đăng nhập với quyền Admin")
    st.header("⚙️ Quản lý lịch làm việc")

    # Admin có thể chỉnh sửa lịch của nhân viên
    for ten in danh_sach_nhan_vien:
        with st.expander(f"Chỉnh sửa lịch làm việc của {ten}"):
            lich = schedule_data[ten]
            for tuan in range(1, so_tuan + 1):
                st.markdown(f"#### 📆 Tuần {tuan}")
                cols = st.columns(7)
                for i, thu in enumerate(thu_trong_tuan):
                    with cols[i]:
                        gio_bat_dau = st.time_input(f"Bắt đầu {thu}", value=None, key=f"{ten}_T{tuan}_{thu}_start", disabled=False)
                        gio_ket_thuc = st.time_input(f"Kết thúc {thu}", value=None, key=f"{ten}_T{tuan}_{thu}_end", disabled=False)
                        
                        if gio_bat_dau and gio_ket_thuc:
                            # Nếu chọn giờ, đánh dấu là làm việc (L)
                            lich[f"Tuần {tuan} - {thu}"] = f"{gio_bat_dau} - {gio_ket_thuc}"
                        else:
                            # Nếu không chọn giờ thì mặc định là nghỉ (H)
                            lich[f"Tuần {tuan} - {thu}"] = "H"
            schedule_data[ten] = lich

    # Thay đổi mật khẩu admin
    st.header("🔑 Thay đổi mật khẩu Admin")
    new_password = st.text_input("Mật khẩu mới", type="password")
    if st.button("Lưu mật khẩu mới"):
        if new_password:
            update_admin_password(new_password)
            st.success("Mật khẩu mới đã được lưu!")
        else:
            st.error("Vui lòng nhập mật khẩu mới.")
else:
    st.warning("🔑 Bạn chưa nhập mật khẩu Admin đúng.")

# Hàm xuất Excel chia sheet theo tuần
def export_excel_multi_sheet(schedule_data):
    wb = Workbook()
    wb.remove(wb.active)  # Xoá sheet mặc định

    for tuan in range(1, 5):
        sheet = wb.create_sheet(title=f"Tuần {tuan}")
        sheet.append(["Họ tên"] + thu_trong_tuan)

        for ten, lich in schedule_data.items():
            row = [ten]
            for thu in thu_trong_tuan:
                # Nếu có giờ làm việc thì điền giờ, nếu không có giờ thì ghi "Nghỉ"
                row.append(lich.get(f"Tuần {tuan} - {thu}", "H"))
            sheet.append(row)

    file_path = "lich_lam_viec_tuan.xlsx"
    wb.save(file_path)
    return file_path

# Nút tải file Excel
if st.button("📥 Tải xuống lịch làm việc"):
    file_path = export_excel_multi_sheet(schedule_data)
    with open(file_path, "rb") as f:
        st.download_button(
            label="⬇️ Nhấn để tải Excel",
            data=f,
            file_name="lich_lam_viec.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
