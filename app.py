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

# --- টগল স্টেট কন্ট্রোল ---
if 'show_comment' not in st.session_state:
    st.session_state.show_comment = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

def toggle_comment():
    st.session_state.show_comment = not st.session_state.show_comment
    st.session_state.show_login = False

def toggle_login():
    st.session_state.show_login = not st.session_state.show_login
    st.session_state.show_comment = False

# --- কাস্টম সিএসএস (CSS) ---
st.markdown("""
    <style>
    /* কালো স্লাইড বার স্টাইল */
    .slide-down-container {
        background-color: #000;
        padding: 20px 50px;
        color: white;
        border-bottom: 4px solid #ff3b30;
        margin-top: -10px;
    }
    .school-title-bn { color: #ff3b30; font-size: 35px; font-weight: bold; line-height: 1.1; }
    .school-title-en { color: #2e7d32; font-size: 20px; font-weight: bold; }
    .footer { background: #111; color: #888; padding: 30px; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- ১. টপ বাটন বার ---
col_empty, col_btns = st.columns([8, 2])
with col_btns:
    c1, c2 = st.columns(2)
    c1.button("মন্তব্য ▼", on_click=toggle_comment, use_container_width=True)
    c2.button("লগ ইন ▼", on_click=toggle_login, use_container_width=True)

# --- ২. স্লাইড ডাউন সেকশন (ভিডিওর ৭ সেকেন্ড পরবর্তী স্টাইল) ---

# মন্তব্য স্লাইড ডাউন
if st.session_state.show_comment:
    with st.container():
        st.markdown('<div class="slide-down-container">', unsafe_allow_html=True)
        st.write("### 💬 আপনার মতামত দিন")
        st.text_input("নাম :")
        c_mail, c_phn = st.columns(2)
        c_mail.text_input("ইমেল :")
        c_phn.text_input("ফোন :")
        st.text_area("মন্তব্য :")
        st.button("পাঠান", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

# লগইন স্লাইড ডাউন
if st.session_state.show_login:
    with st.container():
        st.markdown('<div class="slide-down-container">', unsafe_allow_html=True)
        st.write("### 🔐 অ্যাডমিন লগইন")
        l_user = st.text_input("ব্যবহারকারী নাম :")
        l_pass = st.text_input("গোপন নং :", type="password")
        st.button("প্রবেশ করুন", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

# --- ৩. হেডার (লোগো ও নাম) ---
header_l, header_r = st.columns([1, 5])
with header_l:
    st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg", width=110)
with header_r:
    st.markdown("""
        <div style='margin-left: -40px; margin-top: 10px;'>
            <div class="school-title-bn">সানরাইজ কিন্ডারগার্টেন</div>
            <div class="school-title-en">SUN RISE KINDER GARTEN</div>
        </div>
        """, unsafe_allow_html=True)

# --- ৪. মেনু নেভিগেশন ---
tabs = st.tabs(["হোম পেজ", "স্কুল প্রশাসন", "প্রাতিষ্ঠানিক কার্যক্রম", "অনলাইন ভর্তি", "রেজাল্ট"])

# --- ৫. হোম পেজ কন্টেন্ট ---
with tabs[0]:
    col_left, col_right = st.columns([2.5, 1])
    with col_left:
        st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", use_container_width=True)
        st.markdown("### প্রধান শিক্ষকের বাণী")
        st.write("শিক্ষাই জাতির মেরুদণ্ড। আমরা শিশুদের সঠিক শিক্ষায় গড়ে তুলতে কাজ করছি।")
    
    with col_right:
        st.markdown('<div style="background:#76ba1b; color:white; padding:10px; font-weight:bold;">📢 নোটিশ বোর্ড</div>', unsafe_allow_html=True)
        st.info("📌 ২০২৬ শিক্ষাবর্ষের ভর্তি ফরম বিতরণ শুরু হয়েছে।")
        st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", width=150)

# --- ৬. অনলাইন ভর্তি ---
with tabs[3]:
    st.markdown("## 📝 ভর্তি ফরম")
    with st.form("admission_form"):
        st.text_input("শিক্ষার্থীর নাম (বাংলা)")
        st.text_input("পিতার নাম (বাংলা)")
        st.selectbox("ভর্তির শ্রেণী", ["Play", "Nursery", "One", "Two", "Three"])
        st.form_submit_button("আবেদন জমা দিন")

# --- ৭. ফুটার ---
st.markdown('<div class="footer">© ২০২৬ সানরাইজ কিন্ডারগার্টেন | হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ।</div>', unsafe_allow_html=True)
