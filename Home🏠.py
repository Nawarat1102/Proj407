import json
from streamlit_lottie import st_lottie
import streamlit as st

# ====== โหลดไฟล์ Lottie JSON ======
with open("Maths formula.json", "r", encoding="utf-8") as f:  # ใส่ path ให้ตรงกับไฟล์
    lottie_json = json.load(f)

# ====== หน้า Home ======
st.set_page_config(page_title="Home", page_icon="🏠", layout="centered")

st.title("ระเบียบวิธีแก้ตำแหน่งผิด 📝")
st.write("โปรแกรมนี้ช่วยคำนวณรากสมการด้วยวิธี False Position Method พร้อมแสดงผลกราฟและขั้นตอนการคำนวณ")

# แสดง Lottie Animation
st_lottie(lottie_json, height=200, key="home")

# ปุ่มลิงก์หน้าอื่น
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/หน้าการคำนวณ💻.py", label="หน้าการคำนวณ", icon="💻")
with col2:
    st.page_link("pages/คู่มือ🔍.py", label="คู่มือ", icon="🔍")
with col3:
    st.markdown("[🌎 Google](http://www.google.com)")

# คำแนะนำเบื้องต้น
st.info("📌 เลือกหน้าการคำนวณเพื่อเริ่มหาค่ารากสมการ หรือดูคู่มือเพื่อเรียนรู้วิธีใช้งานโปรแกรม")
