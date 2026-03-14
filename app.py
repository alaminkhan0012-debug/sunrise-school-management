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

# --- কাস্টম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .header { background: #fff; padding: 10px; border-bottom: 3px solid red; display: flex; align-items: center; }
    .school-name { color: red; font-size: 30px; font-weight: bold; margin-left: 20px; }
    .nav-bar { background: #f8f9fa; padding: 10px; border-bottom: 1px solid #ddd; margin-bottom: 20px; }
    .notice-board { background: #76ba1b; color: white; padding: 10px; border-radius: 5px; }
    .footer { background: #1a1a1a; color: white; padding: 40px; margin-top: 50px; }
    .card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- হেডার সেকশন (Screenshot_8 এর মতো) ---
st.markdown(f"""
    <div class="header">
        <img src="https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg" width="80">
        <div class="school-name">সানরাইজ কিন্ডারগার্টেন <br> <span style="font-size:18px; color:green;">SUN RISE KINDER GARTEN</span></div>
    </div>
    """, unsafe_allow_html=True)

# --- সাইডবার মেনু ---
st.sidebar.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg", width=100)
menu = ["🏠 হোম পেজ", "📝 অনলাইন ভর্তি", "🎓 রেজাল্ট", "🎟️ এডমিট কার্ড", "🔐 অ্যাডমিন প্যানেল"]
choice = st.sidebar.radio("Main Menu", menu)

STD_COLS = ["ID", "Name_BN", "Name_EN", "Father_BN", "Mother_BN", "Class", "Phone", "Address", "Date"]

# --- ১. হোম পেজ (Screenshot_8 & 10 অনুযায়ী) ---
if choice == "🏠 হোম পেজ":
    # স্লাইডার ইমেজ
    st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", use_container_width=True)
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.markdown("### প্রধান শিক্ষকের বাণী")
        c1, c2 = st.columns([1, 2])
        with c1:
            st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", width=200)
        with c2:
            st.write("শিক্ষাই জাতির মেরুদণ্ড। সানরাইজ কিন্ডারগার্টেন প্রতিটি শিশুর মেধা বিকাশে নিরলস কাজ করে যাচ্ছে। আমাদের লক্ষ্য আধুনিক ও নৈতিক শিক্ষার সমন্বয়।")
        
        st.markdown("---")
        st.markdown("### আমাদের লক্ষ্য")
        st.write("আমরা বিশ্বাস করি প্রতিটি শিশু অনন্য। তাদের সৃজনশীলতা এবং সুপ্ত প্রতিভা বিকাশের জন্য আমরা একটি চমৎকার পরিবেশ প্রদান করি।")

    with col_side:
        st.markdown("<div class='notice-board'>📢 নোটিশ বোর্ড</div>", unsafe_allow_html=True)
        st.info("📌 ২০২৫ শিক্ষাবর্ষের ভর্তি ফরম পাওয়া যাচ্ছে।")
        st.info("📌 বার্ষিক পরীক্ষার রুটিন প্রকাশিত হয়েছে।")
        st.info("📌 স্কুল ইউনিফর্ম সংক্রান্ত নতুন নির্দেশনা।")

# --- ২. অনলাইন ভর্তি (Screenshot_7/Form অনুযায়ী) ---
elif choice == "📝 অনলাইন ভর্তি":
    st.title("📝 অনলাইন ভর্তি আবেদন")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    with st.form("admission", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            n_bn = st.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
            f_bn = st.text_input("২। পিতার নাম (বাংলা)")
            m_bn = st.text_input("৪। মাতার নাম (বাংলা)")
            s_class = st.selectbox("ভর্তির শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        with c2:
            n_en = st.text_input("Student Name (English Block)")
            f_en = st.text_input("Father's Name (Block)")
            m_en = st.text_input("Mother's Name (Block)")
            mobile = st.text_input("মোবাইল নম্বর")
        
        addr = st.text_area("৫। ঠিকানা (গ্রাম, ডাকঘর, উপজেলা, জেলা)")
        
        if st.form_submit_button("আবেদন জমা দিন"):
            df = load_data("students.csv", STD_COLS)
            new_id = 202500 + len(df) + 1
            new_row = pd.DataFrame([[new_id, n_bn, n_en, f_bn, m_bn, s_class, mobile, addr, str(date.today())]], columns=STD_COLS)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.success(f"আবেদন সফল! আপনার আইডি: {new_id}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- ৩. অ্যাডমিন প্যানেল (এডিট/ডিলিট অপশনসহ) ---
elif choice == "🔐 অ্যাডমিন প্যানেল":
    if 'auth' not in st.session_state: st.session_state['auth'] = False
    
    if not st.session_state['auth']:
        user = st.text_input("Admin User")
        pw = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == "admin" and pw == "12345":
                st.session_state['auth'] = True
                st.rerun()
    else:
        st.title("📊 শিক্ষার্থী ডাটাবেস")
        df = load_data("students.csv", STD_COLS)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### তথ্য সংশোধন/মুছে ফেলা")
        del_id = st.number_input("শিক্ষার্থীর আইডি দিন", min_value=0)
        if st.button("তথ্য ডিলিট করুন"):
            df = df[df['ID'] != del_id]
            df.to_csv("students.csv", index=False)
            st.warning(f"আইডি {del_id} মুছে ফেলা হয়েছে।")
            st.rerun()
        
        if st.button("Logout"):
            st.session_state['auth'] = False
            st.rerun()

# --- ফুটার সেকশন (Screenshot_11 অনুযায়ী) ---
st.markdown(f"""
    <div class="footer">
        <div style="display: flex; justify-content: space-between;">
            <div style="width: 30%;">
                <img src="https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg" width="60">
                <p>© ২০২৬ সর্বস্বত্ব সংরক্ষিত <br> সানরাইজ কিন্ডারগার্টেন</p>
            </div>
            <div style="width: 30%;">
                <h4>যোগাযোগ</h4>
                <p>হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ<br>মোবাইল: +৮৮০ ১৭২৭-৪১৪১৩৪<br>ইমেইল: info@sunrise.edu.bd</p>
            </div>
            <div style="width: 30%;">
                <h4>প্রয়োজনীয় লিংক</h4>
                <p>মাধ্যমিক ও উচ্চশিক্ষা অধিদপ্তর<br>দিনাজপুর শিক্ষা বোর্ড<br>শিক্ষক বাতায়ন</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
