import streamlit as st
import pandas as pd
import os
from datetime import date

# ডাটাবেস হ্যান্ডলিং
def load_data(file_name, columns):
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        for col in columns:
            if col not in df.columns: df[col] = ""
        return df
    return pd.DataFrame(columns=columns)

# পেজ সেটআপ
st.set_page_config(page_title="Sun Rise Kinder Garten", layout="wide", page_icon="🏫")

# --- ক্রিসেন্ট হাই স্কুল স্টাইল ডিজাইন (CSS) ---
st.markdown("""
    <style>
    /* কালো টপ বার (লগইন সেকশন) */
    .top-login-bar { background-color: #000; padding: 15px; display: flex; justify-content: flex-end; gap: 10px; border-bottom: 3px solid red; }
    .top-login-bar input { padding: 5px; border-radius: 3px; border: none; }
    
    /* হেডার সেকশন */
    .header-main { background: white; padding: 20px; display: flex; align-items: center; border-bottom: 1px solid #ddd; }
    .school-title { color: #d32f2f; font-size: 35px; font-weight: bold; margin-left: 20px; font-family: 'SolaimanLipi', sans-serif; }
    
    /* মেনু বার */
    .nav-bar { background: #f8f9fa; border-bottom: 2px solid #ddd; padding: 5px 0; }
    
    /* নোটিশ বোর্ড */
    .notice-box { background: #76ba1b; color: white; padding: 10px; font-weight: bold; border-radius: 5px 5px 0 0; }
    .notice-item { border-bottom: 1px solid #eee; padding: 10px; background: white; }
    .date-tag { background: #008eb0; color: white; padding: 2px 5px; border-radius: 3px; font-size: 12px; }
    
    /* ফুটার */
    .footer { background: #1a1a1a; color: white; padding: 30px; margin-top: 50px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ১. টপ লগইন বার (Screenshot_8 এর মতো) ---
st.markdown("""
    <div class="top-login-bar">
        <input type="text" placeholder="ব্যবহারকারী:">
        <input type="password" placeholder="গোপন নং:">
        <button style="background: #a1887f; color: white; border: none; padding: 5px 15px; cursor: pointer;">পাঠান</button>
    </div>
    """, unsafe_allow_html=True)

# --- ২. মেইন হেডার ---
st.markdown(f"""
    <div class="header-main">
        <img src="https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg" width="100">
        <div class="school-title">সানরাইজ কিন্ডারগার্টেন <br> <span style="font-size: 20px; color: #2e7d32;">SUN RISE KINDER GARTEN</span></div>
    </div>
    """, unsafe_allow_html=True)

# --- ৩. মেনু নেভিগেশন ---
menu = ["হোম পেজ", "স্কুল প্রশাসন", "প্রাতিষ্ঠানিক কার্যক্রম", "গ্যালারি", "অনলাইন ভর্তি", "রেজাল্ট অনুসন্ধান"]
choice = st.tabs(menu)

STD_COLS = ["ID", "Name_BN", "Name_EN", "Father_BN", "Mother_BN", "F_Job", "Class", "Phone", "Address", "Date"]

# --- ৪. হোম পেজ লেআউট ---
with choice[0]:
    col_l, col_r = st.columns([2.5, 1])
    
    with col_l:
        # স্লাইডার ইমেজ (আপনার বিল্ডিংয়ের ছবির মতো)
        st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", caption="আমাদের মনোরম ক্যাম্পাস", use_container_width=True)
        
        st.markdown("### প্রধান শিক্ষকের বাণী")
        c1, c2 = st.columns([1, 3])
        c1.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", width=150)
        c2.write("সানরাইজ কিন্ডারগার্টেন হূমাইপুর অঞ্চলের একটি আদর্শ বিদ্যাপীঠ। আমরা ডিজিটাল বাংলাদেশ গড়ার লক্ষ্যে শিশুদের আধুনিক শিক্ষায় শিক্ষিত করছি।")

    with col_r:
        st.markdown('<div class="notice-box">📢 নোটিশ বোর্ড</div>', unsafe_allow_html=True)
        notices = [
            ("12 March 2026", "২০২৬ শিক্ষাবর্ষের ভর্তি তথ্য।"),
            ("10 March 2026", "নতুন ক্লাসের সময়সূচী।"),
            ("05 March 2026", "বার্ষিক ক্রীড়া প্রতিযোগিতার নোটিশ।")
        ]
        for dt, txt in notices:
            st.markdown(f"""
            <div class="notice-item">
                <span class="date-tag">{dt}</span><br>
                <small>{txt}</small>
            </div>
            """, unsafe_allow_html=True)

# --- ৫. অনলাইন ভর্তি (আপনার ফরম অনুযায়ী) ---
with choice[4]:
    st.markdown("### 📝 ভর্তি আবেদন ফরম (২০২৬)")
    with st.form("admission_form", clear_on_submit=True):
        st.info("আপনার ভর্তি ফরমের আলোকে তথ্যগুলো পূরণ করুন।")
        c1, c2 = st.columns(2)
        n_bn = c1.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
        n_en = c2.text_input("Student Name (English Block)")
        f_bn = c1.text_input("২। পিতার নাম (বাংলা)")
        m_bn = c2.text_input("৪। মাতার নাম (বাংলা)")
        f_job = c1.text_input("৬। পিতার পেশা")
        s_class = c2.selectbox("ভর্তির শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        phone = c1.text_input("মোবাইল নম্বর")
        addr = st.text_area("৫। ঠিকানা")
        
        if st.form_submit_button("আবেদন জমা দিন"):
            df = load_data("students.csv", STD_COLS)
            new_id = 202600 + len(df) + 1
            new_row = pd.DataFrame([[new_id, n_bn, n_en, f_bn, m_bn, f_job, s_class, phone, addr, str(date.today())]], columns=STD_COLS)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.success(f"আবেদন জমা হয়েছে! আপনার আইডি: {new_id}")
            st.balloons()

# --- ৬. ফুটার (Screenshot_11 এর মতো) ---
st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-around; text-align: left;">
            <div>
                <h4>আমাদের ঠিকানা</h4>
                <p>সানরাইজ কিন্ডারগার্টেন<br>হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ।<br>মোবাইল: ০১৭২৭-৪১৪১৩৪</p>
            </div>
            <div>
                <h4>প্রয়োজনীয় লিংক</h4>
                <p>দিনাজপুর শিক্ষা বোর্ড<br>মাধ্যমিক ও উচ্চশিক্ষা অধিদপ্তর<br>শিক্ষক বাতায়ন</p>
            </div>
        </div>
        <hr style='border-color: #444;'>
        <p>© ২০২৬ সর্বস্বত্ব সংরক্ষিত | ডিজাইন ও ডেভেলপমেন্ট: আলামিন খান</p>
    </div>
    """, unsafe_allow_html=True)
