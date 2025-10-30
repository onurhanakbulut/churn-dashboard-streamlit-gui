import streamlit as st


st.set_page_config(page_title="Welcome", page_icon="📊", layout="wide")


st.markdown("""
    <style>
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #4F46E5, #3B82F6);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6em 1.4em;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #3B82F6, #4F46E5);
        transform: scale(1.05);
        box-shadow: 0px 6px 14px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    

st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
    
    
    

# --- sayfa başlığı ---
col_logo, col_button = st.columns([4, 1])
with col_logo:
    st.markdown("<h1 style='text-align:left;'>👋 Welcome to the Customer Churn Demo</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p style='color:gray; font-size:16px; margin-top:-10px;'>
            <b>Version:</b> v1.0 &nbsp; | &nbsp; Developed by <b>Onurhan Akbulut</b> 
        </p>
        """, unsafe_allow_html=True)
with col_button:

    rb1, rb2 = st.columns([1, 2])
    with rb2:
        if st.button("🚀 Go to Dashboard"):
            st.session_state._go_dash = True
            st.rerun()

if st.session_state.get("_go_dash"):
    st.session_state._go_dash = False
    st.switch_page("pages/dashboard_page.py")
    st.stop()


            
st.write("")
col1, col2 = st.columns([2, 1])  

with col1:
    st.markdown(
        """
        ### 📌 About this Demo  

        This Streamlit application presents a **Customer Churn Prediction Dashboard**  
        built using the [Online Retail II dataset (UCI ML Repository)](https://archive.ics.uci.edu/dataset/352/online%2Bretail?utm_source=chatgpt.com).  
        This is a **transactional dataset** containing all online retail transactions  
        made between **01/12/2010 and 09/12/2011** for a **UK-based and registered non-store retailer**.

        The project demonstrates how data-driven insights can help e-commerce businesses  
        identify customers who are likely to churn based on **derived behavioral features**  
        such as **purchase frequency**, **monetary value**, and **customer lifetime patterns**  
        extracted from the original Online Retail II dataset.

        The churn prediction model was developed with **XGBoost**,  
        deployed through a **FastAPI** service, and containerized using **Docker**  
        for scalable and portable integration.

        For this interactive dashboard, a **synthetic dataset** was generated  
        to simulate real-world customer behavior and enable real-time experimentation  
        without exposing sensitive business data.
        """
    )

with col2:
    st.markdown(
        """
        ###  Highlights
        -  **Customer churn probability** estimation per customer  
        -  **Interactive visualizations** for key behavioral metrics  
        -  **Real-time inference** via FastAPI endpoint  
        -  **Containerized deployment** using Docker  
        -  **Modern Streamlit UI** for seamless demo experience  
        """,
    )

st.divider()



col1, col2 = st.columns([1.5, 1.5])

with col1:
    st.image("assets/original_dataset.png", caption="Online Retail II Dataset Preview", width=800)

with col2:
    st.markdown(
            """
            <div style='margin-left:40px'>
                <h4>🧾 Dataset Information</h4>
                The original dataset contains <b>541,910 rows</b> and <b>8 columns</b>,  
                representing real e-commerce transactions.  
                Extensive <b>data preprocessing</b>, <b>feature engineering</b>,  
                and <b>exploratory analysis</b> steps were applied  
                before training the churn prediction model.
            </div>
            """,
            unsafe_allow_html=True
        )

#
st.markdown("### Ready to explore?")

st.markdown("""
    <hr style="margin-top: 50px; margin-bottom: 15px;">
    <div style='text-align: center; color: gray; font-size: 15px;'>
        <p> <b>Customer Churn Dashboard Demo</b> — Version <b>v1.0</b></p>
        <p>Developed by <b>Onurhan Akbulut</b> | 2025</p>
    </div>
    """, unsafe_allow_html=True)

