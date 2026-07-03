import streamlit as st
import pandas as pd

# 1. Dummy Data (အိမ်ဆောက်ပစ္စည်းဆိုင်အတွက် ကုန်ပစ္စည်းစာရင်း)
data = {
    "Product": ["Cement (50kg)", "PVC Pipe (1 inch)", "Nails (1kg)", "Paint (5L)"],
    "Price": [12000, 3500, 2500, 25000],
    "Stock": [100, 50, 200, 30]
}
df = pd.DataFrame(data)

st.set_page_config(page_title="Hardware POS System", layout="wide")
st.title("🏗️ အိမ်ဆောက်ပစ္စည်းအရောင်း POS")

# 2. Sidebar Navigation
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Sale"])

if menu == "Dashboard":
    st.subheader("Inventory လက်ကျန်")
    st.table(df)

elif menu == "Sale":
    st.subheader("ပစ္စည်းရောင်းချခြင်း")
    product = st.selectbox("ပစ္စည်းရွေးပါ", df["Product"])
    qty = st.number_input("အရေအတွက်", min_value=1, step=1)
    
    # ရောင်းချမှုတွက်ချက်ခြင်း
    price = df[df["Product"] == product]["Price"].values[0]
    total = price * qty
    
    if st.button("Confirm Sale"):
        st.success(f"{product} {qty} ခု ရောင်းချပြီးပါပြီ။")
        st.write(f"စုစုပေါင်းကျသင့်ငွေ: {total} ကျပ်")