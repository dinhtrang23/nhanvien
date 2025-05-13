import streamlit as st
import pandas as pd
from datetime import datetime

# Mật khẩu admin
admin_username = "admin"
admin_password = "admin123"

# Hàm lưu lịch làm việc vào file Excel
def save_schedule_to_excel(schedule, filename="lich_lam_viec.xlsx"):
    df = pd.DataFrame(schedule)
    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Lịch Làm Việc")

# Hàm tạo lịch làm việc cho nhân viên
def create_schedule():
    # Nhập tên nhân viên
    ten_nhan_vien = st.text_input("Nhập tên nhân viên:")

    if ten_nhan_vien:
        # Lưu lịch làm việc theo tên nhân viên
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
            save_schedule_to_excel(lich)
            st.success("Lịch làm việc đã được lưu vào file Excel.")
    else:
        st.warning("Vui lòng nhập tên nhân viên để tạo lịch.")

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
