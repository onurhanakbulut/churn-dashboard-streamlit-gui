import streamlit as st
import pandas as pd
import os
import requests, math
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Customer Dashboard", page_icon="📊", layout="wide")
st.title("Customers")
if st.button(" ↩️ Back to Home Screen"):
    st.switch_page("login.py")


#  Sidebar'ı tamamen gizle
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

st.markdown("""
    <style>
        /* Navbar tasarımı */
        .navbar {
            background: linear-gradient(90deg, #4F46E5, #3B82F6); /* mavi-mor gradient */
            padding: 18px 30px;
            border-radius: 10px;
            color: white;
            font-size: 26px;
            font-weight: 600;
            text-align: center;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
            margin-bottom: 35px;
            letter-spacing: 0.5px;
        }

        /*  Sayfa arka planı — daha modern ve profesyonel görünüm */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #1a1c2b, #111826, #0b0e14);
            color: white;
        }

        /*  Sidebar (varsa) */
        [data-testid="stSidebar"] {
            background: #111827;
            color: white;
        }

        /*  Başlık yazıları */
        h1, h2, h3 {
            color: #f8fafc;
        }

        /*  Başarı mesajı (yeşil kutular) */
        .stAlert {
            background-color: #1e3a8a !important;
            color: white !important;
        }

        /*  DataFrame görünümü: açık tablo teması */
        [data-testid="stDataFrame"] table {
            background-color: #f8fafc !important; /* açık gri */
            color: #1e293b !important;            /* koyu yazı */
            border-radius: 10px;
        }

        /*  Satır hover efekti */
        [data-testid="stDataFrame"] tr:hover {
            background-color: #e2e8f0 !important;
        }

        /*  Sütun başlıkları */
        [data-testid="stDataFrame"] thead {
            background-color: #CBD5E1 !important;
            color: #0f172a !important;
        }
    </style>

    <div class="navbar">
         Customer Churn Dashboard
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <p style='color:gray; font-size:16px; margin-top:-10px;'>
        <b>Version:</b> v1.0 &nbsp; | &nbsp; Developed by <b>Onurhan Akbulut-İlayda Sümer</b> 
    </p>
    """, unsafe_allow_html=True)


API_BASE = "https://churn-model-api.onrender.com"
CSV_PATH = os.path.join("data", "synthetic_data.csv")


@st.cache_data
def load_data(path):
    df = pd.read_csv(path, encoding="utf-8", sep=None, engine="python")
    
    return df




def predict_batch(df_in: pd.DataFrame, batch_size: int = 1000):
    out = []
    with requests.Session() as s:
        for start in range(0, len(df_in), batch_size):
            chunk = df_in.iloc[start:start+batch_size]
            payload = {"data": [
                {"Frequency": float(r["Frequency"]),
                 "Monetary": float(r["Monetary"]),
                 "CustomerLifetimeDays": float(r["CustomerLifetimeDays"])}
                for _, r in chunk.iterrows()
            ]}
            r = s.post(f"{API_BASE}/predict-batch", json=payload, timeout=60)
            r.raise_for_status()
            out.extend(r.json())
    return out





if os.path.exists(CSV_PATH):
    df = load_data(CSV_PATH)
    df['Churn Probability'] = None
    df['Status'] = None
    st.success(f"Customer table ready | Number of Customers: {len(df):,}")
    #table_placeholder = st.empty()
    #table_placeholder.dataframe(df, use_container_width=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        table_placeholder = st.empty()
        table_placeholder.dataframe(df, use_container_width=True)
    
    with col2:
        st.markdown("### Key Metrics")
        
        
        
        def risky_stats(df_):
            s = pd.to_numeric(df_["Status"], errors="coerce")
            risky = int((s == 1).sum())

            
            probs = (
                df_["Churn Probability"]
                .replace("%", "", regex=True)
                .astype(float)
                .dropna()
            )
            avg_prob = probs.mean() if len(probs) > 0 else 0.0

            return risky, avg_prob
        
        def revenue_impact(df_):
            # Status ve Monetary sayısallaştır
            s = pd.to_numeric(df_["Status"], errors="coerce")
            m = pd.to_numeric(df_["Monetary"], errors="coerce")
        
            
            pr_raw = df_["Churn Probability"]
            pr = pd.to_numeric(pr_raw.replace("%", "", regex=True), errors="coerce")
            if pr.max(skipna=True) is not None and pr.max(skipna=True) > 1.0:
                pr = pr / 100.0
        
            # Geçerli kayıtlar
            valid = s.notna() & m.notna() & pr.notna()
            s, m, pr = s[valid], m[valid], pr[valid]
        
            risky_loss = (m[s == 1] * pr[s == 1]).sum()
            low_retained = (m[s == 0] * (1 - pr[s == 0])).sum()
        
            return float(risky_loss or 0.0), float(low_retained or 0.0)
        
        # Placeholder'lar
        risky_ph = st.empty()          # riskli müşteri sayısı 
        avgprob_ph = st.empty()        # ortalama churn 
        loss_ph = st.empty()           # risky cohorts impact
        retained_ph = st.empty()       # low-risk retained impact
        
        
        
        try:
            r_init, p_init = risky_stats(df)
        except NameError:
            s0 = pd.to_numeric(df["Status"], errors="coerce")
            r_init = int((s0 == 1).sum())
            # Ortalama churn prob:
            pr0 = pd.to_numeric(df["Churn Probability"].replace("%", "", regex=True), errors="coerce")
            if pr0.max(skipna=True) is not None and pr0.max(skipna=True) > 1.0:
                p_init = float(pr0.mean() or 0.0)
            else:
                p_init = float((pr0.mean() or 0.0) * 100.0)
        
        risky_ph.metric("Risky Customers", f"{r_init:,}")
        avgprob_ph.metric("Average Churn Rate", f"%{p_init:.1f}")
        
        loss0, ret0 = revenue_impact(df)
        loss_ph.metric("Impacted Revenue From Risky Cohorts", f"£{loss0:,.0f}")
        retained_ph.metric("Impacted Revenue From Low Churn Risk Customers", f"£{ret0:,.0f}")

        
        
        

    
    

    
    if st.button("Predict Churn"):
        BATCH_SIZE = 300
        REFRESH_EVERY = 10
        total = len(df)
        done = 0
        
        


        prog = st.progress(0)
        with requests.Session() as s:
            for start in range(0, total, BATCH_SIZE):
                chunk = df.iloc[start:start+BATCH_SIZE]

                payload = {"data": [
                    {
                        "Frequency": float(r["Frequency"]),
                        "Monetary": float(r["Monetary"]),
                        "CustomerLifetimeDays": float(r["CustomerLifetimeDays"])
                    }
                    for _, r in chunk.iterrows()
                ]}

                try:
                    resp = s.post(f"{API_BASE}/predict-batch", json=payload, timeout=60)
                    resp.raise_for_status()
                    results = resp.json()
                except Exception:

                    results = [None] * len(chunk)


                for j, r in enumerate(results):
                    idx = chunk.index[j]
                    if r is not None:
                        p = r["churn_probability"]
                        df.at[idx, "Churn Probability"] = f"%{p*100:.1f}"
                        df.at[idx, "Status"] = 1 if r["is_churn"] else 0
                    else:
                        df.at[idx, "Churn Probability"] = None
                        df.at[idx, "Status"] = None

                    done += 1
                    if (done % REFRESH_EVERY == 0) or (done == total):
                        prog.progress(done / total)
                        table_placeholder.dataframe(df, use_container_width=True)
                        r_now, p_now = risky_stats(df)
                        risky_ph.metric("Risky Customers", f"{r_now:,}")
                        avgprob_ph.metric("Average Churn Rate", f"%{p_now:.1f}")
                        # Metrikleri canlı güncelle
                        try:
                            r_now, p_now = risky_stats(df)
                        except NameError:
                            s_now = pd.to_numeric(df["Status"], errors="coerce")
                            r_now = int((s_now == 1).sum())
                            pr_now = pd.to_numeric(df["Churn Probability"].replace("%", "", regex=True), errors="coerce")
                            if pr_now.max(skipna=True) is not None and pr_now.max(skipna=True) > 1.0:
                                p_now = float(pr_now.mean() or 0.0)
                            else:
                                p_now = float((pr_now.mean() or 0.0) * 100.0)
                        
                        risky_ph.metric("Risky Customers", f"{r_now:,}")
                        avgprob_ph.metric("Average Churn Rate", f"%{p_now:.1f}")
                        
                        loss_now, ret_now = revenue_impact(df)
                        loss_ph.metric("Impacted Revenue From Risky Cohorts", f"£{loss_now:,.0f}")
                        retained_ph.metric("Impacted Revenue From Low Churn Risk Customers", f"£{ret_now:,.0f}")

       
                        
       
        r_fin, p_fin = risky_stats(df)
        risky_ph.metric("Risky Customers", f"{r_fin:,}")
        avgprob_ph.metric("Average Churn Rate", f"%{p_fin:.1f}")
        # Final metrik güncellemesi
        try:
            r_fin, p_fin = risky_stats(df)
        except NameError:
            s_fin = pd.to_numeric(df["Status"], errors="coerce")
            r_fin = int((s_fin == 1).sum())
            pr_fin = pd.to_numeric(df["Churn Probability"].replace("%", "", regex=True), errors="coerce")
            if pr_fin.max(skipna=True) is not None and pr_fin.max(skipna=True) > 1.0:
                p_fin = float(pr_fin.mean() or 0.0)
            else:
                p_fin = float((pr_fin.mean() or 0.0) * 100.0)
        
        risky_ph.metric("Risky Customers", f"{r_fin:,}")
        avgprob_ph.metric("Average Churn Rate", f"%{p_fin:.1f}")
        
        loss_fin, ret_fin = revenue_impact(df)
        loss_ph.metric("Impacted Revenue From Risky Cohorts", f"£{loss_fin:,.0f}")
        retained_ph.metric("Impacted Revenue From Low Churn Risk Customers", f"£{ret_fin:,.0f}")

        # ──────────────────────────────────────────────
        #  Görsel Analiz Alanı 
        # ──────────────────────────────────────────────
        st.divider()
        st.markdown("##  Churn Analytics Dashboard")
        
        
        col1, col2, col3, col4 = st.columns(4)
        
        
        with col1:
            st.markdown("### Churn vs Not Churn")
            s = pd.to_numeric(df.get("Status"), errors="coerce").dropna()
            s = s[s.isin([0, 1])]
            if len(s) > 0:
                churn_count = (s == 1).sum()
                not_churn_count = (s == 0).sum()
                fig1, ax1 = plt.subplots()
                ax1.pie(
                    [churn_count, not_churn_count],
                    labels=["Churn", "Not Churn"],
                    autopct="%1.1f%%",
                    startangle=90
                )
                ax1.axis("equal")
                st.pyplot(fig1, use_container_width=True)
            else:
                st.info("Veri bulunamadı")
        
        
        with col2:
            st.markdown("### Churn Risk by Monetary")
        
            mon = pd.to_numeric(df["Monetary"], errors="coerce")
            prob = pd.to_numeric(df["Churn Probability"].replace("%", "", regex=True), errors="coerce")
            if prob.max(skipna=True) > 1:
                prob = prob / 100.0
        
            valid = mon.notna() & prob.notna()
            data = pd.DataFrame({"Monetary": mon[valid], "ChurnProb": prob[valid]})
        
            if len(data) == 0:
                st.info("Veri bulunamadı")
            else:
                unique_vals = data["Monetary"].nunique()
                if unique_vals < 2:
                    st.info("Monetary değişkeninde segment yapılacak kadar farklı değer yok.")
                else:
                    
                    q = min(12, unique_vals)
        
                    
                    _, bin_edges = pd.qcut(
                        data["Monetary"],
                        q=q,
                        retbins=True,
                        duplicates="drop",
                        labels=None
                    )
        
                    n_bins = len(bin_edges) - 1
                    if n_bins < 2:
                        st.info("Monetary için anlamlı segment üretilemedi.")
                    else:
                        
                        def fmt_currency(x):
                            return f"£{x:,.0f}".replace(",", ".")
        
                        labels = [
                            f"{fmt_currency(bin_edges[i])}–{fmt_currency(bin_edges[i+1])}"
                            for i in range(n_bins)
                        ]
        
                        
                        data["Segment"] = pd.cut(
                            data["Monetary"],
                            bins=bin_edges,
                            labels=labels,
                            include_lowest=True
                        )
        
                        
                        segment_stats = (
                            data.groupby("Segment", observed=True)["ChurnProb"]
                            .mean()
                            .reset_index()
                        )
        
                        fig2, ax2 = plt.subplots(figsize=(7, 4))
                        sns.barplot(data=segment_stats, x="Segment", y="ChurnProb", ax=ax2, color="#3B82F6")
                        ax2.set_ylabel("Average Churn Probability")
                        ax2.set_xlabel("Spending Range")
                        ax2.set_ylim(0, 1)
                        plt.xticks(rotation=45, ha="right")
        
                        for i, v in enumerate(segment_stats["ChurnProb"]):
                            ax2.text(i, min(v + 0.03, 0.98), f"%{v*100:.1f}", ha="center", fontweight="bold")
        
                        st.pyplot(fig2, use_container_width=True)


        
       
        with col3:
            st.markdown("### Churn Risk by Frequency")
        
            freq = pd.to_numeric(df["Frequency"], errors="coerce")
            prob = pd.to_numeric(df["Churn Probability"].replace("%", "", regex=True), errors="coerce")
            if prob.max(skipna=True) > 1:
                prob = prob / 100.0
        
            valid = freq.notna() & prob.notna()
            data = pd.DataFrame({"Frequency": freq[valid], "ChurnProb": prob[valid]})
        
            if len(data) == 0:
                st.info("Veri bulunamadı")
            else:
                unique_vals = data["Frequency"].nunique()
                if unique_vals < 2:
                    st.info("Frequency değişkeninde segment yapılacak kadar farklı değer yok.")
                else:
                    
                    q = min(12, unique_vals)
        
                    
                    _, bin_edges = pd.qcut(
                        data["Frequency"],
                        q=q,
                        retbins=True,
                        duplicates="drop",
                        labels=None
                    )
        
                    n_bins = len(bin_edges) - 1
                    if n_bins < 2:
                        st.info("Frequency için anlamlı segment üretilemedi.")
                    else:
                        
                        labels = [
                            f"{int(bin_edges[i])}-{int(bin_edges[i+1])}"
                            for i in range(n_bins)
                        ]
        
                        
                        data["Segment"] = pd.cut(
                            data["Frequency"],
                            bins=bin_edges,
                            labels=labels,
                            include_lowest=True
                        )
        
                        
                        segment_stats = (
                            data.groupby("Segment", observed=True)["ChurnProb"]
                            .mean()
                            .reset_index()
                        )
        
                        fig3, ax3 = plt.subplots(figsize=(6, 4))
                        sns.barplot(data=segment_stats, x="Segment", y="ChurnProb", ax=ax3, color="#7B61FF")
                        ax3.set_ylabel("Average Churn Probability")
                        ax3.set_xlabel("Frequency Range")
                        ax3.set_ylim(0, 1)
                        plt.xticks(rotation=45, ha="right")
                        for i, v in enumerate(segment_stats["ChurnProb"]):
                            ax3.text(i, min(v + 0.03, 0.98), f"%{v*100:.1f}", ha="center", fontweight="bold")
                        st.pyplot(fig3, use_container_width=True)



        
        
        with col4:
            st.markdown("### Churn Risk by Customer Lifetime (Days)")
        
            life = pd.to_numeric(df["CustomerLifetimeDays"], errors="coerce")
            prob = pd.to_numeric(df["Churn Probability"].replace("%", "", regex=True), errors="coerce")
            if prob.max(skipna=True) > 1:
                prob = prob / 100.0
        
            valid = life.notna() & prob.notna()
            data = pd.DataFrame({"Lifetime": life[valid], "ChurnProb": prob[valid]})
        
            if len(data) == 0:
                st.info("Veri bulunamadı")
            else:
                unique_vals = data["Lifetime"].nunique()
                if unique_vals < 2:
                    st.info("Lifetime değişkeninde segment yapılacak kadar farklı değer yok.")
                else:
                    
                    q = min(8, unique_vals)
        
                    
                    _, bin_edges = pd.qcut(
                        data["Lifetime"],
                        q=q,
                        retbins=True,
                        duplicates="drop",
                        labels=None
                    )
        
                    n_bins = len(bin_edges) - 1
                    if n_bins < 2:
                        st.info("Lifetime için anlamlı segment üretilemedi.")
                    else:
                        
                        labels = [
                            f"{int(bin_edges[i])}-{int(bin_edges[i+1])}"
                            for i in range(n_bins)
                        ]
        
                        # Lifetime'ı segmentle
                        data["Segment"] = pd.cut(
                            data["Lifetime"],
                            bins=bin_edges,
                            labels=labels,
                            include_lowest=True
                        )
        
                        
                        segment_stats = (
                            data.groupby("Segment", observed=True)["ChurnProb"]
                            .mean()
                            .reset_index()
                        )
        
                        fig4, ax4 = plt.subplots(figsize=(7, 4))
                        sns.barplot(data=segment_stats, x="Segment", y="ChurnProb", ax=ax4, color="#10B981")
                        ax4.set_ylabel("Average Churn Probability")
                        ax4.set_xlabel("Customer Lifetime (Days) Range")
                        ax4.set_ylim(0, 1)
                        plt.xticks(rotation=45, ha="right")
        
                        
                        for i, v in enumerate(segment_stats["ChurnProb"]):
                            ax4.text(i, min(v + 0.03, 0.98), f"%{v*100:.1f}", ha="center", fontweight="bold")
        
                        st.pyplot(fig4, use_container_width=True)

        




        
else:
    st.error(f"{CSV_PATH} bulunamadı")
    
    
st.markdown("""
    <hr style="margin-top: 50px; margin-bottom: 15px;">
    <div style='text-align: center; color: gray; font-size: 15px;'>
        <p> <b>Customer Churn Demo</b> — Version <b>v1.0</b></p>
        <p>Developed by <b>Onurhan Akbulut-İlayda Sümer</b> | 2025</p>
    </div>
    """, unsafe_allow_html=True)






