import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TN Complete Slang", page_icon="🌶️", layout="wide")

st.title("🌶️ Tamil Nadu COMPLETE Slang Translator")
st.markdown("**ALL 38 Districts | Multiple Slangs Per District | Dual Tamil/English Boxes**")

# Load ALL 38 district slang libraries from CSV files
DISTRICTS = ["Chennai", "Cuddalore", "Dharmapuri", "Kanchipuram", "Kanyakumari", "Karur",
             "Krishnagiri", "Madurai", "Mayiladuthurai", "Nagapattinam", "Namakkal", "Nilgiris",
             "Perambalur", "Pudukottai", "Ramanathapuram", "Ranipet", "Salem", "Sivaganga",
             "Tenkasi", "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli",
             "Tirupattur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Vellore",
             "Viluppuram", "Virudhunagar", "Coimbatore", "Dindigul", "Erode"]

@st.cache_data
def load_district_slang():
    DISTRICT_SLANG = {}
    csv_folder = "slang_data"  # Folder containing CSV files
    
    for district in DISTRICTS:
        csv_file = os.path.join(csv_folder, f"{district.lower()}.csv")
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            slang_dict = {}
            for _, row in df.iterrows():
                slang_dict[row['slang']] = {
                    'tamil': row.get('tamil', ''),
                    'english': row.get('english', ''),
                    'description': row.get('description', '')
                }
            DISTRICT_SLANG[district] = slang_dict
        else:
            DISTRICT_SLANG[district] = {}
    
    return DISTRICT_SLANG

DISTRICT_SLANG = load_district_slang()

# Input Section
col1, col2 = st.columns([3, 1])

with col1:
    st.header("📥 Input ANY Tamil Nadu Slang")
    input_text = st.text_area("Type slang from ANY district:", height=80, value=st.session_state.get("test_input", ""), key="input_area")
    selected_district = st.selectbox("➜ Show Slangs From:", list(DISTRICT_SLANG.keys()))

with col2:
    st.header("🔍 Quick Tests")
    quick_tests = ["machan", "da", "ayya", "tambi", "koothu"]
    if st.button("Clear Input", key="clear_btn"):
        st.session_state.test_input = ""
    for test in quick_tests:
        if st.button(test, key=f"quick_{test}"):
            st.session_state.test_input = test

# Translation Logic
def find_slang_matches(input_text, district_slang):
    matches = []
    input_lower = input_text.lower()
    for slang, translation in district_slang.items():
        if input_lower in slang.lower() or slang.lower() in input_lower:
            matches.append((slang, translation))
    return matches[:10]

# Display slang with full details
def display_slang_details(slang, trans):
    with st.expander(f"**{slang}** - {trans.get('english', 'N/A')}"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Tamil:** {trans.get('tamil', 'N/A')}")
        with col2:
            st.markdown(f"**English:** {trans.get('english', 'N/A')}")
        if trans.get('description') and trans.get('description').strip():
            st.markdown(f"**Description:** {trans.get('description')}")
        else:
            st.info("📝 Description coming soon...")

if st.button("🚀 FIND & DISPLAY", type="primary"):
    if input_text:
        matches = find_slang_matches(input_text, DISTRICT_SLANG[selected_district])
        
        if matches:
            st.success(f"**Found in {selected_district}: {len(matches)} match(es)**")
            st.divider()
            for slang, trans in matches:
                display_slang_details(slang, trans)
        else:
            st.warning(f"No matches found for '{input_text}' in {selected_district}")

# DISTRICT BROWSER
st.header("📍 **Browse All 38 Districts**")
district_cols = st.columns(6)
for i, district in enumerate(list(DISTRICT_SLANG.keys())[:38]):
    with district_cols[i%6]:
        if st.button(district[:12], key=f"browse_{i}"):
            st.session_state.current_district = district
            st.rerun()

# Show selected district slangs
if 'current_district' in st.session_state:
    district = st.session_state.current_district
    st.markdown(f"### 🔥 **{district} Slang Library**")
    
    if DISTRICT_SLANG[district]:
        for i, (slang, trans) in enumerate(list(DISTRICT_SLANG[district].items())[:30]):
            display_slang_details(slang, trans)
    else:
        st.info(f"No slangs loaded for {district}. Please add CSV data.")

st.markdown("---")
st.markdown("*ALL 38 Tamil Nadu Districts | 200+ Slangs Each | Streamlit Cloud Global*")
