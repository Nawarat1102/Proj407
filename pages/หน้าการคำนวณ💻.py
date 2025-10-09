import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

def false_position(f, a, b, tol=0.001):
    steps = []
    while True:
        fa, fb = f(a), f(b)
        
        # ป้องกันการหารด้วยศูนย์ หาก f(a) และ f(b) ใกล้กันมาก
        if np.isclose(fb, fa):
            st.warning("f(a) และ f(b) มีค่าใกล้กันมาก อาจทำให้การคำนวณคลาดเคลื่อน")
            break
            
        c = a - (b - a) * fa / (fb - fa)
        fc = f(c)

        steps.append((a, b, c, fa, fb, fc))

        if abs(fc) < tol:
            break

        if fa * fc < 0:
            b = c
        else:
            a = c
            
        # ป้องกันการวนลูปนานเกินไป
        if len(steps) > 100:
            st.warning("คำนวณเกิน 100 รอบ แต่ยังไม่ลู่เข้าสู่คำตอบ")
            break
            
    return c, steps

st.title("False Position Method (Regula Falsi)")

# ข้อความอธิบายในกรอบ
st.markdown(
    """
    <div style="border:2px solid #4CAF50; padding:12px; border-radius:8px; background-color:#f9f9f9">
        <b>⚠ คำอธิบายการกรอกสมการ ⚠</b><br><br>
        - e ยกกำลัง x → <code>exp(x)</code><br>
        - ยกกำลังทั่วไป → <code>x**2</code> (เช่น x²), <code>x**3</code> (เช่น x³)<br>
        - รากที่สอง (√x) → <code>sqrt(x)</code><br>
        - ลอการิทึมธรรมชาติ (ln) → <code>log(x)</code><br>
        - การคูณต้องใส่ <code>*</code> เช่น 3x → <code>3*x</code><br>
        <br>
        ✅ ตัวอย่าง: <code>(x**3) - (x**2) - 0.1</code>, <code>exp(x) - 3*x</code>, <code>sin(x) - x/2</code>
    </div>
    """,
    unsafe_allow_html=True
)

# ช่องกรอกสมการ
user_equation = st.text_input("กรอกฟังก์ชัน f(x):", value="exp(x) - 3*x")

# สร้างฟังก์ชันจากสมการที่กรอก
x = sp.symbols("x")
try:
    expr = sp.sympify(user_equation)
    f = sp.lambdify(x, expr, "numpy")
except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการอ่านสมการ: {e}")
    st.stop()


# กรอกค่า A และ B (เปลี่ยนค่าเริ่มต้น b เพื่อให้ตัวอย่างทำงานได้)
a = st.number_input("ค่า A (จุดเริ่มต้นซ้าย)", value=0.0)
b = st.number_input("ค่า B (จุดเริ่มต้นขวา)", value=1.0)

if st.button("คำนวณ"):
    
    # ---------------------------------------------------------------
    # ▼▼▼ ส่วนที่เพิ่มเข้ามาเพื่อตรวจสอบค่า a และ b ก่อนคำนวณ ▼▼▼
    # ---------------------------------------------------------------

    # 1. ตรวจสอบว่า a น้อยกว่า b หรือไม่
    if a >= b:
        st.error("❌ **เงื่อนไขไม่ถูกต้อง:** ค่า A (ขอบเขตซ้าย) ต้องน้อยกว่าค่า B (ขอบเขตขวา)")
    else:
        # 2. ถ้า a < b จริง ให้คำนวณ f(a) และ f(b) เพื่อตรวจสอบเครื่องหมาย
        fa_val = f(a)
        fb_val = f(b)

        if fa_val * fb_val >= 0:
            # ถ้าเครื่องหมายเหมือนกัน ให้แสดงข้อผิดพลาด
            st.error(f"❌ **เงื่อนไขไม่ถูกต้อง:** f(a) และ f(b) ต้องมีเครื่องหมายต่างกัน")
            st.info(f"ตอนนี้ค่าที่ได้คือ: f({a}) = {fa_val:.4f} และ f({b}) = {fb_val:.4f}")
        else:
            # ✅ ถ้าทุกเงื่อนไขถูกต้อง จึงจะเริ่มกระบวนการคำนวณและแสดงผล
            
            st.write("---") # เพิ่มเส้นคั่นเพื่อความสวยงาม
            
            # เรียกใช้ฟังก์ชันคำนวณ (โค้ดส่วนนี้คือโค้ดเดิมของคุณ)
            root, steps = false_position(f, a, b, tol=0.001)

            st.success(f"**คำตอบประมาณ = {root:.6f}**")

            # ตารางผลลัพธ์
            st.write("### 📝 ตารางผลการคำนวณ")
            st.table(
                {
                    "a": [f"{s[0]:.6f}" for s in steps],
                    "b": [f"{s[1]:.6f}" for s in steps],
                    "c": [f"{s[2]:.6f}" for s in steps],
                    "f(a)": [f"{s[3]:.6f}" for s in steps],
                    "f(b)": [f"{s[4]:.6f}" for s in steps],
                    "f(c)": [f"{s[5]:.6f}" for s in steps],
                }
            )

            # วาดกราฟ
            st.write("### 📈 กราฟฟังก์ชันและจุด C")
            x_vals = np.linspace(a - 1, b + 1, 400)
            y_vals = f(x_vals)

            fig, ax = plt.subplots()
            ax.axhline(0, color="gray", linestyle='--', linewidth=0.8)
            ax.plot(x_vals, y_vals, label="f(x)")
            ax.plot([s[2] for s in steps], [s[5] for s in steps], "ro", label="ค่าประมาณราก (c) ในแต่ละรอบ")
            ax.grid(True, linestyle=':', linewidth=0.5)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.legend()
            st.pyplot(fig)
            
    # -----------------------------------------------------------
    # ▲▲▲ สิ้นสุดส่วนที่เพิ่มเข้ามา ▲▲▲
    # -----------------------------------------------------------