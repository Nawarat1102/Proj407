import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

def false_position(f, a, b, tol=0.001):
    steps = []
    while True:
        fa, fb = f(a), f(b)
        c = a - (b - a) * fa / (fb - fa)
        fc = f(c)

        steps.append((a, b, c, fa, fb, fc))

        if abs(fc) < tol:
            break

        if fa * fc < 0:
            b = c
        else:
            a = c
    return c, steps

import streamlit as st


st.title("False Position Method (Regula Falsi)")

# ข้อความอธิบายในกรอบ
st.markdown(
    """
    <div style="border:2px solid #4CAF50; padding:12px; border-radius:8px; background-color:#f9f9f9">
        <b>⚠ คำอธิบายการกรอกสมการ ⚠</b><br><br>
        - e ยกกำลัง x → <code>exp(x)</code><br>
        - ยกกำลังทั่วไป → <code>x**2</code> (เช่น x²), <code>x**3</code> (เช่น x³)<br>
        - รากที่สอง (√x) → <code>sqrt(x)</code><br>
        - รากที่สาม → <code>x**(1/3)</code><br>
        - ลอการิทึมธรรมชาติ (ln) → <code>log(x)</code><br>
        - ลอการิทึมฐาน 10 → <code>log(x, 10)</code><br>
        - ฟังก์ชันตรีโกณ → <code>sin(x)</code>, <code>cos(x)</code>, <code>tan(x)</code><br>
        - ฟังก์ชันตรีโกณผกผัน → <code>asin(x)</code>, <code>acos(x)</code>, <code>atan(x)</code><br>
        - ค่าคงที่ → π = <code>pi</code>, e = <code>E</code><br>
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
    expr = sp.sympify(user_equation)  # แปลงข้อความเป็นสมการ Sympy
    f = sp.lambdify(x, expr, "numpy") # แปลงเป็นฟังก์ชัน Python
except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการอ่านสมการ: {e}")
    st.info(
        """
        🔎 เคล็ดลับการกรอกสมการ:
        - อย่าลืมใส่ * เช่น `3*x` ไม่ใช่ `3x`  
        - ยกกำลังใช้ `**` เช่น `x**2`  
        - รากที่สองใช้ `sqrt(x)`  
        - ลอการิทึมธรรมชาติใช้ `log(x)`  
        - ฟังก์ชันตรีโกณ: `sin(x)`, `cos(x)`  
        """
    )
    st.stop()


# กรอกค่า A และ B
a = st.number_input("ค่า A (จุดเริ่มต้นซ้าย)", value=0.00)
b = st.number_input("ค่า B (จุดเริ่มต้นขวา)", value=0.00)

if st.button("คำนวณ"):
    root, steps = false_position(f, a, b, tol=0.001)

    st.success(f"คำตอบประมาณ = {root:.4f}")

    # ตารางผลลัพธ์
    st.write("### ตารางผลการคำนวณ")
    st.table(
        {
            "A": [f"{s[0]:.6f}" for s in steps],
            "B": [f"{s[1]:.6f}" for s in steps],
            "C": [f"{s[2]:.6f}" for s in steps],
            "f(A)": [f"{s[3]:.6f}" for s in steps],
            "f(B)": [f"{s[4]:.6f}" for s in steps],
            "f(C)": [f"{s[5]:.6f}" for s in steps],
        }
    )

    # วาดกราฟ
    st.write("### กราฟฟังก์ชันและจุด C")
    x_vals = np.linspace(a-1, b+1, 400)
    y_vals = f(x_vals)

    fig, ax = plt.subplots()
    ax.axhline(0, color="black", linewidth=1)
    ax.plot(x_vals, y_vals, label="f(x)")
    ax.plot([s[2] for s in steps], [s[5] for s in steps], "ro-", label="C (ค่าประมาณราก)")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    st.pyplot(fig)
