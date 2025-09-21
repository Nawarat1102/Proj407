import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# False Position Method function
# -------------------------------
def false_position(func, x0, x1, tol=1e-6, max_iter=100):
    if func(x0) * func(x1) >= 0:
        raise ValueError("f(x0) และ f(x1) ต้องมีเครื่องหมายต่างกัน")

    for i in range(max_iter):
        # สูตร Regula Falsi
        x2 = (x0 * func(x1) - x1 * func(x0)) / (func(x1) - func(x0))
        f2 = func(x2)

        if abs(f2) < tol:
            return x2, i+1
        elif func(x0) * f2 < 0:
            x1 = x2
        else:
            x0 = x2

    return x2, max_iter

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🧮 False Position Method (Regula Falsi)")

# Input สมการและค่าเริ่มต้น
func_str = st.text_input("ใส่สมการ f(x):", "x**3 - x - 2")
x0 = st.number_input("ค่า x0:", value=1.0)
x1 = st.number_input("ค่า x1:", value=2.0)
tol = st.number_input("Tolerance:", value=1e-6, format="%.1e")
max_iter = st.number_input("Max Iterations:", value=50, step=1)

# เมื่อกดปุ่ม
if st.button("คำนวณ"):
    try:
        func = lambda x: eval(func_str, {"x": x, "np": np})
        root, iters = false_position(func, x0, x1, tol, max_iter)

        st.success(f"✅ รากประมาณ = {root:.6f} ใน {iters} iterations")

        # วาดกราฟ
        xs = np.linspace(min(x0, x1) - 2, max(x0, x1) + 2, 400)
        ys = [func(x) for x in xs]

        fig, ax = plt.subplots()
        ax.axhline(0, color="black", linewidth=1)
        ax.plot(xs, ys, label="f(x)")
        ax.plot(root, func(root), "ro", label="Root")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
