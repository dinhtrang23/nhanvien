import streamlit as st
from openpyxl import Workbook

st.set_page_config(page_title="Lịch làm việc", layout="centered")

st.title("📅 Ứng dụng đăng ký lịch làm việc theo tuần")

# Đọc danh sách nhân viên từ file nhan_vien.txt
try:
    with open("nhan_vien.txt", "r", encoding="utf-8") as f:
        danh_sach_nhan_vien = [ten.strip() for ten in f.readlines() if ten.strip()]
except FileNotFoundError:
    st.error("⚠️ Không tìm thấy file nhan_vien.txt. Vui lòng tạo file này trước.")
    st.stop()

# Cấu hình cơ bản
thu_trong_tuan = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
so_tuan = 4

schedule_data = {}

st.header("Chọn lịch làm việc")

# Giao diện chọn lịch cho từng nhân viên
for ten in danh_sach_nhan_vien:
    with st.expander(f"🧑 {ten}"):
        lich = {}
        for tuan in range(1, so_tuan + 1):
            st.markdown(f"### Tuần {tuan}")
            cols = st.columns(7)
            for i, thu in enumerate(thu_trong_tuan):
                with cols[i]:
                    ca = st.selectbox(
                        f"{thu}",
                        ["", "Làm (L)", "Nghỉ (H)"],
                        key=f"{ten}_T{tuan}_{thu}"
                    )
                    key = f"Tuần {tuan} - {thu}"
                    # Mặc định là "H" nếu không chọn gì
                    lich[key] = "L" if "Làm" in ca else "H"
        schedule_data[ten] = lich

# Hàm xuất Excel chia sheet theo tuần
def export_excel_multi_sheet(schedule_data):
    wb = Workbook()
    wb.remove(wb.active)
    for tuan in range(1, 5):
        sheet = wb.create_sheet(title=f"Tuần {tuan}")
        sheet.append(["Họ tên"] + thu_trong_tuan)
        for ten, lich in schedule_data.items():
            row = [ten]
            for thu in thu_trong_tuan:
                row.append(lich.get(f"Tuần {tuan} - {thu}", "H"))
            sheet.append(row)
    file_path = "lich_lam_viec_tung_tuan.xlsx"
    wb.save(file_path)
    return file_path

# Nút tải xuống file Excel
if st.button("📥 Tải xuống lịch làm việc chia theo tuần"):
    file_path = export_excel_multi_sheet(schedule_data)
    with open(file_path, "rb") as f:
        st.download_button("Tải file Excel", f, file_name="lich_lam_viec.xlsx")
