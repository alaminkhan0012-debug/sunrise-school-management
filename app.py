import streamlit as st
import pandas as pd
import os
from datetime import date

# ডাটাবেস ফাংশন
def load_data(file_name, columns):
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        for col in columns:
            if col not in df.columns: df[col] = ""
        return df
    return pd.DataFrame(columns=columns)

# পেজ সেটআপ
st.set_page_config(page_title="Sun Rise Kinder Garten", layout="wide")

# --- টগল স্টেট হ্যান্ডলিং ---
if 'show_comment' not in st.session_state:
    st.session_state.show_comment = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

def toggle_comment():
    st.session_state.show_comment = not st.session_state.show_comment
    st.session_state.show_login = False # একটি খুললে অন্যটি বন্ধ হবে

def toggle_login():
    st.session_state.show_login = not st.session_state.show_login
    st.session_state.show_comment = False # একটি খুললে অন্যটি বন্ধ হবে

# --- কাস্টম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .school-title-bn { color: #ff3b30; font-size: 38px; font-weight: bold; line-height: 1.2; }
    .school-title-en { color: #2e7d32; font-size: 22px; font-weight: bold; }
    .footer-dark { background: #1a1a1a; color: #ccc; padding: 40px 50px; margin-top: 50px; text-align: center; }
    .popup-box { background-color: #000; padding: 25px; border-radius: 10px; color: white; border: 2px solid #ff3b30; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ১. টপ সেকশন (বাটন এবং টগল পপ-আপ) ---
col_t1, col_t2 = st.columns([8, 2])
with col_t2:
    c_btn, l_btn = st.columns(2)
    c_btn.button("মন্তব্য ▼", on_click=toggle_comment)
    l_btn.button("লগ ইন ▼", on_click=toggle_login)

# মন্তব্য পপ-আপ (Toggle)
if st.session_state.show_comment:
    with st.container():
        st.markdown('<div class="popup-box">', unsafe_allow_html=True)
        st.subheader("💬 আপনার মন্তব্য")
        name = st.text_input("নাম :", key="c_name")
        c1, c2 = st.columns(2)
        email = c1.text_input("ইমেইল :", key="c_email")
        phone = c2.text_input("ফোন :", key="c_phone")
        msg = st.text_area("মন্তব্য :", key="c_msg")
        if st.button("পাঠান"):
            st.success("ধন্যবাদ! মন্তব্য জমা হয়েছে।")
        st.markdown('</div>', unsafe_allow_html=True)

# লগইন পপ-আপ (Toggle)
if st.session_state.show_login:
    with st.container():
        st.markdown('<div class="popup-box">', unsafe_allow_html=True)
        st.subheader("🔐 অ্যাডমিন লগইন")
        u_name = st.text_input("ব্যবহারকারী নাম:", key="l_user")
        u_pass = st.text_input("গোপন নং:", type="password", key="l_pass")
        if st.button("লগইন"):
            if u_name == "admin" and u_pass == "12345":
                st.success("সফলভাবে লগইন হয়েছে!")
            else:
                st.error("ভুল ইউজার বা পাসওয়ার্ড!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- ২. মেইন হেডার (লোগো ও নাম ঠিক রাখা হয়েছে) ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg", width=120)
with col_text:
    st.markdown("""
        <div style='margin-left: -50px;'>
            <div class="school-title-bn">সানরাইজ কিন্ডারগার্টেন</div>
            <div class="school-title-en">SUN RISE KINDER GARTEN</div>
        </div>
        """, unsafe_allow_html=True)

# --- ৩. নেভিগেশন মেনু (বাকি সব আগের মতো) ---
menu = ["হোম পেজ", "স্কুল প্রশাসন ▼", "প্রাতিষ্ঠানিক কার্যক্রম ▼", "গ্যালারি", "অনলাইন ভর্তি ফরম", "রেজাল্ট অনুসন্ধান"]
tabs = st.tabs(menu)

# --- ৪. হোম পেজ ---
with tabs[0]:
    col_main, col_side = st.columns([2.5, 1])
    with col_main:
        st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", use_container_width=True)
        st.markdown("### স্বাগতম!")
        st.write("আমাদের লক্ষ্য মানসম্মত শিক্ষা এবং নৈতিক চরিত্র গঠন।")
    
    with col_side:
        st.markdown("#### নোটিশ বোর্ড")
        st.info("📌 ২০২৬ শিক্ষাবর্ষের ভর্তি চলছে।")
        st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", caption="প্রধান শিক্ষক", width=150)

# --- ৫. অনলাইন ভর্তি ফরম ---
with tabs[4]:
    st.markdown("### 📝 ভর্তি ফরম")
    with st.form("admission"):
        c1, c2 = st.columns(2)
        n_bn = c1.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
        f_bn = c2.text_input("২। পিতার নাম (বাংলা)")
        if st.form_submit_button("জমা দিন"):
            st.success("আবেদন জমা হয়েছে!")

# --- ৬. ফুটার ---
st.markdown("""
    <div class="footer-dark">
        <p>© ২০২৬ সানরাইজ কিন্ডারগার্টেন | হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ।</p>
    </div>
    """, unsafe_allow_html=True)
