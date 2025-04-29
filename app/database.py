import sqlite3
import os
import pandas as pd

DB_DIR = "./data"
DB_PATH = os.path.join(DB_DIR, "shipments.db")

def connect_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    return conn

def load_temp_shipments_from_uploaded_csv(df):
    conn = connect_db()
    
    # Always ensure risk_score and reroute_suggestion columns exist
    if "risk_score" not in df.columns:
        df["risk_score"] = 0.0
    if "reroute_suggestion" not in df.columns:
        df["reroute_suggestion"] = ""

    # Store the uploaded dataframe into temp_shipments table
    df.to_sql('temp_shipments', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

def fetch_active_shipments():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM temp_shipments", conn)
    conn.close()
    return df

def update_shipment_decision(shipment_id_value, risk_score, reroute_suggestion):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch the dynamic unique ID column
    df_meta = pd.read_sql_query("SELECT __unique_id_col__ FROM temp_shipments LIMIT 1", conn)
    if df_meta.empty:
        conn.close()
        return

    unique_id_col = df_meta["__unique_id_col__"].iloc[0]

    # Dynamic single update
    cursor.execute(
        f"""UPDATE temp_shipments 
            SET risk_score = ?, reroute_suggestion = ? 
            WHERE "{unique_id_col}" = ?""",
        (risk_score, reroute_suggestion, shipment_id_value)
    )

    conn.commit()
    conn.close()

def update_bulk_shipment_decisions(risk_scores_list):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch the dynamic unique ID column
    df_meta = pd.read_sql_query("SELECT __unique_id_col__ FROM temp_shipments LIMIT 1", conn)
    if df_meta.empty:
        conn.close()
        return

    unique_id_col = df_meta["__unique_id_col__"].iloc[0]

    # Now bulk update based on the real unique ID
    for shipment_id_value, risk_score in risk_scores_list:
        cursor.execute(
            f"""UPDATE temp_shipments 
                SET risk_score = ? 
                WHERE "{unique_id_col}" = ?""",
            (risk_score, shipment_id_value)
        )

    conn.commit()
    conn.close()
