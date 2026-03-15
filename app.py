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

# --- সেশন স্টেট ও টগল হ্যান্ডলিং ---
if 'show_comment' not in st.session_state: st.session_state.show_comment = False
if 'show_login' not in st.session_state: st.session_state.show_login = False
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

def toggle_comment():
    st.session_state.show_comment = not st.session_state.show_comment
    st.session_state.show_login = False

def toggle_login():
    if st.session_state.logged_in: # লগইন থাকলে বাটন ক্লিক করলে লগআউট হবে
        st.session_state.logged_in = False
        st.rerun()
    else:
        st.session_state.show_login = not st.session_state.show_login
        st.session_state.show_comment = False

# --- কাস্টম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .slide-down-container { background-color: #000; padding: 25px 50px; color: white; border-bottom: 4px solid #ff3b30; }
    .school-title-bn { color: #ff3b30; font-size: 35px; font-weight: bold; }
    .school-title-en { color: #2e7d32; font-size: 20px; font-weight: bold; }
    .footer { background: #111; color: #888; padding: 20px; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- ১. টপ বাটন বার ---
col_empty, col_btns = st.columns([8, 2])
with col_btns:
    c1, c2 = st.columns(2)
    c1.button("মন্তব্য ▼", on_click=toggle_comment)
    login_label = "লগ আউট" if st.session_state.logged_in else "লগ ইন ▼"
    c2.button(login_label, on_click=toggle_login)

# --- ২. স্লাইড ডাউন সেকশন (ভিডিও অনুযায়ী) ---

# মন্তব্য সেকশন
if st.session_state.show_comment:
    with st.container():
        st.markdown('<div class="slide-down-container">', unsafe_allow_html=True)
        st.write("### 💬 আপনার মন্তব্য দিন")
        st.text_input("নাম :")
        st.text_area("আপনার মতামত :")
        st.button("পাঠান", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

# লগইন সেকশন
if st.session_state.show_login and not st.session_state.logged_in:
    with st.container():
        st.markdown('<div class="slide-down-container">', unsafe_allow_html=True)
        st.write("### 🔐 অ্যাডমিন লগইন")
        l_user = st.text_input("ব্যবহারকারী নাম :")
        l_pass = st.text_input("গোপন নং :", type="password")
        if st.button("প্রবেশ করুন"):
            if l_user == "admin" and l_pass == "12345":
                st.session_state.logged_in = True
                st.session_state.show_login = False
                st.rerun()
            else:
                st.error("ভুল তথ্য!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- ৩. হেডার (লোগো ও নাম) ---
header_l, header_r = st.columns([1, 5])
with header_l:
    st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg", width=110)
with header_r:
    st.markdown("""
        <div style='margin-left: -40px;'>
            <div class="school-title-bn">সানরাইজ কিন্ডারগার্টেন</div>
            <div class="school-title-en">SUN RISE KINDER GARTEN</div>
        </div>
        """, unsafe_allow_html=True)

# --- ৪. মেনু নেভিগেশন (লগইন থাকলে বাড়তি ট্যাব আসবে) ---
menu_items = ["হোম পেজ", "অনলাইন ভর্তি", "রেজাল্ট অনুসন্ধান"]
if st.session_state.logged_in:
    menu_items.append("📊 তথ্য আপডেট/ম্যানেজ")

tabs = st.tabs(menu_items)

# --- ৫. অ্যাডমিন ম্যানেজমেন্ট ট্যাব (তথ্য আপডেট করার জন্য) ---
if st.session_state.logged_in:
    with tabs[-1]:
        st.header("🛠 ওয়েবসাইট ম্যানেজমেন্ট প্যানেল")
        
        manage_option = st.selectbox("কি আপডেট করতে চান?", ["নোটিশ বোর্ড", "ভর্তি আবেদন তালিকা", "শিক্ষক তালিকা"])
        
        if manage_option == "নোটিশ বোর্ড":
            new_notice = st.text_area("নতুন নোটিশ লিখুন:")
            if st.button("নোটিশ আপডেট করুন"):
                st.success("নোটিশ সফলভাবে আপডেট হয়েছে!")
        
        elif manage_option == "ভর্তি আবেদন তালিকা":
            # এখানে csv থেকে ডাটা লোড হবে
            df_students = load_data("students.csv", ["ID", "Name", "Class", "Phone"])
            st.dataframe(df_students, use_container_width=True)
            if st.button("তালিকা ডাউনলোড (Excel)"):
                st.info("ডাউনলোড শুরু হচ্ছে...")

# --- ৬. হোম পেজ ---
with tabs[0]:
    col_main, col_side = st.columns([2.5, 1])
    with col_main:
        st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", use_container_width=True)
        st.markdown("### স্বাগতম!")
        st.write("সানরাইজ কিন্ডারগার্টেনে আধুনিক প্রযুক্তির মাধ্যমে পাঠদান নিশ্চিত করা হয়।")
    
    with col_side:
        st.markdown('<div style="background:#76ba1b; color:white; padding:10px;">📢 নোটিশ বোর্ড</div>', unsafe_allow_html=True)
        st.info("📌 ২০২৬ শিক্ষাবর্ষের ভর্তি চলছে।")
        st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", width=150)

# --- ৭. ফুটার ---
st.markdown('<div class="footer">© ২০২৬ সানরাইজ কিন্ডারগার্টেন | হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ।</div>', unsafe_allow_html=True)
