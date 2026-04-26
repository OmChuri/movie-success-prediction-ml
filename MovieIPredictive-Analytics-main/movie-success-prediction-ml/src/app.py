import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from scipy.stats import ttest_ind, chi2_contingency
import ast

# --- Page Config ---
st.set_page_config(page_title="🎬 Movie Analytics", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Premium Look ---
st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #0E1117;
            color: #FAFAFA;
        }

        /* Top-level Headers */
        h1, h2, h3 {
            font-weight: 700;
            background: -webkit-linear-gradient(#f39c12, #e74c3c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #1a1c23;
            border-right: 1px solid #2d303a;
        }

        /* Metric Cards */
        [data-testid="metric-container"] {
            background-color: #1a1c23;
            border: 1px solid #2d303a;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            transition: transform 0.2s ease;
        }
        [data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            border-color: #f39c12;
        }
        
        /* Buttons */
        .stButton>button {
            border-radius: 8px;
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            font-weight: 600;
            border: none;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #c0392b, #a5281b);
            box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4);
            color: white;
        }

        /* Expanders and Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 15px;
            border-bottom: 2px solid #2d303a;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            background: transparent;
            color: #bdc3c7;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            border-bottom: 2px solid #f39c12 !important;
            color: #f39c12 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Caching Functions ---
@st.cache_data
def load_data(file_path_or_buffer):
    try:
        df = pd.read_csv(file_path_or_buffer)
    except Exception as e:
        return None, [str(e)]

    req_cols = ["budget", "revenue", "popularity", "runtime", "vote_average", "title", "genres"]
    missing_cols = [c for c in req_cols if c not in df.columns]
    
    if missing_cols:
        return None, missing_cols
        
    df = df[req_cols].copy()
    df = df[df["budget"] > 0]
    df = df[df["revenue"] > 0]
    df.dropna(inplace=True)
    df["success"] = (df["revenue"] > df["budget"]).astype(int)
    
    # Safely parse genres
    def parse_genre(x):
        try:
            if isinstance(x, str) and x != '[]':
                parsed = ast.literal_eval(x)
                if isinstance(parsed, list) and len(parsed) > 0 and 'name' in parsed[0]:
                    return parsed[0]['name']
            return "Unknown"
        except (ValueError, SyntaxError):
            return "Unknown"

    df["main_genre"] = df["genres"].apply(parse_genre)
    return df, None

@st.cache_resource
def train_model(filtered_df):
    features = filtered_df[["budget", "popularity", "runtime", "vote_average"]]
    target = filtered_df["success"]
    
    if len(filtered_df) < 20: # Lowered threshold slightly for smaller datasets to avoid issues
        return None, None, None, None, None, None
        
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = model.score(X_test, y_test)
    conf_matrix = confusion_matrix(y_test, y_pred)
    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    
    # Feature Importance
    importances = model.feature_importances_
    
    return model, accuracy, conf_matrix, report_dict, X_test.columns, importances

# --- Sidebar ---
with st.sidebar.container():
    st.image("https://cdn-icons-png.flaticon.com/512/2809/2809590.png", width=60)
    st.title("Movie")
    st.markdown("Predictive Analytics on Film Success")

st.sidebar.divider()

st.sidebar.header("📁 Data Source Selection")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

dataset_options = {
    "🌍 Indian Cinema (All)": os.path.join(DATA_DIR, "dataset_indian_all.csv"),
    "🎬 Bollywood (Hindi)": os.path.join(DATA_DIR, "bollywood.csv"),
    "💥 Tollywood (Telugu)": os.path.join(DATA_DIR, "tollywood.csv"),
    "🔥 Kollywood (Tamil)": os.path.join(DATA_DIR, "dataset_kollywood.csv"),
    "🌐 Global Data (movies.csv)": os.path.join(DATA_DIR, "hollywood.csv"),
    "📤 Upload Custom CSV": "custom"
}

selected_dataset_name = st.sidebar.selectbox("Select Regional Dataset", list(dataset_options.keys()))

df = None
if dataset_options[selected_dataset_name] == "custom":
    uploaded_file = st.sidebar.file_uploader("Upload custom CSV", type=["csv"])
    if uploaded_file:
        df, err = load_data(uploaded_file)
        if err:
            st.sidebar.error(f"Error loading data: {err}")
        else:
            st.sidebar.success("Custom data loaded!")
else:
    file_path = dataset_options[selected_dataset_name]
    if os.path.exists(file_path):
        df, err = load_data(file_path)
        if err:
            st.sidebar.error(f"Data error: {err}")
    else:
        st.sidebar.error(f"Dataset file '{file_path}' not found. Please generate it first.")

if df is not None:
    # --- Filter Options ---
    st.sidebar.header("🔍 Filter Options")
    all_genres = sorted(df["main_genre"].unique())
    selected_genres = st.sidebar.multiselect("Select Genre(s)", options=all_genres, default=all_genres)
    min_votes = st.sidebar.slider("Minimum Vote Average", 0.0, 10.0, 0.0)

    filtered_df = df[(df["main_genre"].isin(selected_genres)) & (df["vote_average"] >= min_votes)]
    
    # --- Main App Content ---
    st.markdown("<h1>Movie Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"**Currently analyzing:** `{selected_dataset_name}`")

    if filtered_df.empty:
        st.warning("⚠️ No data matches your current filters. Please adjust them in the sidebar.")
    else:
        # --- Top-Level KPIs ---
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🎞️ Total Movies", len(filtered_df))
        c2.metric("✅ Success %", f"{filtered_df['success'].mean()*100:.1f}%")
        c3.metric("🎭 Unique Genres", filtered_df['main_genre'].nunique())
        c4.metric("💵 Avg Revenue (₹)", f"{filtered_df['revenue'].mean()/1e7:,.1f} Cr")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Layout Tabs ---
        tab1, tab2, tab3 = st.tabs(["📊 Executive Overview", "🔬 Deep Analytics", "🤖 AI Prediction Engine"])

        # ---------------------------
        # TAB 1: Executive Overview
        # ---------------------------
        with tab1:
            st.subheader("Financial Performance Landscape")
            filtered_df["Success_Label"] = filtered_df["success"].map({1: "Successful", 0: "Unsuccessful"})
            
            fig1 = px.scatter(
                filtered_df, 
                x="budget", 
                y="revenue", 
                color="Success_Label",
                hover_data=["title", "main_genre"],
                labels={"budget": "Budget (INR)", "revenue": "Revenue (INR)"},
                color_discrete_map={"Successful": "#2ecc71", "Unsuccessful": "#e74c3c"},
                opacity=0.8,
                template="plotly_dark"
            )
            fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
            
            with st.expander("📂 View Raw Dataset (Top 50 rows)"):
                st.dataframe(filtered_df.head(50), use_container_width=True)

        # ---------------------------
        # TAB 2: Deep Analytics
        # ---------------------------
        with tab2:
            st.subheader("Feature Correlation Matrix")
            num_cols = ["budget", "revenue", "popularity", "runtime", "vote_average", "success"]
            corr_matrix = filtered_df[num_cols].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="Viridis",
                template="plotly_dark"
            )
            fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_corr, use_container_width=True)

            st.divider()

            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Descriptive Statistics")
                st.dataframe(filtered_df[["budget", "revenue", "popularity", "runtime", "vote_average"]].describe().T, use_container_width=True)

            with col_b:
                st.subheader("Average Metrics by Success")
                avg_metrics = filtered_df.groupby("Success_Label")[["budget", "revenue", "popularity", "runtime", "vote_average"]].mean().reset_index()
                avg_metrics_melt = pd.melt(avg_metrics, id_vars="Success_Label", var_name="Metric", value_name="Average Value")

                fig2 = px.bar(
                    avg_metrics_melt, 
                    x="Metric", 
                    y="Average Value", 
                    color="Success_Label", 
                    barmode="group",
                    color_discrete_map={"Successful": "#2ecc71", "Unsuccessful": "#e74c3c"},
                    template="plotly_dark"
                )
                fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)

        # ---------------------------
        # TAB 3: AI Prediction Engine
        # ---------------------------
        with tab3:
            st.subheader("Random Forest Prediction Model")
            
            model, accuracy, conf_matrix, report_dict, feature_cols, importances = train_model(filtered_df)

            if model is None:
                st.warning("⚠️ Insufficient data to train a reliable model. Please select a larger dataset or relax filters.")
            else:
                col_m1, col_m2, col_m3 = st.columns([1, 1, 1.5])
                with col_m1:
                    st.metric("Model Accuracy", f"{accuracy:.2%}")
                    st.markdown("##### Classification Report")
                    report_df = pd.DataFrame(report_dict).transpose()
                    st.dataframe(report_df.style.format("{:.2f}"))

                with col_m2:
                    st.markdown("##### Confusion Matrix")
                    fig3 = px.imshow(
                        conf_matrix,
                        labels=dict(x="Predicted", y="Actual", color="Count"),
                        x=["Unsuccessful", "Successful"],
                        y=["Unsuccessful", "Successful"],
                        text_auto=True,
                        color_continuous_scale="Blues",
                        template="plotly_dark"
                    )
                    fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=30))
                    st.plotly_chart(fig3, use_container_width=True)
                    
                with col_m3:
                    st.markdown("##### Feature Importance")
                    importance_df = pd.DataFrame({"Feature": feature_cols, "Importance": importances}).sort_values(by="Importance", ascending=True)
                    fig_imp = px.bar(
                        importance_df, 
                        x="Importance", 
                        y="Feature", 
                        orientation='h',
                        color="Importance",
                        color_continuous_scale="Oranges",
                        template="plotly_dark"
                    )
                    fig_imp.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=30))
                    st.plotly_chart(fig_imp, use_container_width=True)

                st.divider()

                # --- Prediction Form ---
                st.markdown("### 🎬 Predict Custom Movie Success")
                st.markdown("Enter hypothetical movie parameters below to see if the AI predicts it will be a blockbuster.")
                
                with st.form("prediction_form"):
                    col_f1, col_f2 = st.columns(2)
                    with col_f1:
                        input_budget = st.number_input("Production Budget (INR)", min_value=1000000, max_value=5000000000, value=50000000, step=5000000)
                        input_runtime = st.slider("Runtime (minutes)", 60, 240, 150)
                    with col_f2:
                        input_popularity = st.slider("Marketing Popularity Score", 0.0, 200.0, 50.0)
                        input_vote_average = st.slider("Expected IMDB Rating", 1.0, 10.0, 7.5)

                    submit = st.form_submit_button("Launch AI Prediction Engine", use_container_width=True)

                if submit:
                    input_data = pd.DataFrame({
                        "budget": [input_budget],
                        "popularity": [input_popularity],
                        "runtime": [input_runtime],
                        "vote_average": [input_vote_average]
                    })

                    prediction = model.predict(input_data)[0]
                    prediction_proba = model.predict_proba(input_data)[0][prediction]

                    # Gauge Chart
                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = prediction_proba * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "AI Confidence Score (%)", 'font': {'color': 'white'}},
                        number = {'font': {'color': 'white'}},
                        gauge = {
                            'axis': {'range': [0, 100], 'tickcolor': 'white'},
                            'bar': {'color': "white"},
                            'steps': [
                                {'range': [0, 50], 'color': "#c0392b"},
                                {'range': [50, 100], 'color': "#27ae60"}
                            ],
                        }
                    ))
                    fig_gauge.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    
                    col_res1, col_res2 = st.columns([1, 2])
                    with col_res1:
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        if prediction == 1:
                            st.success(f"### 🌟 BLOCKBUSTER!\nThe AI predicts this film will be highly profitable and successful at the box office.")
                        else:
                            st.error(f"### 🚨 FLOP WARNING!\nThe AI predicts this film is likely to lose money and fail at the box office.")
                    with col_res2:
                        st.plotly_chart(fig_gauge, use_container_width=True)

else:
    st.info("👆 Please select a valid dataset from the sidebar to begin analytics.")