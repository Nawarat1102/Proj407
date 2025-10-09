import streamlit as st

# ====== หน้า Home ======
st.set_page_config(page_title="Home", page_icon="🏠", layout="centered")

st.title("ระเบียบวิธีแก้ตำแหน่งผิด 📝")
st.write(
    """
    โปรแกรมนี้ช่วยคำนวณรากของสมการ f(x) = 0 ด้วยวิธี False Position Method 
    พร้อมแสดงผลกราฟและขั้นตอนการคำนวณอย่างละเอียด
    """
)
st.write("---") # เพิ่มเส้นคั่นเพื่อความสวยงาม

# ปุ่มลิงก์ไปยังหน้าต่างๆ
st.subheader("เมนูหลัก")
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/หน้าการคำนวณ💻.py", label="**เริ่มคำนวณ**", icon="💻")

with col2:
    st.page_link("pages/คู่มือ🔍.py", label="**คู่มือใช้งาน**", icon="🔍")

with col3:
    # ใช้ st.link_button เพื่อความสวยงามและสอดคล้อง
    st.link_button(
        "**Wiki: เรียนรู้เพิ่ม**", 
        url="https://th.wikipedia.org/wiki/ระเบียบวิธีแก้ตำแหน่งผิด", 
        icon="📚"
    )

st.write("---")

# คำแนะนำเบื้องต้น
st.info(
    "📌 **เริ่มต้นใช้งาน:** กดปุ่ม **'เริ่มคำนวณ'** เพื่อหาค่ารากของสมการที่คุณต้องการ"
)

# จัดวางรูปภาพให้อยู่ตรงกลาง
col_left, col_center, col_right = st.columns([1, 3, 1])
with col_center:
    # แนะนำให้สร้างโฟลเดอร์ assets เพื่อเก็บรูปภาพ
    st.image("assets/MAT.jpg", caption="False Position Method Visualization", use_container_width=True)