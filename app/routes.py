from fastapi import APIRouter, UploadFile, File, Form
import pandas as pd
import io
from fastapi.responses import StreamingResponse, JSONResponse
from app.database import load_temp_shipments_from_uploaded_csv, fetch_active_shipments
from app.agent import analyze_and_decide_shipment_risks_async

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "✅ Server healthy"}

@router.post("/upload_dataset/")
async def upload_dataset(
    file: UploadFile = File(...),
    selected_columns: str = Form(...),
    unique_id_col: str = Form(...)
):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    df = df.fillna("Unknown")

    selected_cols = selected_columns.split(",") if selected_columns else []
    df["__selected_columns__"] = "|".join(selected_cols)
    df["__unique_id_col__"] = unique_id_col

    load_temp_shipments_from_uploaded_csv(df)
    return {"message": "✅ Dataset uploaded and ready!"}

@router.get("/get_shipments/")
async def get_shipments():
    df = fetch_active_shipments()
    return {"shipments": df.to_dict(orient="records")}

@router.post("/run_agent/")
async def run_agent():
    async def event_stream():
        async for status in analyze_and_decide_shipment_risks_async():
            yield (status + "\n")
    return StreamingResponse(event_stream(), media_type="text/event-stream")
