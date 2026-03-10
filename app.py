import streamlit as st
import pandas as pd
import os

# ডাটাবেস চেক
def load_data():
    if os.path.exists("students.csv"):
        return pd.read_csv("students.csv")
    else:
        return pd.DataFrame(columns=["Name", "Roll", "Class", "Guardian", "Phone"])

st.set_page_config(page_title="Sun Rise Management", layout="wide")
st.title("🏫 Sun Rise Kinder Garten Management")

menu = ["ড্যাশবোর্ড", "ছাত্র ভর্তি", "ছাত্র তালিকা"]
choice = st.sidebar.selectbox("মেনু", menu)

if choice == "ছাত্র ভর্তি":
    st.header("📝 নতুন ছাত্র ভর্তি")
    with st.form("admission"):
        name = st.text_input("নাম")
        roll = st.text_input("রোল")
        s_class = st.selectbox("শ্রেণী", ["Play", "Nursery", "One", "Two", "Three", "Four", "Five"])
        guardian = st.text_input("পিতার নাম")
        phone = st.text_input("মোবাইল")
        if st.form_submit_button("সেভ করুন"):
            df = load_data()
            new_data = pd.DataFrame([[name, roll, s_class, guardian, phone]], columns=df.columns)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv("students.csv", index=False)
            st.success("সফলভাবে সেভ হয়েছে!")

elif choice == "ছাত্র তালিকা":
    st.header("📋 তালিকা")
    df = load_data()
    st.dataframe(df, use_container_width=True)

else:
    st.header("📊 ড্যাশবোর্ড")
    df = load_data()
    st.metric("মোট ছাত্র", len(df))