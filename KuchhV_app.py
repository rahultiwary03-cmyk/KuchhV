import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. SETUP & DATABASE
# ==========================================
st.set_page_config(page_title="KuchhV | Har Zarurat, Ek Platform", layout="wide", page_icon="🚀")

REQUIREMENTS_FILE = "req_v4.csv"
PARTNERS_FILE = "partners_v4.csv"
ORDERS_FILE = "orders_v4.csv"

INDIAN_SERVICES = [
    "Grocery & Daily Needs", "Fresh Vegetables & Fruits", "Dairy & Milk Delivery", 
    "Plumber", "Electrician", "Carpenter", "AC Repair & Servicing", 
    "IT Freelancer (Python/Excel)", "Web Developer", "Graphic Designer",
    "Tractor Rental", "JCB & Crane Rental", "Mini Truck (Tata Ace) Booking", "Bike Taxi",
    "CA & GST Filing (Pragya Kendra)", "Lawyer & Notary", "Real Estate (Rent/Buy)",
    "Doctor Appointment", "Medicine Delivery", "Lab Test at Home",
    "Men's Salon", "Women's Parlour", "Bridal Makeup", 
    "Tent House & Decorator", "Caterers (Halwai)", "Labour Contractor (Daily Wage)"
]

for file, cols in [
    (REQUIREMENTS_FILE, ["Timestamp", "Phone", "Category", "Requirement", "Location", "Status"]),
    (PARTNERS_FILE, ["Phone", "Password", "Business_Name", "Category", "Verification_Status", "Base_Price"]),
    (ORDERS_FILE, ["Timestamp", "Customer_Phone", "Partner", "Service", "Price", "Platform_Fee", "Partner_Earning", "Status"])
]:
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)

def load_data(file_name):
    return pd.read_csv(file_name, dtype=str)

def save_data(file_name, new_data):
    df = pd.DataFrame([new_data])
    df.to_csv(file_name, mode='a', header=False, index=False)

def overwrite_data(file_name, df):
    df.to_csv(file_name, index=False)

# Professional Colorful CSS
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%); }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .support-box { background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px; border: 1px solid rgba(255,255,255,0.3); }
    .price-card { background: white; padding: 20px; border-radius: 12px; border-left: 5px solid #2563eb; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px;}
    .fee-text { color: #dc2626; font-size: 14px; font-weight: 600;}
    .earning-text { color: #059669; font-size: 15px; font-weight: 700;}
    h1, h2, h3 { color: #0f172a; }
    </style>
""", unsafe_allow_html=True)

if 'logged_in_partner' not in st.session_state:
    st.session_state['logged_in_partner'] = None

# ==========================================
# 2. APP NAVIGATION & 24/7 SUPPORT
# ==========================================
st.sidebar.title("📱 KuchhV Super App")
st.sidebar.caption("Har Zarurat, Ek Platform.")
st.sidebar.write("---")
app_mode = st.sidebar.radio("Main Menu:", ["🏠 Customer Marketplace", "📢 Requirement Hub", "💼 Partner Portal", "⚙️ Admin Center"])
st.sidebar.write("---")

# 24/7 Customer Support Module
st.sidebar.markdown("""
<div class='support-box'>
    <h3 style='color: white; margin-bottom: 5px;'>🎧 24/7 Customer Support</h3>
    <p style='font-size: 13px; margin-bottom: 5px;'>Need help with booking or verification?</p>
    <p style='margin: 0; font-weight: bold;'>📞 8521413089</p>
    <p style='margin: 0; font-size: 12px;'>✉️ Rahultiwary03@gmail.com</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. CUSTOMER MARKETPLACE
# ==========================================
if app_mode == "🏠 Customer Marketplace":
    st.title("🛍️ KuchhV Marketplace")
    st.markdown("### Search anything. Compare prices. Book the lowest.")
    
    selected_service = st.selectbox("🔍 What do you need today?", ["-- Select or Type Here --"] + INDIAN_SERVICES)
    
    if selected_service != "-- Select or Type Here --":
        st.write("---")
        st.subheader(f"Available Partners for '{selected_service}'")
        
        partner_df = load_data(PARTNERS_FILE)
        available = partner_df[(partner_df['Category'] == selected_service) & (partner_df['Verification_Status'] == 'Verified ✅')].copy()
        
        if not available.empty:
            available['Base_Price'] = pd.to_numeric(available['Base_Price'], errors='coerce').fillna(999)
            available = available.sort_values(by='Base_Price')
            
            st.success(f"✅ Found {len(available)} verified partner(s). Showing lowest prices first.")
            
            for index, row in available.iterrows():
                partner_name = row['Business_Name']
                price = float(row['Base_Price'])
                platform_fee = price * 0.01 
                partner_earning = price - platform_fee
                
                st.markdown(f"""
                <div class='price-card'>
                    <h3 style='margin-top:0;'>🏪 {partner_name}</h3>
                    <p style='font-size: 22px; font-weight: 800; color: #1e293b; margin: 5px 0;'>Price: ₹{price:,.2f}</p>
                    <p class='fee-text' style='margin:0;'>KuchhV Platform Fee (1%): ₹{platform_fee:,.2f}</p>
                    <p class='earning-text' style='margin:0;'>Partner Earns: ₹{partner_earning:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"Book {partner_name} Now"):
                    with st.form(f"book_{index}"):
                        cust_phone = st.text_input("Your Mobile Number:")
                        if st.form_submit_button("Confirm Booking"):
                            if cust_phone:
                                save_data(ORDERS_FILE, {
                                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "Customer_Phone": cust_phone, "Partner": partner_name, "Service": selected_service,
                                    "Price": price, "Platform_Fee": platform_fee, "Partner_Earning": partner_earning, "Status": "Pending"
                                })
                                st.success("🎉 Booking Confirmed! The partner will contact you shortly.")
                            else:
                                st.error("Please enter your mobile number.")
        else:
            st.warning("No verified partners found for this service right now.")
            st.info("💡 Post this in the Requirement Hub and local partners will bid for your request!")

# ==========================================
# 4. REQUIREMENT HUB
# ==========================================
elif app_mode == "📢 Requirement Hub":
    st.title("📢 Custom Requirement Hub")
    st.write("Need bulk materials, a large workforce, or custom services? Post it here.")
    
    with st.container():
        st.markdown("<div style='background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
        with st.form("req_form"):
            col1, col2 = st.columns(2)
            with col1:
                req_cat = st.selectbox("Category", INDIAN_SERVICES)
                loc = st.text_input("Pincode / City")
            with col2:
                phone = st.text_input("Mobile Number")
            
            desc = st.text_area("Detail your exact need:")
            
            if st.form_submit_button("Broadcast to Partners 🚀"):
                if phone and desc and loc:
                    save_data(REQUIREMENTS_FILE, {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Phone": phone, "Category": req_cat, "Requirement": desc, "Location": loc, "Status": "Open"
                    })
                    st.success("✅ Broadcasted! Partners will bid on your requirement.")
                    st.balloons()
                else:
                    st.error("Please fill all details.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. PARTNER PORTAL
# ==========================================
elif app_mode == "💼 Partner Portal":
    st.title("💼 Partner Business Portal")
    
    if st.session_state['logged_in_partner'] is None:
        t1, t2 = st.tabs(["🔐 Login", "📝 Register Business"])
        
        with t2:
            st.subheader("Join KuchhV & Grow Your Business")
            st.info("KuchhV Platform charges only 1% fee on your total billing.")
            with st.form("reg_form"):
                biz_name = st.text_input("Business / Freelancer Name")
                phone = st.text_input("Mobile Number")
                pwd = st.text_input("Create Password", type="password")
                cat = st.selectbox("Your Primary Category", INDIAN_SERVICES)
                base_price = st.number_input("Your Starting Price / Hourly Rate (₹)", min_value=10, value=100)
                
                if st.form_submit_button("Register"):
                    pdf = load_data(PARTNERS_FILE)
                    if phone in pdf['Phone'].values:
                        st.error("Mobile Number already registered!")
                    else:
                        save_data(PARTNERS_FILE, {
                            "Phone": phone, "Password": pwd, "Business_Name": biz_name, 
                            "Category": cat, "Verification_Status": "Pending", "Base_Price": base_price
                        })
                        st.success("✅ Registered! Please wait for Admin approval.")
                        
        with t1:
            st.subheader("Secure Login")
            l_phone = st.text_input("Mobile Number ")
            l_pwd = st.text_input("Password ", type="password")
            
            if st.button("Login Now"):
                pdf = load_data(PARTNERS_FILE)
                user = pdf[(pdf['Phone'] == l_phone) & (pdf['Password'] == l_pwd)]
                
                if not user.empty:
                    stat = user.iloc[0]['Verification_Status']
                    if stat == 'Verified ✅':
                        st.session_state['logged_in_partner'] = user.iloc[0]['Business_Name']
                        st.success("Login Successful!")
                        st.rerun()
                    else:
                        st.error(f"Account Status: {stat}. Admin approval is required.")
                else:
                    st.error("Invalid credentials.")
    else:
        st.success(f"👋 Welcome, {st.session_state['logged_in_partner']}!")
        if st.button("Logout"):
            st.session_state['logged_in_partner'] = None
            st.rerun()
            
        st.subheader("📦 Your Direct Orders")
        odf = load_data(ORDERS_FILE)
        my_orders = odf[odf['Partner'] == st.session_state['logged_in_partner']]
        st.dataframe(my_orders, use_container_width=True)

# ==========================================
# 6. SUPER ADMIN CENTER (Full Database Control)
# ==========================================
elif app_mode == "⚙️ Admin Center":
    st.title("⚙️ Super Admin Control Room")
    st.write("Complete Database Management System (View, Add, Edit, Delete Records)")
    
    t_partners, t_orders, t_reqs = st.tabs(["👥 Manage Partners", "🛒 Manage Orders", "📢 Manage Requirements"])
    
    with t_partners:
        st.subheader("Partner Database (Add/Modify/Delete)")
        pdf = load_data(PARTNERS_FILE)
        edited_pdf = st.data_editor(pdf, num_rows="dynamic", use_container_width=True, key="edit_partners")
        if st.button("💾 Save Partner Changes"):
            overwrite_data(PARTNERS_FILE, edited_pdf)
            st.success("Partner database updated successfully!")
            
    with t_orders:
        st.subheader("Orders Database (Add/Modify/Delete)")
        odf = load_data(ORDERS_FILE)
        edited_odf = st.data_editor(odf, num_rows="dynamic", use_container_width=True, key="edit_orders")
        if st.button("💾 Save Order Changes"):
            overwrite_data(ORDERS_FILE, edited_odf)
            st.success("Orders database updated successfully!")

    with t_reqs:
        st.subheader("Requirement Hub Database (Add/Modify/Delete)")
        rdf = load_data(REQUIREMENTS_FILE)
        edited_rdf = st.data_editor(rdf, num_rows="dynamic", use_container_width=True, key="edit_reqs")
        if st.button("💾 Save Requirement Changes"):
            overwrite_data(REQUIREMENTS_FILE, edited_rdf)
            st.success("Requirements database updated successfully!")
