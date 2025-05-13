import streamlit as st
import pandas as pd
from datetime import datetime

# Mật khẩu admin
admin_username = "admin"
admin_password = "admin123"

# Hàm đọc tên nhân viên từ file nhan_vien.txt
def get_employee_names(filename="nhan_vien.txt"):
    try:
        with open(filename, "r") as file:
            # Đọc danh sách tên nhân viên từ file, mỗi tên 1 dòng
            employees = file.readlines()
        # Loại bỏ ký tự newline và trả về danh sách tên nhân viên
        return [name.strip() for name in employees]
    except FileNotFoundError:
        st.error(f"Không tìm thấy file {filename}.")
        return []

# Hàm lưu lịch làm việc vào file Excel
def save_schedule_to_excel(schedule, filename="lich_lam_viec.xlsx"):
    # Chuyển lịch làm việc thành DataFrame
    df = pd.DataFrame(schedule)
    
    # Kiểm tra xem file Excel đã tồn tại chưa
    try:
        # Nếu file đã tồn tại, mở file và thêm dữ liệu vào
        with pd.ExcelWriter(filename, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, index=False, sheet_name="Lịch Làm Việc")
    except FileNotFoundError:
        # Nếu file chưa tồn tại, tạo mới file Excel
        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Lịch Làm Việc")

# Hàm tạo lịch làm việc cho nhân viên
def create_schedule():
    # Lấy danh sách nhân viên từ file nhan_vien.txt
    employee_names = get_employee_names()

    if employee_names:
        # Cho nhân viên chọn tên từ danh sách đã lấy từ file
        ten_nhan_vien = st.selectbox("Chọn tên nhân viên:", employee_names)

        # Lưu lịch làm việc theo tên nhân viên
        if ten_nhan_vien:
            lich = {}

            # Lặp qua các ngày trong tuần
            for thu in ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]:
                col1, col2 = st.columns(2)

                with col1:
                    gio_bat_dau = st.time_input(f"Bắt đầu {thu}", value=None, key=f"{ten_nhan_vien}_{thu}_start")

                with col2:
                    gio_ket_thuc = st.time_input(f"Kết thúc {thu}", value=None, key=f"{ten_nhan_vien}_{thu}_end")

                if gio_bat_dau and gio_ket_thuc:
                    # Nếu chọn giờ, đánh dấu là làm việc (L)
                    lich[thu] = f"{gio_bat_dau} - {gio_ket_thuc}"
                else:
                    # Nếu không chọn giờ thì mặc định là nghỉ (H)
                    lich[thu] = "H"
            
            # Hiển thị lịch làm việc và lưu vào Excel
            st.write(f"Lịch làm việc của {ten_nhan_vien}:")
            st.write(lich)

            # Lưu lịch vào Excel
            if st.button("Lưu lịch"):
                # Chuyển lịch làm việc thành DataFrame và lưu vào Excel
                schedule = {"Nhân viên": [ten_nhan_vien] * len(lich), "Ngày": list(lich.keys()), "Lịch làm việc": list(lich.values())}
                save_schedule_to_excel(schedule)
                st.success("Lịch làm việc đã được lưu vào file Excel.")
    else:
        st.warning("Không có nhân viên nào trong danh sách.")

# Hàm cho đăng nhập admin
def admin_login():
    st.subheader("Đăng nhập Admin")

    # Nhập tên đăng nhập và mật khẩu
    username = st.text_input("Tên đăng nhập:")
    password = st.text_input("Mật khẩu:", type="password")

    if st.button("Đăng nhập"):
        if username == admin_username and password == admin_password:
            st.success("Đăng nhập thành công!")
            return True
        else:
            st.error("Tên đăng nhập hoặc mật khẩu không đúng.")
            return False

    return False

# Hàm cho trang đăng ký lịch làm việc của nhân viên
def employee_schedule():
    st.title("Trang Đăng Ký Lịch Làm Việc Cho Nhân Viên")
    create_schedule()

# Hàm chính
def main():
    # Giao diện chọn login admin hoặc nhân viên
    login_type = st.radio("Chọn vai trò", ("Nhân viên", "Admin"))

    if login_type == "Admin":
        # Admin đăng nhập
        if admin_login():
            st.subheader("Admin Trang Quản Lý")
            st.write("Tại đây admin có thể chỉnh sửa lịch làm việc của nhân viên.")
            # Thêm tính năng quản lý admin tại đây (ví dụ: xem lịch làm việc, chỉnh sửa, v.v...)
    elif login_type == "Nhân viên":
        # Nhân viên đăng ký lịch làm việc
        employee_schedule()

if __name__ == "__main__":
    main()
