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

# --- প্রিমিয়াম কাস্টম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    /* টপ বার (মন্তব্য ও লগইন) */
    .top-header-bar {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        padding: 10px 50px;
        background-color: #f8f9fa;
    }
    .btn-comment { background-color: #ff3b30; color: white; padding: 5px 15px; border-radius: 5px; font-size: 14px; text-decoration: none; font-weight: bold; }
    .btn-login { background-color: #ff3b30; color: white; padding: 5px 15px; border-radius: 5px; font-size: 14px; text-decoration: none; font-weight: bold; }
    
    /* লোগো ও স্কুলের নাম সেকশন */
    .mid-header {
        display: flex;
        align-items: center;
        padding: 20px 50px;
        background: white;
    }
    .school-title-bn { color: #ff3b30; font-size: 38px; font-weight: bold; font-family: 'SolaimanLipi', sans-serif; line-height: 1.2; }
    .school-title-en { color: #2e7d32; font-size: 22px; font-weight: bold; }
    
    /* নেভিগেশন মেনু */
    .nav-container {
        background: white;
        border-top: 1px solid #eee;
        border-bottom: 2px solid #ddd;
        padding: 0 50px;
    }
    
    /* নোটিশ বোর্ড */
    .notice-head { background: #76ba1b; color: white; padding: 10px; font-weight: bold; border-radius: 5px 5px 0 0; display: flex; justify-content: space-between; }
    
    /* ফুটার */
    .footer-dark { background: #1a1a1a; color: #ccc; padding: 40px 50px; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- ১. টপ বার (মন্তব্য ও লগইন) ---
st.markdown("""
    <div class="top-header-bar">
        <a href="#" class="btn-comment">মন্তব্য ▼</a>
        <a href="#" class="btn-login">লগ ইন ▼</a>
    </div>
    """, unsafe_allow_html=True)

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

# --- ৩. নেভিগেশন মেনু ---
menu_options = ["হোম পেজ", "স্কুল প্রশাসন ▼", "প্রাতিষ্ঠানিক কার্যক্রম ▼", "গ্যালারি", "অন্যান্য তথ্য ▼", "যোগাযোগ", "ভর্তি তথ্য ▼", "অনলাইন ভর্তি ফরম", "রেজাল্ট অনুসন্ধান"]
tabs = st.tabs(menu_options)

STD_COLS = ["ID", "Name_BN", "Name_EN", "Father_BN", "Mother_BN", "F_Job", "Class", "Phone", "Address", "Date"]

# --- ৪. হোম পেজ কন্টেন্ট ---
with tabs[0]:
    col_main, col_notice = st.columns([2.5, 1])
    
    with col_main:
        # স্লাইডার ইমেজ
        st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", use_container_width=True)
        
        # প্রধান শিক্ষকের বাণী
        st.markdown("### প্রধান শিক্ষকের বাণী")
        c1, c2 = st.columns([1, 2.5])
        c1.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", width=180)
        c2.write("সানরাইজ কিন্ডারগার্টেন এর পক্ষ থেকে সবাইকে স্বাগতম। আমরা উন্নত ও নৈতিক শিক্ষার মাধ্যমে একটি আদর্শ ভবিষ্যৎ প্রজন্ম গড়তে বদ্ধপরিকর। আমাদের রয়েছে দক্ষ শিক্ষক মণ্ডলী এবং আধুনিক পাঠদান পদ্ধতি।")
    
    with col_notice:
        st.markdown('<div class="notice-head"><span>নোটিশ বোর্ড</span><span>⬇️</span></div>', unsafe_allow_html=True)
        st.info("📌 ২০২৬ শিক্ষাবর্ষের ভর্তি ফরম বিতরণ শুরু হয়েছে।")
        st.info("📌 আগামী ২০শে মার্চ স্কুল ড্রেস কোড চেক করা হবে।")
        st.info("📌 প্রথম সাময়িক পরীক্ষার রুটিন ডাউনলোড করুন।")
        st.button("সকল নোটিশ...")

# --- ৫. অনলাইন ভর্তি ফরম ---
with tabs[7]:
    st.markdown("## 📝 অনলাইন ভর্তি আবেদন ফরম")
    with st.form("web_admission", clear_on_submit=True):
        st.markdown("#### শিক্ষার্থীর ব্যক্তিগত তথ্য")
        c1, c2 = st.columns(2)
        n_bn = c1.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
        n_en = c2.text_input("Student Name (English Block)")
        f_bn = c1.text_input("২। পিতার নাম (বাংলা)")
        f_en = c2.text_input("Father's Name (English Block)")
        m_bn = c1.text_input("৪। মাতার নাম (বাংলা)")
        m_en = c2.text_input("Mother's Name (English Block)")
        
        st.markdown("#### অন্যান্য তথ্য")
        c3, c4 = st.columns(2)
        f_job = c3.text_input("৬। পিতার পেশা")
        s_class = c4.selectbox("১১। ভর্তির শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        mobile = c3.text_input("মোবাইল নম্বর")
        dob = c4.date_input("৭। জন্ম তারিখ")
        
        addr = st.text_area("৫। ঠিকানা (গ্রাম, ডাকঘর, উপজেলা, জেলা)")
        
        if st.form_submit_button("আবেদন জমা দিন"):
            df = load_data("students.csv", STD_COLS)
            new_id = 2026001 + len(df)
            new_row = pd.DataFrame([[new_id, n_bn, n_en, f_bn, m_bn, f_job, s_class, mobile, addr, str(date.today())]], columns=STD_COLS)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.success(f"আবেদন সফল! আপনার আইডি: {new_id}")

# --- ৬. ফুটার সেকশন ---
st.markdown(f"""
    <div class="footer-dark">
        <div style="display: flex; justify-content: space-between;">
            <div style="width: 30%;">
                <img src="https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg" width="80"><br><br>
                <p>© ২০২৬ সর্বস্বত্ব সংরক্ষিত <br> সানরাইজ কিন্ডারগার্টেন</p>
            </div>
            <div style="width: 30%;">
                <h4>যোগাযোগ</h4>
                <p>হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ।<br>ফোন: ০১৭২৭-৪১৪১৩৪<br>ইমেইল: info@sunrise.edu.bd</p>
            </div>
            <div style="width: 30%;">
                <h4>গুরুত্বপূর্ণ লিংক</h4>
                <p>দিনাজপুর শিক্ষা বোর্ড<br>মাধ্যমিক ও উচ্চশিক্ষা অধিদপ্তর<br>শিক্ষক বাতায়ন</p>
            </div>
        </div>
        <hr style="border-color: #333;">
        <p style="text-align: center; font-size: 12px;">Developed with ❤️ for Sun Rise K.G.</p>
    </div>
    """, unsafe_allow_html=True)
