import streamlit as st
import json
import os
from datetime import datetime

# Path aman untuk menyimpan file JSON di folder yang sama
DATA_FILE = os.path.join(os.path.dirname(__file__), "todo_data.json")

# Fungsi untuk load data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Fungsi untuk save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Inisialisasi session state
if "todo_list" not in st.session_state:
    st.session_state.todo_list = load_data()

st.title("📝 To-Do List Sederhana")

# Input user
new_task = st.text_input("Tambahkan tugas baru:")
deadline = st.date_input("Deadline tugas (opsional):")
category = st.selectbox("Kategori:", ["Penting", "Biasa", "Santai"])

# Tombol Tambah & Hapus sejajar
col_tambah, col_hapus = st.columns([2, 1])

with col_tambah:
    if st.button("➕ Tambah"):
        if new_task.strip():
            st.session_state.todo_list.append({
                "task": new_task,
                "done": False,
                "deadline": str(deadline),
                "category": category
            })
            save_data(st.session_state.todo_list)
        else:
            st.warning("Tugas tidak boleh kosong!")

with col_hapus:
    if st.button("🗑 Hapus yang sudah selesai"):
        st.session_state.todo_list = [item for item in st.session_state.todo_list if not item["done"]]
        save_data(st.session_state.todo_list)

# Daftar tugas
# ⬇️ Tambahkan ini sebelum menampilkan daftar tugas
st.markdown("---")
st.markdown("### 🔍 Filter Tugas")

filter_status = st.selectbox("Status:", ["Semua", "Selesai", "Belum selesai"])
filter_kategori = st.selectbox("Kategori:", ["Semua", "Penting", "Biasa", "Santai"])

st.subheader("Daftar Tugas:")

# Terapkan filter
filtered_list = []
for item in st.session_state.todo_list:
    status_sesuai = (
        (filter_status == "Semua") or
        (filter_status == "Selesai" and item["done"]) or
        (filter_status == "Belum selesai" and not item["done"])
    )
    kategori_sesuai = (
        (filter_kategori == "Semua") or
        (item.get("category", "-") == filter_kategori)
    )
    if status_sesuai and kategori_sesuai:
        filtered_list.append(item)

# Tampilkan tugas yang lolos filter
for i, item in enumerate(filtered_list):

    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        checkbox = st.checkbox("", key=f"check_{i}", value=item["done"])
    with col2:
        # Hari dan bulan versi Indonesia
        indo_days = {
            "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
            "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
        }

        indo_months = {
            "January": "Januari", "February": "Februari", "March": "Maret",
            "April": "April", "May": "Mei", "June": "Juni", "July": "Juli",
            "August": "Agustus", "September": "September", "October": "Oktober",
            "November": "November", "December": "Desember"
        }

        if "deadline" in item and item["deadline"] != "-":
            try:
                date_obj = datetime.strptime(item["deadline"], "%Y-%m-%d")
                hari = indo_days.get(date_obj.strftime("%A"), date_obj.strftime("%A"))
                bulan = indo_months.get(date_obj.strftime("%B"), date_obj.strftime("%B"))
                tanggal = f"{date_obj.day} {bulan} {date_obj.year}"
                deadline_str = f"{hari}, {tanggal}"
            except:
                deadline_str = item["deadline"]
        else:
            deadline_str = "-"

        category_str = item.get("category", "-")

        # Warna berdasarkan kategori
        warna = {
            "Penting": "red",
            "Biasa": "orange",
            "Santai": "green"
        }.get(category_str, "white")

        task_display = f"""
        <div style="border-left: 6px solid {warna}; padding-left: 10px;">
        📌 <strong>{item['task']}</strong><br>
        🗂️ <span style='color:{warna}; font-weight:bold;'>{category_str}</span> | ⏰ {deadline_str}
        </div>
        """

        if checkbox:
            st.markdown(f"<s>{task_display}</s>", unsafe_allow_html=True)
        else:
            st.markdown(task_display, unsafe_allow_html=True)

    st.session_state.todo_list[i]["done"] = checkbox

# Simpan saat ada perubahan
save_data(st.session_state.todo_list)
