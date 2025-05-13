import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

FILE_NAME = "nguyen_vong.xlsx"
ADMIN_FILE = "admin_pass.txt"

def lay_mat_khau_admin():
    if not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "w") as f:
            f.write("1234")
    with open(ADMIN_FILE, "r") as f:
        return f.read().strip()

def doi_mat_khau_admin(mat_khau_moi):
    with open(ADMIN_FILE, "w") as f:
        f.write(mat_khau_moi)

def tao_file_excel():
    # Tạo cấu trúc file Excel với các thứ trong tuần theo hàng ngang
    columns = ["Họ tên", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
    df = pd.DataFrame(columns=columns)
    df.to_excel(FILE_NAME, index=False)

def ghi_du_lieu(ho_ten, du_lieu):
    if not os.path.exists(FILE_NAME):
        tao_file_excel()
    df = pd.read_excel(FILE_NAME)

    # Tìm dòng của nhân viên, nếu không có thì thêm mới
    if ho_ten not in df["Họ tên"].values:
        df = pd.concat([df, pd.DataFrame([[ho_ten] + [""]*7], columns=df.columns)], ignore_index=True)

    for i, thu in enumerate(["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]):
        # Lưu giờ vào cột tương ứng
        gio_bat_dau, gio_ket_thuc = du_lieu.get(thu, ("", ""))
        df.loc[df["Họ tên"] == ho_ten, thu] = f"{gio_bat_dau}-{gio_ket_thuc}" if gio_bat_dau and gio_ket_thuc else "Nghỉ"

    df.to_excel(FILE_NAME, index=False)

def hien_thi_form_tuan():
    st.title("📝 Đăng ký nguyện vọng làm việc trong tuần")
    ho_ten = st.selectbox("Chọn tên của bạn", doc_danh_sach_nhan_vien())

    ngay_hom_nay = datetime.today()
    thu_trong_tuan = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
    du_lieu_gui = {}

    for i in range(7):
        ngay = ngay_hom_nay + timedelta(days=(i - ngay_hom_nay.weekday()) % 7 + i // 7 * 7)
        with st.expander(f"{thu_trong_tuan[i]} - {ngay.strftime('%d/%m/%Y')}"):
            gio_bat_dau = st.time_input(f"Giờ bắt đầu ({thu_trong_tuan[i]})", key=f"bat_dau_{i}")
            gio_ket_thuc = st.time_input(f"Giờ kết thúc ({thu_trong_tuan[i]})", key=f"ket_thuc_{i}")
            du_lieu_gui[thu_trong_tuan[i]] = (gio_bat_dau.strftime("%H:%M") if gio_bat_dau else "", 
                                              gio_ket_thuc.strftime("%H:%M") if gio_ket_thuc else "")

    if st.button("✅ Gửi nguyện vọng"):
        ghi_du_lieu(ho_ten, du_lieu_gui)
        st.success("Đã gửi nguyện vọng thành công!")

def doc_danh_sach_nhan_vien():
    try:
        with open("nhan_vien.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["Nguyễn Văn A", "Trần Thị B"]

# --- Giao diện chính ---
hien_thi_form_tuan()

# --- KHU VỰC ADMIN ---
st.markdown("---")
st.subheader("🔐 Khu vực Admin")

with st.expander("Đăng nhập admin"):
    admin_password = lay_mat_khau_admin()
    password = st.text_input("Nhập mật khẩu admin", type="password")

    if password == admin_password:
        st.success("✅ Đăng nhập thành công!")
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "rb") as f:
                st.download_button(
                    label="📁 Tải file Excel nguyện vọng",
                    data=f,
                    file_name=FILE_NAME,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        if st.button("🗑️ Xóa toàn bộ dữ liệu"):
            os.remove(FILE_NAME)
            tao_file_excel()
            st.warning("⚠️ Đã xóa toàn bộ dữ liệu nguyện vọng!")

        st.markdown("### 🔄 Đổi mật khẩu admin")
        mat_khau_moi = st.text_input("Nhập mật khẩu mới", type="password")
        mat_khau_xac_nhan = st.text_input("Nhập lại mật khẩu mới", type="password")
        if st.button("✅ Đổi mật khẩu"):
            if mat_khau_moi and mat_khau_moi == mat_khau_xac_nhan:
                doi_mat_khau_admin(mat_khau_moi)
                st.success("🔑 Đã đổi mật khẩu admin thành công!")
            else:
                st.error("❌ Mật khẩu không khớp hoặc rỗng!")
    elif password:
        st.error("❌ Mật khẩu sai. Vui lòng thử lại.")
"""

# Cập nhật lại file zip với app.py mới
zip_path = "/mnt/data/nguyen_vong_app_hang_ngang.zip"
with zipfile.ZipFile(zip_path, "w") as zipf:
    zipf.writestr("app.py", updated_app_py_code)
    zipf.writestr("nhan_vien.txt", nhan_vien_txt)
    zipf.writestr("requirements.txt", requirements_txt)

zip_path
