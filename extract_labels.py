import os
import csv

DATASET_PATH = "./data"
OUTPUT_CSV = "all_labels.csv"

# Mappings
savee_map = {
    'a': 'angry',
    'd': 'disgust',
    'f': 'fear',
    'h': 'happy',
    'n': 'neutral',
    'sa': 'sad',
    'su': 'surprise'
}

emotion_to_sentiment = {
    'happy': 'satisfied',
    'calm': 'satisfied',
    'neutral': 'neutral',
    'angry': 'unsatisfied',
    'fear': 'unsatisfied',
    'disgust': 'unsatisfied',
    'sad': 'unsatisfied',
    'surprise': 'neutral'
}

ravdess_map = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fear',
    '07': 'disgust',
    '08': 'surprise'
}

crema_map = {
    'SAD': 'sad',
    'ANG': 'angry',
    'DIS': 'disgust',
    'FEA': 'fear',
    'HAP': 'happy',
    'NEU': 'neutral'
}

with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['filepath', 'emotion', 'sentiment'])

    for dataset in ['Savee', 'Ravdess', 'Crema', 'Tess']:
        dataset_path = os.path.join(DATASET_PATH, dataset)

        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if not file.endswith(".wav"):
                    continue

                filepath = os.path.relpath(os.path.join(root, file), DATASET_PATH).replace("\\", "/")
                emotion = "neutral"

                if dataset.lower() == 'savee':
                    base = os.path.splitext(file)[0]
                    parts = base.split('_')
                    if len(parts) != 2:
                        print(f"⚠️ fichier ignoré: {file}")
                        continue
                    code = parts[1]
                    if code.startswith("sa") or code.startswith("su"):
                        prefix = code[:2]
                    else:
                        prefix = code[0]
                    emotion = savee_map.get(prefix, 'neutral')

                elif dataset.lower() == 'ravdess':
                    base = os.path.splitext(file)[0]
                    parts = base.split('-')
                    if len(parts) < 3:
                        print(f"⚠️ fichier ignoré: {file}")
                        continue
                    emotion_id = parts[2]
                    emotion = ravdess_map.get(emotion_id, 'neutral')

                elif dataset.lower() == 'crema':
                    base = os.path.splitext(file)[0]
                    for key in crema_map:
                        if key in base:
                            emotion = crema_map[key]
                            break

                elif dataset.lower() == 'tess':
                    base = os.path.splitext(file)[0]
                    if 'angry' in base.lower():
                        emotion = 'angry'
                    elif 'disgust' in base.lower():
                        emotion = 'disgust'
                    elif 'fear' in base.lower():
                        emotion = 'fear'
                    elif 'happy' in base.lower():
                        emotion = 'happy'
                    elif 'neutral' in base.lower():
                        emotion = 'neutral'
                    elif 'sad' in base.lower():
                        emotion = 'sad'
                    elif 'ps' in base.lower() or 'suprise' in base.lower() or 'surprise' in base.lower():
                        emotion = 'surprise'

                sentiment = emotion_to_sentiment.get(emotion, 'neutral')
                writer.writerow([filepath, emotion, sentiment])

print(f"✅ Fichier généré : {OUTPUT_CSV}")
