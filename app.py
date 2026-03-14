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
    .top-header-bar { display: flex; justify-content: flex-end; gap: 10px; padding: 10px 50px; background-color: #f8f9fa; }
    .school-title-bn { color: #ff3b30; font-size: 38px; font-weight: bold; line-height: 1.2; }
    .school-title-en { color: #2e7d32; font-size: 22px; font-weight: bold; }
    .footer-dark { background: #1a1a1a; color: #ccc; padding: 40px 50px; margin-top: 50px; }
    /* কমেন্ট বক্স স্টাইল */
    .comment-container { background: #000; padding: 20px; border-radius: 5px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ১. টপ বার (লগইন ও মন্তব্য বাটন) ---
col_top1, col_top2 = st.columns([8, 2])
with col_top2:
    t1, t2 = st.columns(2)
    show_comment = t1.button("মন্তব্য ▼")
    show_login = t2.button("লগ ইন ▼")

# --- ২. লগইন পপ-আপ/ফর্ম সেকশন ---
if show_login:
    with st.expander("🔐 অ্যাডমিন লগইন করুন", expanded=True):
        u_name = st.text_input("ইউজারনেম")
        u_pass = st.text_input("পাসওয়ার্ড", type="password")
        if st.button("প্রবেশ করুন"):
            if u_name == "admin" and u_pass == "12345":
                st.session_state['logged_in'] = True
                st.success("লগইন সফল!")
                st.rerun()
            else:
                st.error("ভুল ইউজারনেম বা পাসওয়ার্ড!")

# --- ৩. মেইন হেডার (লোগো ও নাম) ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg", width=120)
with col_text:
    st.markdown(f"""
        <div style='margin-left: -50px;'>
            <div class="school-title-bn">সানরাইজ কিন্ডারগার্টেন</div>
            <div class="school-title-en">SUN RISE KINDER GARTEN</div>
        </div>
        """, unsafe_allow_html=True)

# --- ৪. নেভিগেশন মেনু ---
menu_options = ["হোম পেজ", "স্কুল প্রশাসন ▼", "প্রাতিষ্ঠানিক কার্যক্রম ▼", "গ্যালারি", "অনলাইন ভর্তি ফরম", "রেজাল্ট অনুসন্ধান"]
if st.session_state['logged_in']:
    menu_options.append("📊 অ্যাডমিন ড্যাশবোর্ড")

tabs = st.tabs(menu_options)

STD_COLS = ["ID", "Name_BN", "Name_EN", "Father_BN", "Mother_BN", "Class", "Phone", "Address", "Date"]

# --- ৫. হোম পেজ ও মন্তব্য বক্স ---
with tabs[0]:
    col_main, col_side = st.columns([2.5, 1])
    with col_main:
        st.image("https://ckgghs.edu.bd/uploads/sliders/1709444391.jpg", use_container_width=True)
        
        # আপনার দেওয়া ছবির মতো মন্তব্য সেকশন
        st.markdown("### 💬 আপনার মতামত জানান")
        with st.container():
            st.markdown('<div style="background:#f0f2f6; padding:20px; border-radius:10px;">', unsafe_allow_html=True)
            c_name = st.text_input("নাম :", placeholder="আপনার নাম লিখুন")
            col_mail, col_phone = st.columns(2)
            c_email = col_mail.text_input("ইমেইল :", placeholder="example@mail.com")
            c_phone = col_phone.text_input("ফোন :", placeholder="017xx-xxxxxx")
            c_msg = st.text_area("মন্তব্য :", placeholder="আপনার মূল্যবান মতামত লিখুন...")
            if st.button("পাঠান", type="primary"):
                st.success("আপনার মন্তব্যটি সফলভাবে পাঠানো হয়েছে!")
            st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        st.info("📢 ২০২৬ শিক্ষাবর্ষের ভর্তি চলছে।")
        st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_10.jpg", caption="প্রধান শিক্ষক", width=150)

# --- ৬. অনলাইন ভর্তি ফরম ---
with tabs[4]:
    st.markdown("## 📝 অনলাইন ভর্তি আবেদন ফরম")
    with st.form("admission_form"):
        c1, c2 = st.columns(2)
        n_bn = c1.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
        n_en = c2.text_input("Student Name (English)")
        f_bn = c1.text_input("২। পিতার নাম (বাংলা)")
        m_bn = c2.text_input("৪। মাতার নাম (বাংলা)")
        s_class = c1.selectbox("ভর্তির শ্রেণী", ["Play", "Nursery", "One", "Two", "Three"])
        phone = c2.text_input("মোবাইল নম্বর")
        if st.form_submit_button("আবেদন জমা দিন"):
            st.success("আবেদন জমা হয়েছে!")

# --- ৭. অ্যাডমিন ড্যাশবোর্ড (লগইন করলেই দেখা যাবে) ---
if st.session_state['logged_in']:
    with tabs[-1]:
        st.header("📊 ম্যানেজমেন্ট প্যানেল")
        st.write("এখানে আপনি শিক্ষার্থীদের তালিকা দেখতে এবং এডিট করতে পারবেন।")
        if st.button("লগ আউট"):
            st.session_state['logged_in'] = False
            st.rerun()

# --- ৮. ফুটার ---
st.markdown("""
    <div class="footer-dark">
        <div style="display: flex; justify-content: space-between;">
            <div><img src="https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg" width="60"><p>© ২০২৬ সানরাইজ কিন্ডারগার্টেন</p></div>
            <div><h4>যোগাযোগ</h4><p>হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ।<br>ফোন: ০১৭২৭-৪১৪১৩৪</p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
