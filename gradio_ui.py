import gradio as gr
from pipeline import transcribe_audio, predict_sentiment

def pipeline_fn(audio):
    text = transcribe_audio(audio)
    sentiment = predict_sentiment(text)
    return text, sentiment

iface = gr.Interface(
    fn=pipeline_fn,
    inputs=gr.Audio(type="filepath", label="Upload your audio"),
    outputs=[
        gr.Textbox(label="Transcription"),
        gr.Textbox(label="Predicted Sentiment")
    ],
    title="Speech-to-Sentiment",
    description="Upload a WAV audio file. The system transcribes it and predicts the sentiment."
)

if __name__ == "__main__":
    iface.launch(share=True)
