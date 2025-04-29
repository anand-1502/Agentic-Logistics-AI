import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time
import base64

# --- Page config ---
st.set_page_config(page_title="Agentic AI Dashboard", layout="centered", page_icon="🚛")

# --- Set blurred background ---
def set_background(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        body {{
            background: url("data:image/jpg;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
        }}
        .stApp {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 3rem 2rem;
            border-radius: 20px;
            max-width: 800px;
            margin: 5rem auto;
            box-shadow: 0px 10px 40px rgba(0,0,0,0.25);
        }}
        </style>
    """, unsafe_allow_html=True)

# Set background
set_background("bg.jpg")

# --- Main content ---
st.title("🚛 Agentic AI - Supply Chain Risk Intelligence")
st.header("📤 Upload Your Shipment Data")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state["uploaded_df"] = df
    columns = df.columns.tolist()

    st.success(f"✅ Uploaded: {uploaded_file.name} successfully!")

    st.subheader("🛠️ Select Columns for Risk Focus")
    suggested_cols = [col for col in columns if any(word in col.lower() for word in ["time", "rating", "delay", "status", "care", "problem"])]
    selected_cols = st.multiselect("Focus Columns for AI Analysis:", options=columns, default=suggested_cols)

    st.subheader("🆔 Choose Unique ID Column")
    unique_id_col = st.selectbox("Which column uniquely identifies a shipment?", options=columns)

    if st.button("🚀 Upload & Register Dataset"):
        with st.spinner("Uploading..."):
            uploaded_file.seek(0)
            try:
                response = requests.post(
                    "http://localhost:8000/upload_dataset/",
                    files={"file": uploaded_file},
                    data={
                        "selected_columns": ",".join(selected_cols),
                        "unique_id_col": unique_id_col
                    }
                )
                if response.status_code == 200:
                    st.success("✅ Dataset Registered Successfully!")
                else:
                    st.error(f"❌ Upload Failed: {response.text}")
            except Exception as e:
                st.error(f"❌ Upload Failed due to network error: {e}")

st.header("🧠 Run Risk Scorer")

if st.button("🔎 Analyze Risks"):
    if "uploaded_df" in st.session_state:
        total_rows = len(st.session_state["uploaded_df"])
        batch_size = 100
        est_time_sec = int((total_rows / batch_size) * 5)
        est_min, est_sec = divmod(est_time_sec, 60)

        st.info(f"⏳ Estimated Completion Time: {est_min} min {est_sec} sec")

        progress_bar = st.progress(0)
        status_text = st.empty()

        with st.spinner("Agent is analyzing risks..."):
            try:
                response = requests.post("http://localhost:8000/run_agent/")
                if response.status_code == 200:
                    for i in range(100):
                        time.sleep(est_time_sec / 100)
                        progress_bar.progress(i + 1)
                        status_text.text(f"🚚 Progress: {i+1}% completed")
                    st.success("✅ Risk Scoring Completed!")
                else:
                    st.error(f"❌ Failed to start Agent: {response.text}")
            except Exception as e:
                st.error(f"❌ Agent request failed: {e}")

st.header("📦 View Risk-Scored Shipments")

if st.button("📄 View Results"):
    try:
        response = requests.get("http://localhost:8000/get_shipments/")
        if response.status_code == 200:
            shipments = response.json().get("shipments", [])
            if shipments:
                df_result = pd.DataFrame(shipments)

                if "risk_score" in df_result.columns:
                    cols = ["risk_score"] + [col for col in df_result.columns if col != "risk_score"]
                    df_result = df_result[cols]

                st.dataframe(df_result, use_container_width=True)

                if "risk_score" in df_result.columns:
                    bins = [0, 0.2, 0.5, 0.8, 1.0]
                    labels = ['Low', 'Medium', 'High', 'Critical']
                    df_result["risk_category"] = pd.cut(df_result["risk_score"], bins=bins, labels=labels)

                    pie_fig = px.pie(df_result, names="risk_category", title="📊 Risk Distribution - Pie Chart")
                    bar_fig = px.bar(
                        df_result["risk_category"].value_counts().reset_index(),
                        x="risk_category",
                        y="count",
                        labels={"risk_category": "Risk Category", "count": "Shipments"},
                        title="📊 Risk Distribution - Bar Chart"
                    )
                    st.plotly_chart(pie_fig, use_container_width=True)
                    st.plotly_chart(bar_fig, use_container_width=True)

                csv = df_result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "⬇️ Download Risk-Scored CSV",
                    csv,
                    "risk_scored_shipments.csv",
                    "text/csv"
                )
            else:
                st.warning("🟡 No shipment data found yet.")
        else:
            st.error(f"❌ Failed to fetch data: {response.text}")
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
