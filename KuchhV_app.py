import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. SETUP & PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="KuchhV | Super App", layout="wide", page_icon="🚀")

# File names changed to v2 so old data doesn't crash the new structure
PARTNERS_FILE = "partners_v2.csv"
ORDERS_FILE = "orders_v2.csv"

if not os.path.exists(PARTNERS_FILE):
    pd.DataFrame(columns=["Phone", "Password", "Business_Name", "Category", "Verification_Status"]).to_csv(PARTNERS_FILE, index=False)

if not os.path.exists(ORDERS_FILE):
    pd.DataFrame(columns=["Timestamp", "Customer_Phone", "Category", "Requirement", "Status", "Partner_Assigned"]).to_csv(ORDERS_FILE, index=False)

def load_data(file_name):
    # Ensure phone numbers are treated as strings
    return pd.read_csv(file_name, dtype={"Phone": str, "Customer_Phone": str, "Password": str})

def save_data(file_name, new_data):
    df = pd.DataFrame([new_data])
    df.to_csv(file_name, mode='a', header=False, index=False)

# Custom CSS for UI
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%); color: white !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .category-box { padding: 20px; border-radius: 12px; background: #ffffff; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Login
if 'logged_in_partner' not in st.session_state:
    st.session_state['logged_in_partner'] = None

# ==========================================
# 2. APP NAVIGATION
# ==========================================
st.sidebar.title("📱 KuchhV Hub")
st.sidebar.write("---")
app_mode = st.sidebar.radio("Navigation Menu:", ["🏠 Customer App", "💼 Partner Portal", "⚙️ Admin Dashboard"])
st.sidebar.write("---")

# ==========================================
# 3. CUSTOMER APP (Order & Availability Logic)
# ==========================================
if app_mode == "🏠 Customer App":
    st.title("🛒 KuchhV - Har Zarurat, Ek Platform.")
    
    st.markdown("### 1. Aapko kya service chahiye?")
    category_list = ["Grocery & Retail", "Home Repairs", "IT Freelancers", "Asset Rentals", "Bike Taxi", "Healthcare"]
    selected_category = st.selectbox("Category chunein:", category_list)
    
    st.markdown("### 2. Available Partners Check")
    partner_df = load_data(PARTNERS_FILE)
    
    # Filter only Verified partners in the selected category
    available_partners = partner_df[(partner_df['Category'] == selected_category) & (partner_df['Verification_Status'] == 'Verified ✅')]
    
    if not available_partners.empty:
        st.success(f"✅ {len(available_partners)} Verified Partner(s) available in your area!")
        st.dataframe(available_partners[['Business_Name', 'Category']], use_container_width=True)
        
        with st.form("book_service_form"):
            customer_phone = st.text_input("Enter your Mobile Number to Book:")
            requirement = st.text_area("Order Details:")
            if st.form_submit_button("Book Now"):
                new_order = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Customer_Phone": customer_phone,
                    "Category": selected_category,
                    "Requirement": requirement,
                    "Status": "Direct Order",
                    "Partner_Assigned": "Pending Acceptance"
                }
                save_data(ORDERS_FILE, new_order)
                st.success("Order Placed Successfully! Partner will contact you.")
    else:
        st.error("⚠️ Koi verified partner abhi is category me available nahi hai.")
        st.info("💡 **Solution:** Apni zarurat niche likh dein, jaise hi koi partner aayega hum aapko connect karenge (Requirement Hub).")
        with st.form("requirement_hub_form"):
            customer_phone = st.text_input("Your Mobile Number:")
            requirement = st.text_area("Apni requirement detail me likhein:")
            if st.form_submit_button("Post to Requirement Hub"):
                new_order = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Customer_Phone": customer_phone,
                    "Category": selected_category,
                    "Requirement": requirement,
                    "Status": "Waitlist (Requirement Hub)",
                    "Partner_Assigned": "None"
                }
                save_data(ORDERS_FILE, new_order)
                st.success("Request added to Hub! Local partners notified.")

# ==========================================
# 4. PARTNER PORTAL (Login & Registration)
# ==========================================
elif app_mode == "💼 Partner Portal":
    st.title("💼 Partner Business Portal")
    
    if st.session_state['logged_in_partner'] is None:
        tab_login, tab_signup = st.tabs(["🔐 Login", "📝 New Registration"])
        
        with tab_signup:
            st.subheader("Partner Registration")
            with st.form("signup_form"):
                phone = st.text_input("Mobile Number")
                password = st.text_input("Create Password", type="password")
                business_name = st.text_input("Business / Shop Name")
                category = st.selectbox("Category", ["Grocery & Retail", "Home Repairs", "IT Freelancers", "Asset Rentals", "Bike Taxi", "Healthcare"])
                
                if st.form_submit_button("Register"):
                    partner_df = load_data(PARTNERS_FILE)
                    if phone in partner_df['Phone'].values:
                        st.error("Yeh number pehle se registered hai! Login karein.")
                    else:
                        new_partner = {"Phone": phone, "Password": password, "Business_Name": business_name, "Category": category, "Verification_Status": "Pending"}
                        save_data(PARTNERS_FILE, new_partner)
                        st.success("Registration Successful! Please wait for Admin Approval.")
                        
        with tab_login:
            st.subheader("Partner Login")
            phone_login = st.text_input("Enter Mobile Number")
            pass_login = st.text_input("Enter Password", type="password")
            
            if st.button("Login"):
                partner_df = load_data(PARTNERS_FILE)
                user = partner_df[(partner_df['Phone'] == phone_login) & (partner_df['Password'] == pass_login)]
                
                if not user.empty:
                    status = user.iloc[0]['Verification_Status']
                    if status == 'Verified ✅':
                        st.session_state['logged_in_partner'] = user.iloc[0]['Business_Name']
                        st.success("Login Successful!")
                        st.rerun()
                    else:
                        st.error(f"Account Status: {status}. Admin approval pending.")
                else:
                    st.error("Galat Mobile Number ya Password.")
    else:
        st.success(f"Welcome, {st.session_state['logged_in_partner']}!")
        if st.button("Logout"):
            st.session_state['logged_in_partner'] = None
            st.rerun()
            
        st.subheader("Your Live Orders & Leads")
        orders_df = load_data(ORDERS_FILE)
        st.dataframe(orders_df, use_container_width=True)

# ==========================================
# 5. ADMIN DASHBOARD (Approval Process)
# ==========================================
elif app_mode == "⚙️ Admin Dashboard":
    st.title("⚙️ Super Admin Center")
    
    partner_df = load_data(PARTNERS_FILE)
    st.subheader("Partner KYC & Verification")
    
    if not partner_df.empty:
        st.write("Edit the 'Verification_Status' below to approve partners.")
        edited_partner_df = st.data_editor(
            partner_df,
            column_config={
                "Password": None, # Hide passwords from admin view for security
                "Verification_Status": st.column_config.SelectboxColumn(
                    "Status", options=["Pending", "Verified ✅", "Rejected ❌"], required=True
                )
            },
            use_container_width=True
        )
        if st.button("💾 Save Verification Status"):
            # Update the original dataframe with edited status while keeping passwords intact
            partner_df['Verification_Status'] = edited_partner_df['Verification_Status']
            partner_df.to_csv(PARTNERS_FILE, index=False)
            st.success("Status Updated Successfully!")
    else:
        st.info("No partners registered yet.")
