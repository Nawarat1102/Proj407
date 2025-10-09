import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# --- เพิ่มส่วนนี้เพื่อแก้ปัญหาฟอนต์ภาษาไทย (สี่เหลี่ยม) ---
plt.rcParams['font.family'] = 'Tahoma'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False # แก้ไขการแสดงผลเครื่องหมายลบ
# ----------------------------------------------------

def false_position(f, a, b, tol=0.001):
    steps = []
    while True:
        fa, fb = f(a), f(b)
        
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
            
        if len(steps) > 100:
            st.warning("คำนวณเกิน 100 รอบ แต่ยังไม่ลู่เข้าสู่คำตอบ")
            break
            
    return c, steps

st.title("False Position Method (Regula Falsi)")

st.markdown(
    """
    <div style="border:2px solid #4CAF50; padding:12px; border-radius:8px; background-color:#f9f9f9">
        <b>⚠ คำอธิบายการกรอกค่าฟังก์ชัน ⚠</b><br><br>
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

user_equation = st.text_input("กรอกฟังก์ชัน f(x):", value="exp(x) - 3*x")

x = sp.symbols("x")
try:
    expr = sp.sympify(user_equation)
    f = sp.lambdify(x, expr, "numpy")
except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการอ่านสมการ: {e}")
    st.stop()

a = st.number_input("ค่า A (จุดเริ่มต้นซ้าย)", value=0.0)
b = st.number_input("ค่า B (จุดเริ่มต้นขวา)", value=1.0)

if st.button("คำนวณ"):
    
    if a >= b:
        st.error("❌ **เงื่อนไขไม่ถูกต้อง:** ค่า A (ขอบเขตซ้าย) ต้องน้อยกว่าค่า B (ขอบเขตขวา)")
    else:
        fa_val = f(a)
        fb_val = f(b)

        if fa_val * fb_val >= 0:
            st.error(f"❌ **เงื่อนไขไม่ถูกต้อง:** f(a) และ f(b) ต้องมีเครื่องหมายต่างกัน")
            st.info(f"ตอนนี้ค่าที่ได้คือ: f({a}) = {fa_val:.4f} และ f({b}) = {fb_val:.4f}")
        else:
            st.write("---") 
            
            root, steps = false_position(f, a, b, tol=0.001)

            st.success(f"**คำตอบประมาณ = {root:.6f}**")

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

            st.write("### 📈 กราฟฟังก์ชันและจุด C")
            x_vals = np.linspace(a - 1, b + 1, 400)
            y_vals = f(x_vals)

            fig, ax = plt.subplots()
            ax.axhline(0, color="gray", linestyle='--', linewidth=0.8)
            ax.plot(x_vals, y_vals, label="f(x)")
            
            # --- แก้ไข label ของกราฟตรงนี้ ---
            # เปลี่ยน label จาก "จุด (c)" เป็นภาษาอังกฤษ
            ax.plot([s[2] for s in steps], [s[5] for s in steps], "ro", label="Point (c)") 
            # ---------------------------------
            
            ax.grid(True, linestyle=':', linewidth=0.5)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.legend()
            st.pyplot(fig)