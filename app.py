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

# --- কাস্টম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .school-title-bn { color: #ff3b30; font-size: 38px; font-weight: bold; line-height: 1.2; }
    .school-title-en { color: #2e7d32; font-size: 22px; font-weight: bold; }
    .footer-dark { background: #1a1a1a; color: #ccc; padding: 40px 50px; margin-top: 50px; text-align: center; }
    .comment-popup-bg { background-color: #000; padding: 20px; border-radius: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- ১. টপ সেকশন (মন্তব্য ও লগইন পপ-আপ) ---
col_t1, col_t2 = st.columns([8, 2])
with col_t2:
    c_btn, l_btn = st.columns(2)
    show_comm = c_btn.button("মন্তব্য ▼")
    show_log = l_btn.button("লগ ইন ▼")

# মন্তব্য পপ-আপ বক্স (ক্লিক করলে ওপেন হবে)
if show_comm:
    with st.expander("💬 আপনার মন্তব্য লিখুন", expanded=True):
        st.markdown('<div class="comment-popup-bg">', unsafe_allow_html=True)
        name = st.text_input("নাম :")
        c_col1, c_col2 = st.columns(2)
        email = c_col1.text_input("ইমেইল :")
        phone = c_col2.text_input("ফোন :")
        msg = st.text_area("মন্তব্য :")
        if st.button("পাঠান"):
            st.success("ধন্যবাদ! আপনার মন্তব্যটি আমাদের কাছে পৌঁছেছে।")
        st.markdown('</div>', unsafe_allow_html=True)

# লগইন পপ-আপ বক্স (ক্লিক করলে ওপেন হবে)
if show_log:
    with st.expander("🔐 অ্যাডমিন লগইন", expanded=True):
        u_name = st.text_input("ব্যবহারকারী নাম:")
        u_pass = st.text_input("গোপন নং:", type="password")
        if st.button("লগইন করুন"):
            if u_name == "admin" and u_pass == "12345":
                st.success("লগইন সফল!")
            else:
                st.error("ভুল ইউজারনেম বা পাসওয়ার্ড!")

# --- ২. মেইন হেডার (লোগো ও নাম) ---
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
        st.write("সানরাইজ কিন্ডারগার্টেনে আপনার শিশুকে উন্নত ও আধুনিক শিক্ষায় শিক্ষিত করে তুলতে আমরা প্রতিশ্রুতিবদ্ধ।")
    
    with col_side:
        st.markdown("#### নোটিশ বোর্ড")
        st.info("📌 ২০২৬ শিক্ষাবর্ষের ভর্তি কার্যক্রম চলছে।")
        st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", caption="প্রধান শিক্ষক", width=150)

# --- ৫. অনলাইন ভর্তি ফরম ---
with tabs[4]:
    st.markdown("### 📝 অনলাইন ভর্তি ফরম")
    with st.form("admission"):
        c1, c2 = st.columns(2)
        n_bn = c1.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
        n_en = c2.text_input("Student Name (English)")
        f_bn = c1.text_input("২। পিতার নাম (বাংলা)")
        m_bn = c2.text_input("৪। মাতার নাম (বাংলা)")
        if st.form_submit_button("আবেদন জমা দিন"):
            st.success("আবেদন সফল হয়েছে!")

# --- ৬. ফুটার ---
st.markdown("""
    <div class="footer-dark">
        <p>© ২০২৬ সানরাইজ কিন্ডারগার্টেন | হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ।</p>
    </div>
    """, unsafe_allow_html=True)
