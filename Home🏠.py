import streamlit as st
import requests
from streamlit_lottie import st_lottie

# ====== หน้า Home ======
st.set_page_config(page_title="Home", page_icon="🏠", layout="centered")

# Title
st.title("ระเบียบวิธีแก้ตำแหน่งผิด 📝")
st.write("โปรแกรมนี้ช่วยคำนวณรากสมการด้วยวิธี **False Position Method** พร้อมแสดงผลกราฟและขั้นตอนการคำนวณ")

# Lottie Animation (ฝังจาก URL)
st.markdown("""
<lottie-player src="https://assets10.lottiefiles.com/packages/lf20_ddca4e64.json" background="transparent" speed="1" loop autoplay style="width: 100%; height: 200px;"></lottie-player>
""", unsafe_allow_html=True)

# ปุ่มลิงก์หน้าอื่น
st.markdown("### เริ่มใช้งาน:")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/หน้าการคำนวณ💻.py", label="หน้าการคำนวณ", icon="💻")
with col2:
    st.page_link("pages/คู่มือ🔍.py", label="คู่มือ", icon="🔍")
with col3:
    st.markdown("[🌎 Google](http://www.google.com)")

# คำแนะนำเบื้องต้น
st.info("📌 เลือกหน้าการคำนวณเพื่อเริ่มหาค่ารากสมการ หรือดูคู่มือเพื่อเรียนรู้วิธีใช้งานโปรแกรม")
