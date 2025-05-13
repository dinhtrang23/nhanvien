import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

# Hàm kiểm tra và lưu lịch làm việc vào file Excel
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
                gio_bat_dau = st.time_input(f"Bắt đầu {thu}", value=None, key=f"{ten_nhan_vien}_{thu}_start_{str(hash(ten_nhan_vien))}")

            with col2:
                gio_ket_thuc = st.time_input(f"Kết thúc {thu}", value=None, key=f"{ten_nhan_vien}_{thu}_end_{str(hash(ten_nhan_vien))}")

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

# Trang đăng nhập admin
def admin_login():
    admin_username = st.text_input("Nhập tên đăng nhập admin:")
    admin_password = st.text_input("Nhập mật khẩu admin:", type="password")

    if admin_username == "admin" and admin_password == "admin":
        st.success("Đăng nhập thành công!")
        return True
    else:
        st.error("Sai tên đăng nhập hoặc mật khẩu.")
        return False

# Trang chính
def main():
    st.title("Ứng dụng Quản Lý Lịch Làm Việc")

    if admin_login():
        create_schedule()

if __name__ == "__main__":
    main()
