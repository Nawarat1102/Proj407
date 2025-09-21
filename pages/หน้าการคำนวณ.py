import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# -------------------------------
# ฟังก์ชันคำนวณ False Position
# -------------------------------
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

# -------------------------------
# ส่วนของ Streamlit
# -------------------------------
st.title("False Position Method (Regula Falsi)")

# ช่องกรอกสมการ
user_equation = st.text_input("กรอกสมการ f(x):", value="exp(x) - 3*x")

# สร้างฟังก์ชันจากสมการที่กรอก
x = sp.symbols("x")
try:
    expr = sp.sympify(user_equation)  # แปลงข้อความเป็นสมการ Sympy
    f = sp.lambdify(x, expr, "numpy") # แปลงเป็นฟังก์ชัน Python
except Exception as e:
    st.error(f"Error in equation: {e}")
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
