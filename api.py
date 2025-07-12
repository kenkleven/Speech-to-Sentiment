from fastapi import FastAPI, UploadFile
from pipeline import transcribe_audio, predict_sentiment
import uvicorn
import tempfile

app = FastAPI()

@app.post("/v1/api/predict")
async def predict(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = transcribe_audio(tmp_path)
    sentiment = predict_sentiment(text)
    return {"transcription": text, "sentiment": sentiment}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
