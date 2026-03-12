import streamlit as st
import pandas as pd
import os
from datetime import date
import plotly.express as px

# ডাটাবেস হ্যান্ডলিং
def load_data(file_name, columns):
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        for col in columns:
            if col not in df.columns: df[col] = ""
        return df
    return pd.DataFrame(columns=columns)

# পেজ সেটআপ
st.set_page_config(page_title="Sun Rise K.G. Admin", layout="wide", page_icon="🏫")

# --- প্রিমিয়াম ডিজাইন (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    .stMetric { background: linear-gradient(135deg, #ffffff 0%, #e3e9f3 100%); padding: 20px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.05); border-top: 4px solid #002D62; }
    .card { background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); margin-bottom: 20px; }
    .stButton>button { border-radius: 8px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    /* প্রিন্ট সেকশন স্টাইল */
    @media print { .no-print { display: none !important; } .print-only { display: block !important; } }
    </style>
    """, unsafe_allow_html=True)

# --- লগইন সিস্টেম ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
        # আপনার লোগো এখানে (GitHub এ আপলোড করা লোগোর লিঙ্ক দিতে পারেন)
        st.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg", width=180) 
        st.markdown("<h2 style='color: #002D62;'>সানরাইজ কিন্ডারগার্টেন অ্যাডমিন</h2>", unsafe_allow_html=True)
        user = st.text_input("ইউজারনেম", placeholder="Admin ID")
        pw = st.text_input("পাসওয়ার্ড", type="password", placeholder="Password")
        if st.button("লগইন করুন", use_container_width=True):
            if user == "admin" and pw == "12345":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("ভুল তথ্য দেওয়া হয়েছে")
    st.stop()

# --- সাইডবার ---
st.sidebar.image("https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg", width=120)
st.sidebar.markdown("<h2 style='text-align: center;'>অ্যাডমিন প্যানেল</h2>", unsafe_allow_html=True)
menu = ["🏠 ড্যাশবোর্ড", "📝 ভর্তি ফরম", "👥 শিক্ষার্থী তালিকা", "🎓 রেজাল্ট শিট", "🎟️ এডমিট কার্ড", "💰 ফিস কালেকশন"]
choice = st.sidebar.selectbox("মেনু নির্বাচন করুন", menu)

STD_COLS = ["ID", "Name_BN", "Name_EN", "Class", "Phone", "Father", "Address", "Admission_Date"]

# --- ১. ড্যাশবোর্ড ---
if choice == "🏠 ড্যাশবোর্ড":
    st.title("📊 স্কুল ওভারভিউ")
    df = load_data("students.csv", STD_COLS)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("মোট শিক্ষার্থী", len(df))
    c2.metric("শ্রেণী সংখ্যা", "৬টি")
    c3.metric("শিক্ষক সংখ্যা", "৪ জন")
    c4.metric("প্রতিষ্ঠিত", "২০২৫ খ্রিঃ")
    
    st.markdown("---")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.markdown("<div class='card'><h3>📈 শিক্ষার্থী ডিস্ট্রিবিউশন</h3>", unsafe_allow_html=True)
        if not df.empty:
            fig = px.pie(df, names='Class', hole=.4, color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        else: st.info("কোনো ডাটা নেই")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_r:
        st.markdown("<div class='card'><h3>📅 আজকের আপডেট</h3>", unsafe_allow_html=True)
        st.info(f"তারিখ: {date.today().strftime('%d %B, %Y')}")
        st.write("✅ সার্ভার অনলাইন")
        st.write("✅ ডাটাবেস ব্যাকআপ রেডি")
        st.markdown("</div>", unsafe_allow_html=True)

# --- ২. ভর্তি ফরম ---
elif choice == "📝 ভর্তি ফরম":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("📝 ডিজিটাল ভর্তি আবেদন ফরম")
    with st.form("admission_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        n_bn = c1.text_input("১। শিক্ষার্থীর নাম (বাংলা)")
        n_en = c2.text_input("Student Name (English Block)")
        f_bn = c1.text_input("২। পিতার নাম (বাংলা)")
        f_en = c2.text_input("Father's Name (English Block)")
        s_class = c1.selectbox("১১। ভর্তির শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        phone = c2.text_input("মোবাইল নম্বর")
        addr = st.text_area("৫। ঠিকানা")
        
        if st.form_submit_button("আবেদন সেভ করুন"):
            df = load_data("students.csv", STD_COLS)
            new_id = 202600 + len(df) + 1
            new_row = pd.DataFrame([[new_id, n_bn, n_en, s_class, phone, f_bn, addr, str(date.today())]], columns=STD_COLS)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.success(f"সফলভাবে নিবন্ধিত! আইডি: {new_id}")
            st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

# --- ৩. শিক্ষার্থী তালিকা (এডিট/ডিলিট/প্রিন্ট) ---
elif choice == "👥 শিক্ষার্থী তালিকা":
    st.header("👥 সকল শিক্ষার্থীর ডাটাবেস")
    df = load_data("students.csv", STD_COLS)
    
    search = st.text_input("🔍 নাম বা আইডি দিয়ে খুঁজুন")
    if search:
        df = df[df['Name_BN'].str.contains(search, na=False) | df['ID'].astype(str).contains(search, na=False)]
    
    st.dataframe(df, use_container_width=True)
    
    if st.button("📥 ডাটা এক্সেল ফাইল হিসেবে ডাউনলোড করুন"):
        df.to_csv("students_export.csv", index=False)
        st.download_button(label="Click to Download", data=df.to_csv(), file_name="students_list.csv")

# --- ৪. এডমিট কার্ড (প্রিন্ট ফরম্যাট) ---
elif choice == "🎟️ এডমিট কার্ড":
    st.header("🎟️ প্রবেশ পত্র জেনারেটর")
    target_id = st.number_input("শিক্ষার্থীর আইডি দিন", min_value=0)
    df = load_data("students.csv", STD_COLS)
    
    if st.button("এডমিট কার্ড তৈরি করুন"):
        student = df[df['ID'] == target_id]
        if not student.empty:
            s = student.iloc[0]
            st.markdown(f"""
            <div style="border: 4px solid #002D62; padding: 20px; width: 500px; margin: auto; background: white; font-family: sans-serif;">
                <table style="width: 100%;">
                    <tr>
                        <td style="width: 80px;"><img src="https://raw.githubusercontent.com/alaminkhan0012-debug/sunrise-school-management/main/Screenshot_9.jpg" width="70"></td>
                        <td style="text-align: center;">
                            <h2 style="margin: 0; color: #002D62;">Sun Rise Kinder Garten</h2>
                            <p style="margin: 0; font-size: 14px;">হূমাইপুর, বাজিতপুর, কিশোরগঞ্জ</p>
                        </td>
                    </tr>
                </table>
                <h3 style="text-align: center; border-bottom: 2px solid #002D62; padding-bottom: 5px;">ADMIT CARD</h3>
                <p><b>নাম:</b> {s['Name_BN']}</p>
                <p><b>আইডি:</b> {s['ID']} | <b>শ্রেণী:</b> {s['Class']}</p>
                <p><b>পরীক্ষা:</b> বার্ষিক পরীক্ষা - ২০২৬</p>
                <div style="margin-top: 40px; display: flex; justify-content: space-between;">
                    <span>_________________<br>অধ্যক্ষের স্বাক্ষর</span>
                    <span>_________________<br>অভিভাবকের স্বাক্ষর</span>
                </div>
            </div>
            <p style='text-align:center; color:gray; font-size:12px;'>কীবোর্ড থেকে Ctrl + P চেপে প্রিন্ট করুন</p>
            """, unsafe_allow_html=True)
        else: st.error("এই আইডি পাওয়া যায়নি।")

# লগআউট
if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()
