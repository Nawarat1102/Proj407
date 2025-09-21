import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# False Position Method
# -------------------------------
def false_position(func, A, B, N):
    fA = func(A)
    fB = func(B)

    rows = []
    for i in range(1, N+1):
        # สูตร Regula Falsi
        C = A - (B - A) * fA / (fB - fA)
        fC = func(C)

        rows.append([i, A, B, C, fC])

        if fC < 0:
            A, fA = C, fC
        elif fC > 0:
            B, fB = C, fC
        else:
            break

    return pd.DataFrame(rows, columns=["i", "A", "B", "C", "f(C)"])

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("📐 วิธีแก้ตำแหน่งผิด (False Position Method)")

# รับอินพุตจากผู้ใช้
func_str = st.text_input("ใส่สมการ f(x):", "np.exp(x) - 3*x")
A = st.number_input("ค่าเริ่มต้น A:", value=0.6)
B = st.number_input("ค่าเริ่มต้น B:", value=0.65)
N = st.number_input("จำนวน Iterations:", value=5, step=1)

if st.button("คำนวณ"):
    try:
        # สร้างฟังก์ชันจากสมการที่ผู้ใช้กรอก
        func = lambda x: eval(func_str, {"x": x, "np": np})

        # คำนวณตาราง
        df = false_position(func, A, B, N)
        st.subheader("📊 ตารางการคำนวณ")
        st.dataframe(df, use_container_width=True)

        # วาดกราฟ f(x)
        xs = np.linspace(min(A, B) - 0.5, max(A, B) + 0.5, 400)
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
