
import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

FILE_NAME = "nguyen_vong.xlsx"
ADMIN_FILE = "admin_pass.txt"

def lay_mat_khau_admin():
    if not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "w") as f:
            f.write("1234")  # mật khẩu mặc định
    with open(ADMIN_FILE, "r") as f:
        return f.read().strip()

def doi_mat_khau_admin(mat_khau_moi):
    with open(ADMIN_FILE, "w") as f:
        f.write(mat_khau_moi)

def tao_file_excel():
    df = pd.DataFrame(columns=["Họ tên", "Thứ", "Ngày", "Giờ bắt đầu", "Giờ kết thúc"])
    df.to_excel(FILE_NAME, index=False)

def ghi_du_lieu(ho_ten, du_lieu):
    if not os.path.exists(FILE_NAME):
        tao_file_excel()
    df = pd.read_excel(FILE_NAME)
    df = df[df["Họ tên"] != ho_ten]
    df = pd.concat([df, pd.DataFrame(du_lieu)], ignore_index=True)
    df.to_excel(FILE_NAME, index=False)

def hien_thi_form_tuan():
    st.title("📝 Đăng ký nguyện vọng làm việc trong tuần")
    ho_ten = st.selectbox("Chọn tên của bạn", doc_danh_sach_nhan_vien())

    ngay_hom_nay = datetime.today()
    thu_trong_tuan = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
    du_lieu_gui = []

    for i in range(7):
        ngay = ngay_hom_nay + timedelta(days=(i - ngay_hom_nay.weekday()) % 7 + i // 7 * 7)
        with st.expander(f"{thu_trong_tuan[i]} - {ngay.strftime('%d/%m/%Y')}"):
            gio_bat_dau = st.time_input(f"Giờ bắt đầu ({thu_trong_tuan[i]})", key=f"bat_dau_{i}")
            gio_ket_thuc = st.time_input(f"Giờ kết thúc ({thu_trong_tuan[i]})", key=f"ket_thuc_{i}")
            if gio_bat_dau != gio_ket_thuc:
                du_lieu_gui.append({
                    "Họ tên": ho_ten,
                    "Thứ": thu_trong_tuan[i],
                    "Ngày": ngay.strftime("%d/%m/%Y"),
                    "Giờ bắt đầu": gio_bat_dau.strftime("%H:%M"),
                    "Giờ kết thúc": gio_ket_thuc.strftime("%H:%M")
                })

    if st.button("✅ Gửi nguyện vọng"):
        if du_lieu_gui:
            ghi_du_lieu(ho_ten, du_lieu_gui)
            st.success("Đã gửi nguyện vọng thành công!")
        else:
            st.warning("Bạn chưa chọn giờ làm ngày nào!")

def doc_danh_sach_nhan_vien():
    try:
        with open("nhan_vien.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["Nguyễn Văn A", "Trần Thị B"]

# --- Giao diện chính ---
hien_thi_form_tuan()

# --- KHU VỰC ADMIN: xem và xóa dữ liệu ---
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
