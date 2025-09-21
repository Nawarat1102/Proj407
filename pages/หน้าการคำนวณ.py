import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ฟังก์ชันที่ต้องการแก้ราก
def f(x):
    return np.exp(x) - 3*x

# ฟังก์ชัน False Position แบบทำตาราง
def false_position_table(A, B, N):
    fA = f(A)
    fB = f(B)

    rows = []
    for i in range(1, N+1):
        C = A - (B - A) * fA / (fB - fA)
        fC = f(C)

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
st.title("🔢 False Position Method (Regula Falsi)")

A = st.number_input("ค่าเริ่มต้น A:", value=0.0)
B = st.number_input("ค่าเริ่มต้น B:", value=1.0)
N = st.number_input("จำนวน Iterations (N):", value=10, step=1)

if st.button("คำนวณ"):
    try:
        # สร้างตาราง Iteration
        df = false_position_table(A, B, N)
        st.subheader("📊 ตารางผลการคำนวณ")
        st.dataframe(df, use_container_width=True)

        # วาดกราฟ f(x)
        xs = np.linspace(min(A, B) - 1, max(A, B) + 1, 400)
        ys = f(xs)

        fig, ax = plt.subplots()
        ax.axhline(0, color="black", linewidth=1)
        ax.plot(xs, ys, label="f(x)")
        ax.plot(df["C"], df["f(C)"], "ro--", label="Approximation (C)")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend()
        st.subheader("📈 กราฟฟังก์ชันและจุดประมาณราก")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
