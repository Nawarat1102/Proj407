import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# False Position Method with tolerance
# -------------------------------
def false_position(func, A, B, tol=1e-3, max_iter=100):
    fA = func(A)
    fB = func(B)

    rows = []
    for i in range(1, max_iter+1):
        # สูตร Regula Falsi
        C = A - (B - A) * fA / (fB - fA)
        fC = func(C)

        rows.append([i, A, B, C, fC])

        # เงื่อนไขหยุดเมื่อ |f(C)| < tolerance
        if abs(fC) < tol:
            break

        if fA * fC < 0:
            B, fB = C, fC
        else:
            A, fA = C, fC

    return pd.DataFrame(rows, columns=["i", "A", "B", "C", "f(C)"])

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("📐 วิธีแก้ตำแหน่งผิด (False Position Method)")

# รับอินพุตจากผู้ใช้
func_str = st.text_input("ใส่สมการ f(x):", "np.exp(x) - 3*x")
A = st.number_input("ค่าเริ่มต้น A:", value=0.6)
B = st.number_input("ค่าเริ่มต้น B:", value=0.65)
tol = st.number_input("Tolerance (เช่น 0.001):", value=0.001, format="%.6f")

if st.button("คำนวณ"):
    try:
        # สร้างฟังก์ชันจากสมการที่ผู้ใช้กรอก
        func = lambda x: eval(func_str, {"x": x, "np": np})

        # คำนวณ
        df = false_position(func, A, B, tol)
        st.subheader("📊 ตารางการคำนวณ")
        st.dataframe(df, use_container_width=True)

        # คำตอบสุดท้าย
        last_row = df.iloc[-1]
        st.success(f"✅ ค่าประมาณราก = {last_row['C']:.6f} (f(C) = {last_row['f(C)']:.6f})")

        # วาดกราฟ
        xs = np.linspace(min(A, B) - 1, max(A, B) + 1, 400)
        ys = func(xs)

        fig, ax = plt.subplots()
        ax.axhline(0, color="black", linewidth=1)
        ax.plot(xs, ys, label="f(x)")
        ax.plot(df["C"], df["f(C)"], "ro--", label="จุด C แต่ละรอบ")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend()
        st.subheader("📈 กราฟฟังก์ชันและจุดประมาณราก")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
