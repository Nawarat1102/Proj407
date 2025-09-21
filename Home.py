import streamlit as st
from streamlit_lottie import st_lottie
import requests

# ====== ฟังก์ชันโหลด Lottie ======
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

import json
from streamlit_lottie import st_lottie
st.page_link("pages/หน้าการคำนวณ.py", label="หน้าการคำนวณ", icon="3️⃣")
st.page_link("pages/คู่มือ.py", label="คู่มือ", icon="3️⃣")
st.page_link("http://www.google.com", label="Google", icon="🌎")