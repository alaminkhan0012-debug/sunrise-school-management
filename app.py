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

# --- সেশন স্টেট (লগইন কন্ট্রোল) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- কাস্টম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .top-bar-container { display: flex; justify-content: flex-end; gap: 10px; padding: 10px 50px; background-color: #f8f9fa; }
    .school-title-bn { color: #ff3b30; font-size: 38px; font-weight: bold; line-height: 1.2; }
    .school-title-en { color: #2e7d32; font-size: 22px; font-weight: bold; }
    .footer-dark { background: #1a1a1a; color: #ccc; padding: 40px 50px; margin-top: 50px; }
    /* কমেন্ট বক্সের কালো ব্যাকগ্রাউন্ড স্টাইল (ছবির মতো) */
    .comment-box-bg { background-color: #000; padding: 30px; border-radius: 5px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- ১. টপ বার: মন্তব্য ও লগইন অপশন (বাকি সব ঠিক রেখে) ---
col_t1, col_t2 = st.columns([8, 2])
with col_t2:
    c_btn, l_btn = st.columns(2)
    show_comm = c_btn.button("মন্তব্য ▼")
    show_log = l_btn.button("লগ ইন ▼")

# লগইন অপশন (ক্লিক করলে আসবে)
if show_log:
    with st.expander("🔐 লগইন করুন", expanded=True):
        u_name = st.text_input("ব্যবহারকারী নাম:")
        u_pass = st.text_input("গোপন নং:", type="password")
        if st.button("পাঠান"):
            if u_name == "admin" and u_pass == "12345":
                st.session_state['logged_in'] = True
                st.success("লগইন সফল!")
            else:
                st.error("ভুল তথ্য!")

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

# --- ৩. নেভিগেশন মেনু (বাকি সব ঠিক আছে) ---
menu = ["হোম পেজ", "স্কুল প্রশাসন ▼", "প্রাতিষ্ঠানিক কার্যক্রম ▼", "গ্যালারি", "অনলাইন ভর্তি ফরম", "রেজাল্ট অনুসন্ধান"]
tabs = st.tabs(menu)

# --- ৪. হোম পেজ ও মন্তব্য সেকশন (ছবির মতো ডিজাইন) ---
with tabs[0]:
    col_main, col_side = st.columns([2.5, 1])
    with col_main:
        st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", use_container_width=True)
        
        # মন্তব্য সেকশন (আপনার পাঠানো ছবির হুবহু ডিজাইন)
        if show_comm:
            st.markdown("### মন্তব্য করুন")
            with st.container():
                st.markdown('<div class="comment-box-bg">', unsafe_allow_html=True)
                m_name = st.text_input("নাম :")
                m_col1, m_col2 = st.columns(2)
                m_email = m_col1.text_input("ইমেল :")
                m_phone = m_col2.text_input("ফোন :")
                m_msg = st.text_area("মন্তব্য :")
                if st.button("পাঠান", key="send_msg"):
                    st.write("ধন্যবাদ! আপনার মন্তব্য জমা হয়েছে।")
                st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown("#### নোটিশ বোর্ড")
        st.info("📌 ২০২৬ শিক্ষাবর্ষের ভর্তি চলছে।")
        st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", caption="প্রধান শিক্ষক", width=150)

# --- ৫. অনলাইন ভর্তি ফরম (আপনার অরিজিনাল ফরম ঠিক রাখা হয়েছে) ---
with tabs[4]:
    st.markdown("## 📝 অনলাইন ভর্তি আবেদন ফরম")
    with st.form("admission"):
        c1, c2 = st.columns(2)
        name_bn = c1.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
        name_en = c2.text_input("Student Name (English)")
        f_name = c1.text_input("২। পিতার নাম (বাংলা)")
        m_name = c2.text_input("৪। মাতার নাম (বাংলা)")
        s_class = c1.selectbox("ভর্তির শ্রেণী", ["Play", "Nursery", "One", "Two", "Three"])
        if st.form_submit_button("আবেদন জমা দিন"):
            st.success("সফলভাবে জমা হয়েছে!")

# --- ৬. ফুটার ---
st.markdown("""
    <div class="footer-dark">
        <p style="text-align: center;">© ২০২৬ সর্বস্বত্ব সংরক্ষিত | সানরাইজ কিন্ডারগার্টেন <br> হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ।</p>
    </div>
    """, unsafe_allow_html=True)
