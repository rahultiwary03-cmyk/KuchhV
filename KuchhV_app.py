import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. SETUP & PAGE CONFIGURATION
# ==========================================
# Wide layout for a premium professional look
st.set_page_config(page_title="KuchhV | Super App", layout="wide", page_icon="🚀")

REQUIREMENTS_FILE = "requirements.csv"
PARTNERS_FILE = "partners.csv"

# Create CSV files if they don't exist
if not os.path.exists(REQUIREMENTS_FILE):
    pd.DataFrame(columns=["Timestamp", "Category", "Description", "Budget", "Location", "Status"]).to_csv(REQUIREMENTS_FILE, index=False)

if not os.path.exists(PARTNERS_FILE):
    pd.DataFrame(columns=["Timestamp", "Business_Name", "Category", "Verification_Status"]).to_csv(PARTNERS_FILE, index=False)

def load_data(file_name):
    return pd.read_csv(file_name)

def save_data(file_name, new_data):
    df = pd.DataFrame([new_data])
    df.to_csv(file_name, mode='a', header=False, index=False)

# ==========================================
# 2. ADVANCED UI/UX (COLORFUL & PROFESSIONAL)
# ==========================================
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Sidebar Styling - Colorful Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%);
        color: white !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Title and Header Fonts */
    h1, h2, h3 {
        color: #0f172a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
    }
    
    /* App Slogan */
    .slogan {
        font-size: 26px;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #f59e0b, #e11d48);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    /* Category Boxes - Modern App Cards */
    .category-box {
        padding: 25px 15px;
        border-radius: 16px;
        background: #ffffff;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    .category-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 20px -3px rgba(59, 130, 246, 0.3);
        border-color: #3b82f6;
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
    }
    .cat-icon {
        font-size: 45px;
        margin-bottom: 12px;
        display: block;
    }
    .cat-title {
        font-size: 16px;
        font-weight: 700;
        color: #1e293b;
    }

    /* Beautiful Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 700;
        transition: 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8 0%, #4338ca 100%);
        transform: scale(1.03);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }
    
    /* DataFrame Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. APP NAVIGATION
# ==========================================
st.sidebar.title("📱 KuchhV Hub")
st.sidebar.caption("Pan-India Operations")
st.sidebar.write("---")
app_mode = st.sidebar.radio("Navigation Menu:", ["🏠 Customer App", "📢 Requirement Hub", "💼 Partner Portal", "⚙️ Admin Dashboard"])
st.sidebar.write("---")
st.sidebar.info("App Version: 2.0 (Pan-India Enterprise)")

# ==========================================
# 4. CUSTOMER HOME
# ==========================================
if app_mode == "🏠 Customer App":
    st.title("🛒 KuchhV")
    st.markdown("<div class='slogan'>Har Zarurat, Ek Platform.</div>", unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Search for Groceries, Mechanics, Taxis, PGs...", placeholder="E.g. Plumber in Chatra...")
    
    st.write("---")
    st.subheader("🔥 Top Services Near You")
    
    # 4-Column Grid for beautiful icons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='category-box'><span class='cat-icon'>🍎</span><span class='cat-title'>Grocery & Retail</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='category-box'><span class='cat-icon'>🏠</span><span class='cat-title'>Real Estate</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='category-box'><span class='cat-icon'>🔧</span><span class='cat-title'>Home Repairs</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='category-box'><span class='cat-icon'>📄</span><span class='cat-title'>E-Gov & CSC</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='category-box'><span class='cat-icon'>💻</span><span class='cat-title'>IT Freelancers</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='category-box'><span class='cat-icon'>🏥</span><span class='cat-title'>Healthcare</span></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='category-box'><span class='cat-icon'>🚜</span><span class='cat-title'>Asset Rentals</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='category-box'><span class='cat-icon'>🛵</span><span class='cat-title'>Bike Taxi</span></div>", unsafe_allow_html=True)

# ==========================================
# 5. REQUIREMENT HUB
# ==========================================
elif app_mode == "📢 Requirement Hub":
    st.title("📢 The Requirement Hub")
    st.info("💡 **Can't find what you need?** Post your custom requirement here and let local verified partners contact you.")
    
    with st.container():
        st.markdown("<div style='background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
        with st.form("requirement_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                req_type = st.selectbox("Select Service Category", ["Bulk Labour/Manpower", "IT/Developer", "Event & Catering", "Logistics/Truck", "Other"])
                location = st.text_input("Pincode / City Area (e.g. 825401)")
            with col_b:
                budget = st.text_input("Expected Budget (₹) - Optional")
                
            description = st.text_area("Detail your exact requirement here:", placeholder="Example: Need 10 labourers and 2 Rajmistris for 3 days...")
            
            st.write("") # Spacer
            submitted = st.form_submit_button("🚀 Broadcast to Local Partners")
            
            if submitted and description and location:
                new_req = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Category": req_type,
                    "Description": description,
                    "Budget": budget,
                    "Location": location,
                    "Status": "Open"
                }
                save_data(REQUIREMENTS_FILE, new_req)
                st.success("✅ Request Broadcasted Successfully! Partners will contact you soon.")
                st.balloons()
            elif submitted:
                st.error("⚠️ Please fill in the description and location.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. PARTNER PORTAL
# ==========================================
elif app_mode == "💼 Partner Portal":
    st.title("💼 Partner Business Portal")
    
    tab1, tab2 = st.tabs(["📝 Register Business", "📡 Live City Demands"])
    
    with tab1:
        st.markdown("### Join the KuchhV Network")
        with st.form("partner_form"):
            col1, col2 = st.columns(2)
            with col1:
                business_name = st.text_input("Business / Freelancer Name")
            with col2:
                category = st.selectbox("Primary Service Area", ["Retail Shop", "Professional Service", "Labour Contractor", "Fleet Owner", "Freelancer"])
            submitted = st.form_submit_button("Submit KYC for Verification")
            
            if submitted and business_name:
                new_partner = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Business_Name": business_name,
                    "Category": category,
                    "Verification_Status": "Pending"
                }
                save_data(PARTNERS_FILE, new_partner)
                st.success("✅ Application Submitted! Awaiting Admin Approval.")
                
    with tab2:
        st.markdown("### Live Requirements Near You")
        req_df = load_data(REQUIREMENTS_FILE)
        if not req_df.empty:
            open_reqs = req_df[req_df["Status"] == "Open"]
            st.dataframe(open_reqs[::-1], use_container_width=True)
        else:
            st.info("No active demands currently.")

# ==========================================
# 7. ADMIN DASHBOARD
# ==========================================
elif app_mode == "⚙️ Admin Dashboard":
    st.title("⚙️ Super Admin Center")
    st.write("Pan-India Operations & Verification Hub")
    
    req_df = load_data(REQUIREMENTS_FILE)
    partner_df = load_data(PARTNERS_FILE)
    
    tab_overview, tab_partners, tab_reqs = st.tabs(["📊 Analytics Overview", "👥 Partner Verification", "📝 Track Demands"])
    
    with tab_overview:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="📣 Total Demands", value=len(req_df), delta="Active")
        col2.metric(label="🤝 Registered Partners", value=len(partner_df), delta="Total")
        col3.metric(label="📍 Active Regions", value="1", delta="Pilot Mode")
        col4.metric(label="⚡ Platform Status", value="100%", delta="Online")
        
        st.divider()
        st.subheader("Partner Distribution by Category")
        if not partner_df.empty:
            cat_counts = partner_df['Category'].value_counts()
            st.bar_chart(cat_counts, color="#3b82f6")
        else:
            st.info("Not enough data to display analytics.")

    with tab_partners:
        st.subheader("Partner KYC & Verification")
        if not partner_df.empty:
            st.warning("⚠️ **Action Required:** Click on the 'Verification_Status' cell below to approve or reject partners.")
            edited_partner_df = st.data_editor(
                partner_df,
                column_config={
                    "Verification_Status": st.column_config.SelectboxColumn(
                        "Status",
                        help="Change the approval status",
                        options=["Pending", "Verified ✅", "Rejected ❌"],
                        required=True,
                    )
                },
                use_container_width=True,
                key="partner_editor"
            )
            
            if st.button("💾 Save Verification Status"):
                edited_partner_df.to_csv(PARTNERS_FILE, index=False)
                st.success("✅ Database Updated Successfully!")
        else:
            st.info("No partners registered yet.")

    with tab_reqs:
        st.subheader("Customer Requirement Engine")
        if not req_df.empty:
            status_filter = st.selectbox("Filter by Status", ["All", "Open", "Closed"])
            display_df = req_df if status_filter == "All" else req_df[req_df["Status"] == status_filter]
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No requests placed yet.")