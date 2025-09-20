import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ===== Input จากผู้ใช้ =====
func_str = st.text_input("ใส่สมการ f(x):", "x**3 - x - 2")
x0 = st.number_input("ค่า x0:", value=1.0)
x1 = st.number_input("ค่า x1:", value=2.0)
tol = st.number_input("Tolerance:", value=1e-6, format="%.1e")
max_iter = st.number_input("Max Iterations:", value=50, step=1)

# แปลงเป็นฟังก์ชันจริง
func = lambda x: eval(func_str, {"x": x, "np": np})

if st.button("คำนวณ"):
    try:
        root, iters = false_position(func, x0, x1, tol, max_iter)
        st.success(f"รากประมาณ = {root:.6f} ใน {iters} iterations")

        # วาดกราฟ
        xs = np.linspace(min(x0, x1) - 1, max(x0, x1) + 1, 200)
        ys = [func(x) for x in xs]

        fig, ax = plt.subplots()
        ax.axhline(0, color="black", linewidth=1)
        ax.plot(xs, ys, label="f(x)")
        ax.plot(root, func(root), "ro", label="Root")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")
