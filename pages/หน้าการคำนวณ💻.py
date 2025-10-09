import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# ฟังก์ชัน false_position เหมือนเดิม
def false_position(f, a, b, tol=0.001):
    steps = []
    fa, fb = f(a), f(b)
    
    if np.isclose(fa, fb):
        st.error("f(a) และ f(b) มีค่าใกล้เคียงกันมาก อาจทำให้หารด้วยศูนย์")
        st.stop()
        
    while True:
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        steps.append((a, b, c, fa, fb, fc))

        if abs(fc) < tol:
            break

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
            
        if len(steps) > 100:
             st.warning("คำนวณเกิน 100 รอบ แต่ยังไม่ลู่เข้าสู่คำตอบ อาจเกิดจากลักษณะของกราฟ")
             break
             
    return c, steps

st.title("False Position Method (Regula Falsi)")

# ส่วนของคำอธิบายเหมือนเดิม
st.markdown(
    """
    <div style="border:2px solid #4CAF50; padding:12px; border-radius:8px; background-color:#f9f9f9">
        <b>⚠ คำอธิบายการกรอกสมการ ⚠</b><br><br>
        - e ยกกำลัง x → <code>exp(x)</code><br>
        - ยกกำลังทั่วไป → <code>x**2</code> (เช่น x²), <code>x**3</code> (เช่น x³)<br>
        - รากที่สอง (√x) → <code>sqrt(x)</code><br>
        - การคูณต้องใส่ <code>*</code> เช่น 3x → <code>3*x</code><br>
        <br>
        ✅ ตัวอย่าง: <code>x**3 - x - 2</code>, <code>exp(x) - 3*x</code>, <code>cos(x) - x</code>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 💡 จุดที่แก้ไข: เพิ่มส่วน "ข้อจำกัดของระเบียบวิธี" ---
st.info(
    """
    ### ❗ ข้อจำกัดของระเบียบวิธี (Limitations)
    1.  **ต้องหาช่วงเริ่มต้น [a, b] ที่ f(a) และ f(b) มีเครื่องหมายต่างกันให้ได้ก่อน** ซึ่งในบางครั้งอาจทำได้ยาก
    2.  **การลู่เข้าสู่คำตอบอาจช้ามาก** หากกราฟของฟังก์ชันมีความโค้งสูงใกล้ราก อาจทำให้ขอบเขตด้านใดด้านหนึ่งไม่ขยับเลย (One-sided convergence) ทำให้การคำนวณใช้เวลานาน
    3.  **ไม่เหมาะกับฟังก์ชันที่มีรากซ้ำ** (Multiple roots)
    """
)


# ช่องกรอกสมการ
user_equation = st.text_input("กรอกฟังก์ชัน f(x):", value="exp(x) - 3*x")

try:
    x = sp.symbols("x")
    expr = sp.sympify(user_equation)
    f = sp.lambdify(x, expr, "numpy")
except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาดในการอ่านสมการ: {e}")
    st.stop()

# กรอกค่า A และ B
a = st.number_input("ค่า A (ขอบเขตซ้าย)", value=0.0)
b = st.number_input("ค่า B (ขอบเขตขวา)", value=1.0) 

if st.button("คำนวณ"):
    # --- 💡 จุดที่แก้ไข: เพิ่มการตรวจสอบ a < b ก่อนเงื่อนไขอื่น ---
    # 1. ตรวจสอบว่า a น้อยกว่า b หรือไม่
    if a >= b:
        st.error("❌ **เงื่อนไขไม่ถูกต้อง:** ค่า A (ขอบเขตซ้าย) ต้องน้อยกว่าค่า B (ขอบเขตขวา)")
    else:
        # 2. ตรวจสอบเงื่อนไข f(a) * f(b) < 0
        fa_val = f(a)
        fb_val = f(b)

        if fa_val * fb_val >= 0:
            st.error(f"❌ **เงื่อนไขไม่ถูกต้อง:** f(a) และ f(b) ต้องมีเครื่องหมายต่างกัน")
            st.info(f"ตอนนี้ค่าที่ได้คือ: f({a}) = {fa_val:.4f} และ f({b}) = {fb_val:.4f} (เครื่องหมายเหมือนกัน)")
        else:
            # --- ถ้าทุกอย่างถูกต้อง ให้เริ่มคำนวณ ---
            try:
                root, steps = false_position(f, a, b, tol=0.001)

                st.success(f"🎉 คำตอบประมาณ = {root:.6f}")

                # ตารางผลลัพธ์
                st.write("### 📝 ตารางผลการคำนวณ")
                st.table(
                    {
                        "รอบที่": [i+1 for i in range(len(steps))],
                        "a": [f"{s[0]:.6f}" for s in steps],
                        "b": [f"{s[1]:.6f}" for s in steps],
                        "c (ราก)": [f"{s[2]:.6f}" for s in steps],
                        "f(c)": [f"{s[5]:.6f}" for s in steps],
                    }
                )

                # วาดกราฟ
                st.write("### 📈 กราฟฟังก์ชันและจุด C")
                x_vals = np.linspace(a - 1, b + 1, 400)
                y_vals = f(x_vals)

                fig, ax = plt.subplots()
                ax.axhline(0, color="gray", linewidth=0.8, linestyle='--')
                ax.axvline(0, color="gray", linewidth=0.8, linestyle='--')
                ax.plot(x_vals, y_vals, label=f"f(x) = {user_equation}")
                
                # --- 💡 จุดที่แก้ไข: เปลี่ยน "ro-" เป็น "ro" เพื่อไม่ให้มีเส้นเชื่อม ---
                ax.plot([s[2] for s in steps], [s[5] for s in steps], "ro", label="ค่าประมาณของราก (c) ในแต่ละรอบ")
                
                ax.plot(root, f(root), 'g*', markersize=10, label=f"คำตอบสุดท้าย ≈ {root:.4f}")
                ax.set_xlabel("x")
                ax.set_ylabel("f(x)")
                ax.grid(True, which='both', linestyle='--', linewidth=0.5)
                ax.legend()
                st.pyplot(fig)

            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดระหว่างการคำนวณ: {e}")