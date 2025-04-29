import pandas as pd
import os
from transformers import pipeline
from app.database import fetch_active_shipments, update_bulk_shipment_decisions

# Load HuggingFace model once
risk_classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english", top_k=None)

async def analyze_and_decide_shipment_risks_async(batch_size: int = 100):
    df = fetch_active_shipments()

    if df.empty:
        yield "No shipments to process."
        return

    total_rows = len(df)
    yield f"Starting agent run... Total rows: {total_rows}"

    risk_scores = []
    shipment_ids = []

    for i in range(0, total_rows, batch_size):
        batch_df = df.iloc[i:i+batch_size]

        batch_texts = batch_df.apply(lambda row: ' '.join(str(x) for x in row.values), axis=1).tolist()

        try:
            results = risk_classifier(batch_texts)

            for shipment, result in zip(batch_df.itertuples(), results):
                if isinstance(result, list):
                    risk_score = result[1]['score'] if len(result) > 1 else result[0]['score']
                else:
                    risk_score = result['score']

                risk_scores.append((shipment.Index, risk_score))  # shipment.Index is row index
                shipment_ids.append(shipment.Index)
        
        except Exception as e:
            for shipment in batch_df.itertuples():
                risk_scores.append((shipment.Index, 0.0))
                shipment_ids.append(shipment.Index)

        yield f"Processed {min(i+batch_size, total_rows)}/{total_rows}"

    # Now update all shipment risk scores in one go
    update_bulk_shipment_decisions(risk_scores)

    yield "✅ Completed all shipments."
