# 📊 Customer Churn Prediction Demo (Streamlit)

**Version:** v1.0  
**Developed by:** Onurhan Akbulut  
**https://churn-dashboard-demo.streamlit.app**

---

## 🚀 Overview

This Streamlit web application demonstrates an interactive **Customer Churn Prediction Dashboard**,  
built using the [Online Retail II dataset (UCI Machine Learning Repository)](https://archive.ics.uci.edu/dataset/352/online%2Bretail).

This is a **transactional dataset** containing all online retail transactions made between  
**01/12/2010 and 09/12/2011** for a **UK-based and registered non-store retailer**.

The project illustrates how **data-driven insights** can help e-commerce businesses identify customers  
who are likely to churn based on **derived behavioral features** such as:

- Purchase frequency  
- Monetary value  
- Customer lifetime duration  

The churn prediction model was developed with **XGBoost**, deployed via a **FastAPI** service,  
and containerized with **Docker** for scalable and portable integration.

For this interactive dashboard, a **synthetic dataset** was generated to simulate real-world customer behavior  
and enable real-time experimentation without exposing any sensitive business data.

---

## 🧩 Tech Stack

- **Frontend / UI:** Streamlit  
- **Backend API:** FastAPI  
- **ML Model:** XGBoost  
- **Visualization:** Matplotlib & Seaborn  
- **Containerization:** Docker  

---

## ⚙️ Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/<your-username>/churn-demo.git
cd churn-demo
pip install -r requirements.txt
▶️ Run the App
Start the Streamlit app locally:

bash
Kodu kopyala
streamlit run streamlit_app.py
The dashboard will open automatically in your default browser
(at http://localhost:8501 by default).

🌐 Deployment (Streamlit Cloud)
Push your repository to GitHub.

Go to Streamlit Cloud.

Click “New app” → select your repo and streamlit_app.py as the entry file.

Add the following secret variable in the “Secrets” section:


API_BASE="https://churn-model-api.onrender.com"
Deploy and enjoy your live interactive dashboard!

📁 Project Structure

churn-demo/
├─ login.py            # Home page
├─ pages/
│  └─ dashboard_page.py           # Main dashboard
├─ assets/
│  └─ original_dataset.png     # Dataset preview image
├─ data/
│  └─ synthetic_data.csv     # Synthetic sample data
├─ requirements.txt
├─ README.md

📦 Requirements

streamlit==1.38.0
pandas==2.2.2
requests==2.32.3
matplotlib==3.9.0
seaborn==0.13.2

🏁 Notes
The dataset used here is synthetic for demo purposes.

All API endpoints and model files are hosted separately.

This project was created for educational and portfolio demonstration purposes.

⭐ If you like this project, give it a star on GitHub!

