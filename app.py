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

# পেজ কনফিগারেশন
st.set_page_config(page_title="Sun Rise Kinder Garten", layout="wide")

# --- কাস্টম সিএসএস (ডিজাইন সুন্দর করার জন্য) ---
st.markdown("""
    <style>
    /* টপ বার ডিজাইন (মন্তব্য ও লগইন) */
    .top-header { background-color: #d32f2f; padding: 5px 20px; display: flex; justify-content: flex-end; align-items: center; gap: 15px; }
    .top-btn { background: transparent; color: white; border: 1px solid white; padding: 2px 10px; border-radius: 4px; font-size: 14px; cursor: pointer; }
    
    /* মেইন হেডার */
    .main-header { background: white; padding: 20px; display: flex; align-items: center; border-bottom: 1px solid #ddd; }
    .school-info { margin-left: 20px; }
    .school-info h1 { color: #d32f2f; margin: 0; font-size: 32px; }
    .school-info p { color: #2e7d32; margin: 0; font-size: 18px; font-weight: bold; }

    /* নোটিশ বোর্ড স্টাইল */
    .notice-card { background: #76ba1b; color: white; padding: 10px; border-radius: 5px 5px 0 0; font-weight: bold; }
    .notice-item { background: #f9f9f9; padding: 10px; border-bottom: 1px solid #ddd; font-size: 14px; }

    /* ফুটার ডিজাইন */
    .footer { background: #1a1a1a; color: white; padding: 40px 20px; margin-top: 50px; }
    .footer h4 { color: #FFD700; border-bottom: 1px solid #444; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ১. উপরের অংশ (মন্তব্য ও লগইন) ---
st.markdown("""
    <div class="top-header">
        <button class="top-btn">মন্তব্য ▼</button>
        <button class="top-btn" style="background: white; color: red;">লগ ইন ⏻</button>
    </div>
    """, unsafe_allow_html=True)

# --- ২. স্কুলের লোগো ও নাম ---
st.markdown(f"""
    <div class="main-header">
        <img src="https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg" width="90">
        <div class="school-info">
            <h1>সানরাইজ কিন্ডারগার্টেন</h1>
            <p>SUN RISE KINDER GARTEN</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- ৩. মেইন মেনু ---
menu = st.tabs(["🏠 হোম পেজ", "📝 অনলাইন ভর্তি", "🎓 রেজাল্ট", "👥 প্রশাসন", "📞 যোগাযোগ"])

STD_COLS = ["ID", "Name_BN", "Name_EN", "Father_BN", "Mother_BN", "Class", "Phone", "Address", "Date"]

# --- ৪. হোম পেজ লেআউট ---
with menu[0]:
    col_main, col_side = st.columns([2.5, 1])
    
    with col_main:
        # স্লাইডার বা মেইন ছবি
        st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", use_container_width=True)
        
        # প্রধান শিক্ষকের বাণী সেকশন
        st.markdown("### 👤 প্রধান শিক্ষকের বাণী")
        c1, c2 = st.columns([1, 3])
        c1.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", width=180)
        c2.write("সানরাইজ কিন্ডারগার্টেন-এর অনলাইন পোর্টালে আপনাদের স্বাগতম। আমরা প্রতিটি শিক্ষার্থীর মেধা বিকাশে প্রতিশ্রুতিবদ্ধ।")

    with col_side:
        st.markdown('<div class="notice-card">📢 নোটিশ বোর্ড</div>', unsafe_allow_html=True)
        notices = [
            ("12 Feb 2026", "২০২৬ শিক্ষাবর্ষের ভর্তি শুরু।"),
            ("10 Feb 2026", "সিলেবাস ও পাঠ্যবই সংক্রান্ত নোটিশ।"),
            ("05 Jan 2026", "নতুন ক্লাসের রুটিন।")
        ]
        for dt, txt in notices:
            st.markdown(f'<div class="notice-item"><span style="color:blue; font-weight:bold;">{dt}</span><br>{txt}</div>', unsafe_allow_html=True)

# --- ৫. অনলাইন ভর্তি ফরম (আপনার ফরমের তথ্য অনুযায়ী) ---
with menu[1]:
    st.markdown("### 📝 ভর্তি আবেদন ফরম")
    with st.form("admission", clear_on_submit=True):
        st.info("ভর্তি ফরমের তথ্যের আলোকে নিচের ঘরগুলো পূরণ করুন।")
        c1, c2 = st.columns(2)
        n_bn = c1.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
        n_en = c2.text_input("Student Name (English Block)")
        f_bn = c1.text_input("২। পিতার নাম (বাংলা)")
        m_bn = c2.text_input("৪। মাতার নাম (বাংলা)")
        s_class = c1.selectbox("ভর্তির শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        phone = c2.text_input("মোবাইল নম্বর")
        addr = st.text_area("৫। ঠিকানা (গ্রাম, ডাকঘর, উপজেলা, জেলা)")
        
        if st.form_submit_button("আবেদন জমা দিন"):
            df = load_data("students.csv", STD_COLS)
            new_id = 202600 + len(df) + 1
            new_row = pd.DataFrame([[new_id, n_bn, n_en, f_bn, m_bn, s_class, phone, addr, str(date.today())]], columns=STD_COLS)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.success(f"সফলভাবে আবেদন জমা হয়েছে! আইডি: {new_id}")
            st.balloons()

# --- ৬. প্রফেশনাল ফুটার (Screenshot_11 অনুযায়ী) ---
st.markdown(f"""
    <div class="footer">
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div style="width: 300px;">
                <img src="https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg" width="70">
                <p>© ২০২৬ সর্বস্বত্ব সংরক্ষিত <br> সানরাইজ কিন্ডারগার্টেন</p>
            </div>
            <div style="width: 300px;">
                <h4>আমাদের ঠিকানা</h4>
                <p>হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ।<br>ফোন: ০১৭২৭-৪১৪১৩৪<br>ইমেইল: info@sunrise.edu.bd</p>
            </div>
            <div style="width: 300px;">
                <h4>প্রয়োজনীয় লিংক</h4>
                <p>• দিনাজপুর শিক্ষা বোর্ড<br>• মাধ্যমিক ও উচ্চশিক্ষা অধিদপ্তর<br>• শিক্ষক বাতায়ন</p>
            </div>
        </div>
        <hr style="border-color: #444; margin: 20px 0;">
        <p style="text-align: center; color: #888; font-size: 12px;">Developed by: Alamin Khan</p>
    </div>
    """, unsafe_allow_html=True)
