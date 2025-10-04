import streamlit as st
import requests
from streamlit_lottie import st_lottie

# ====== ฟังก์ชันโหลด Lottie จาก URL ======
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ====== หน้า Home ======
st.set_page_config(page_title="Home", page_icon="🏠", layout="centered")

# Title
st.title("ระเบียบวิธีแก้ตำแหน่งผิด 📝")
st.write("โปรแกรมนี้ช่วยคำนวณรากสมการด้วยวิธี **False Position Method** พร้อมแสดงผลกราฟและขั้นตอนการคำนวณ")

# โหลด Lottie JSON จาก URL
lottie_url = "https://assets10.lottiefiles.com/packages/lf20_ddca4e64.json"  # URL JSON ของ Lottie
lottie_json = load_lottieurl(lottie_url)

if lottie_json:
    st_lottie(lottie_json, height=200, key="home")

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
