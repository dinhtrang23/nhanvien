import streamlit as st
import openpyxl
from openpyxl import Workbook
import os
from datetime import datetime, timedelta

FILE_NAME = "nguyen_vong.xlsx"
DS_NHAN_VIEN = "nhan_vien.txt"

def tao_file_excel():
    if not os.path.exists(FILE_NAME):
        wb = Workbook()
        ws = wb.active
        ws.title = "NguyenVong"
        header = ["Họ và tên", "Tuần bắt đầu", "Thứ", "Ngày", "Giờ làm", "Ghi chú", "Thời điểm gửi"]
        ws.append(header)
        wb.save(FILE_NAME)

def doc_danh_sach_nhan_vien():
    if not os.path.exists(DS_NHAN_VIEN):
        return []
    with open(DS_NHAN_VIEN, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def luu_nguyen_vong(ho_ten, tuan_bat_dau, thu, ngay, gio, ghi_chu):
    wb = openpyxl.load_workbook(FILE_NAME)
    ws = wb.active
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append([ho_ten, tuan_bat_dau.strftime("%Y-%m-%d"), thu, ngay.strftime("%Y-%m-%d"), gio, ghi_chu, now])
    wb.save(FILE_NAME)

def hien_thi_form_tuan():
    st.title("📋 Đăng ký nguyện vọng giờ làm theo tuần")

    danh_sach_nv = doc_danh_sach_nhan_vien()
    if not danh_sach_nv:
        st.error("⚠️ Chưa có danh sách nhân viên. Vui lòng tạo file 'nhan_vien.txt'")
        return

    ho_ten = st.selectbox("Chọn tên nhân viên", danh_sach_nv)

    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    tuan_bat_dau = st.date_input("Chọn tuần bắt đầu (Thứ 2)", value=monday)

    gio_lam_dict = {}

    with st.form("form_nguyen_vong_tuan"):
        for i in range(7):
            ngay = tuan_bat_dau + timedelta(days=i)
            thu = f"Thứ {i+2}" if i < 6 else "Chủ nhật"
            gio = st.time_input(f"{thu} ({ngay.strftime('%Y-%m-%d')})", value=datetime.strptime("08:00", "%H:%M").time())
            gio_lam_dict[i] = (thu, ngay, gio)

        ghi_chu = st.text_area("Ghi chú (nếu có)")
        submitted = st.form_submit_button("Gửi nguyện vọng")

        if submitted:
            for i in range(7):
                thu, ngay, gio = gio_lam_dict[i]
                luu_nguyen_vong(ho_ten, tuan_bat_dau, thu, ngay, gio.strftime("%H:%M"), ghi_chu)
            st.success("✅ Đã gửi nguyện vọng thành công cho cả tuần!")

# --- MAIN ---
tao_file_excel()
hien_thi_form_tuan()
