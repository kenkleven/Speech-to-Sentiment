import os
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, pipeline
import pandas as pd
from tqdm import tqdm

emotion_to_sentiment = {
    'happy': 'satisfied',
    'calm': 'satisfied',
    'neutral': 'neutral',
    'angry': 'unsatisfied',
    'fear': 'unsatisfied',
    'fearful': 'unsatisfied',  
    'disgust': 'unsatisfied',
    'sad': 'unsatisfied',
    'surprise': 'neutral',
    'surprised': 'neutral'
}

# 📄 init modèles HF
print("🔷 Loading Wav2Vec2...")
asr_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
asr_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

print("🔷 Loading sentiment analysis model...")
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


def transcribe_audio(audio_path, sr=16000):
    audio, _ = librosa.load(audio_path, sr=sr)
    input_values = asr_processor(audio, sampling_rate=sr, return_tensors="pt").input_values
    with torch.no_grad():
        logits = asr_model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = asr_processor.decode(predicted_ids[0])
    return transcription.lower()


def predict_sentiment(text):
    result = sentiment_pipeline(text)[0]
    label = result['label']
    if label == 'POSITIVE':
        return 'satisfied'
    elif label == 'NEGATIVE':
        return 'unsatisfied'
    else:
        return 'neutral'


def evaluate_dataset(dataset_csv, audio_base_dir):
    df = pd.read_csv(dataset_csv)
    y_true = []
    y_pred = []
    transcriptions = []

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        relative_path = row['filepath']
        file_path = os.path.join(audio_base_dir, relative_path)
        emotion = row['emotion']
        true_sentiment = emotion_to_sentiment.get(emotion, 'neutral')
        try:
            text = transcribe_audio(file_path)
            pred_sentiment = predict_sentiment(text)
        except Exception as e:
            print(f"⚠️ Error with {file_path}: {e}")
            pred_sentiment = 'neutral'
            text = ""

        y_true.append(true_sentiment)
        y_pred.append(pred_sentiment)
        transcriptions.append(text)

    df['transcription'] = transcriptions
    df['true_sentiment'] = y_true
    df['pred_sentiment'] = y_pred
    df.to_csv("evaluation_results.csv", index=False)
    print("✅ Evaluation results saved to evaluation_results.csv")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_csv", type=str, help="CSV file with file paths & emotions", default="all_labels.csv")
    parser.add_argument("--audio_base_dir", type=str, help="Base directory containing Savee, Ravdess, Crema, Tess", default="data/")
    parser.add_argument("--single_wav", type=str, help="Single wav file for inference", default=None)

    args = parser.parse_args()

    if args.single_wav:
        text = transcribe_audio(args.single_wav)
        sentiment = predict_sentiment(text)
        print(f"\n🔷 Transcription:\n{text}")
        print(f"🔷 Predicted sentiment: {sentiment}")
    else:
        evaluate_dataset(args.dataset_csv, args.audio_base_dir)
