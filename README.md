```
  ███████╗███╗   ███╗ ██████╗ ████████╗██╗ ██████╗ ███╗   ██╗
  ██╔════╝████╗ ████║██╔═══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
  █████╗  ██╔████╔██║██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║
  ██╔══╝  ██║╚██╔╝██║██║   ██║   ██║   ██║██║   ██║██║╚██╗██║
  ███████╗██║ ╚═╝ ██║╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚████║
  ╚══════╝╚═╝     ╚═╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
  ██████╗ ███████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗██╗████████╗██╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔════╝ ████╗  ██║██║╚══██╔══╝██║██╔═══██╗████╗  ██║
  ██████╔╝█████╗  ██║     ██║   ██║██║  ███╗██╔██╗ ██║██║   ██║   ██║██║   ██║██╔██╗ ██║
  ██╔══██╗██╔══╝  ██║     ██║   ██║██║   ██║██║╚██╗██║██║   ██║   ██║██║   ██║██║╚██╗██║
  ██║  ██║███████╗╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║██║   ██║   ██║╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
  ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
  ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
  ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
  ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
  ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
  ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
```

# 😊 Emotion Recognition System with Bangla Voice Response

### *Real-Time Facial Emotion Detection — Powered by DeepFace + Microsoft Neural TTS*

> **একটি বুদ্ধিমান emotion detection system যা ব্যবহারকারীর মুখের অভিব্যক্তি বিশ্লেষণ করে**
> **এবং সেই অনুযায়ী বাংলায় কথা বলে সাড়া দেয়।**
> DeepFace দিয়ে real-time emotion detect করে, Microsoft Nabanita Neural Voice দিয়ে
> ব্যক্তিগতকৃত Bangla response তৈরি করে — সম্পূর্ণ offline-capable desktop application।

[![Made by](https://img.shields.io/badge/Made%20by-MD%20Naimur%20Hamim-d4af37?style=flat-square)](https://github.com/naimurhamim)
[![Year](https://img.shields.io/badge/Year-2026-d4af37?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#license)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue?style=flat-square)](#)
[![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)](#)
[![Voice](https://img.shields.io/badge/Voice-Nabanita%20Neural-d4af37?style=flat-square)](#)

---

## 🎬 Demo Screenshots

| Neutral Detection | Fear Detection |
|---|---|
| ![Neutral](Screenshots/neutral.png) | ![Fear](Screenshots/fear.png) |

| Angry Detection | Happy Detection |
|---|---|
| ![Angry](Screenshots/angry.png) | ![Happy](Screenshots/happy.png) |

> System টি real-time এ মুখের অভিব্যক্তি detect করে, emotion score দেখায় এবং Bangla voice এ response দেয়।

---

## 📌 Project Overview

Emotion Recognition System একটি AI-powered desktop application যা মানুষের মুখের ছবি বিশ্লেষণ করে তার মানসিক অবস্থা বোঝার চেষ্টা করে এবং সেই অনুযায়ী বাংলা ভাষায় সাড়া দেয়।

মানুষ যখন দুঃখী থাকে, রাগান্বিত থাকে বা হতাশ থাকে — তখন একটি সহানুভূতিশীল সাড়া তার মনে ইতিবাচক প্রভাব ফেলতে পারে। এই system টি সেই ধারণাকে বাস্তবে রূপ দেওয়ার একটি প্রচেষ্টা।

**মূল লক্ষ্য:**
- Webcam থেকে real-time এ মুখের অভিব্যক্তি detect করা
- Detected emotion অনুযায়ী ব্যক্তিগতকৃত Bangla response তৈরি করা
- Microsoft Nabanita Neural Voice দিয়ে সেই response শোনানো
- সম্পূর্ণ desktop GUI application হিসেবে চালানো

---

## ✨ Features

| Feature | বিবরণ |
|---|---|
| 😊 **Real-Time Emotion Detection** | Webcam থেকে একাধিক frame capture করে emotion analyze করা |
| 🎯 **8 Emotion Support** | Happy, Sad, Depressed, Angry, Surprised, Fear, Disgust, Neutral |
| 🗣️ **Bangla Neural Voice** | Microsoft bn-BD-NabanitaNeural দিয়ে natural Bangla speech |
| 📊 **Emotion Score Bars** | প্রতিটি emotion এর confidence score visual bar এ দেখানো |
| 👤 **Personalized Response** | ব্যবহারকারীর নাম নিয়ে ব্যক্তিগতকৃত সাড়া |
| 🖥️ **Desktop GUI** | PyQt6 দিয়ে তৈরি Gold/Silver/Black themed desktop app |
| ⚡ **Multi-Frame Analysis** | একাধিক frame এর dominant emotion নির্ধারণ করে accuracy বাড়ানো |
| 🔄 **Replay Voice** | যেকোনো সময় voice response আবার শোনার সুবিধা |
| 🚀 **Single Command Launch** | একটি command এ backend + GUI একসাথে চালু হয় |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Emotion Detection | DeepFace (FER model) |
| Backend API | FastAPI + Uvicorn |
| Desktop GUI | PyQt6 |
| Voice Synthesis | Microsoft Edge TTS (bn-BD-NabanitaNeural) |
| Camera Processing | OpenCV 4.x |
| ML Framework | TensorFlow / Keras |
| Language | Python 3.10 |
| Communication | REST API (localhost) |

---

## 🧠 How It Works

```
Webcam → Frame Capture (3–10 frames)
        ↓
DeepFace Emotion Analysis → প্রতিটি frame এ emotion detect
        ↓
Dominant Emotion নির্ধারণ → সব frame এর most common emotion
        ↓
Response Generation → Emotion + User Name দিয়ে Bangla text তৈরি
        ↓
Edge TTS (Nabanita Neural) → Bangla text থেকে voice generate
        ↓
GUI তে Result দেখানো → Emotion, Score Bars, Response Text, Audio Player
```

---

## 📊 Emotion → Response Mapping

| Emotion | Response ধরন |
|---|---|
| 😊 Happy | উৎসাহমূলক কথা, আনন্দ বাড়ানো |
| 😢 Sad | সহানুভূতি + হালকা রসিকতা |
| 😔 Depressed | অনুপ্রেরণামূলক কথা |
| 😠 Angry | শান্ত করার কথা |
| 😲 Surprised | কৌতূহলী প্রতিক্রিয়া |
| 😨 Fear | আশ্বস্ত করার কথা |
| 🤢 Disgust | ইতিবাচক দৃষ্টিভঙ্গি |
| 😐 Neutral | বন্ধুত্বপূর্ণ কথোপকথন |

---

## 📁 Project Structure

```
emotion-recognition/
│
├── run_gui.py              # Single entry point — backend + GUI একসাথে চালু করে
├── run.py                  # শুধু backend চালানোর জন্য
├── README.md
│
├── 📁 backend/
│   ├── main.py             # FastAPI server — REST API endpoints
│   ├── emotion_engine.py   # DeepFace দিয়ে emotion detection logic
│   ├── voice_engine.py     # Edge TTS — Nabanita Neural voice generation
│   ├── response_map.py     # Emotion → Bangla response mapping
│   ├── requirements.txt    # Python dependencies
│   └── 📁 audio/           # Generated voice files (auto-created)
│
├── 📁 gui/
│   └── app.py              # PyQt6 desktop GUI — সম্পূর্ণ UI
│
├── 📁 dataset/
│   ├── 📁 train/           # Training images (angry/happy/sad/...)
│   └── 📁 test/            # Test images
│
├── 📁 Screenshots/         # Demo screenshots
│
└── 📁 .venv/               # Python 3.10 virtual environment
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10**
- Webcam
- Internet connection (Edge TTS এর জন্য)

### 1. Repository Clone করো

```bash
git clone https://github.com/naimurhamim/emotion-recognition-system.git
cd emotion-recognition-system
```

### 2. Virtual Environment তৈরি করো

```bash
py -3.10 -m venv .venv

# Windows
.venv\Scripts\activate
```

### 3. Dependencies Install করো

```bash
pip install -r backend/requirements.txt
```

### 4. App চালাও

```bash
python run_gui.py
```

> প্রথমবার চালালে DeepFace automatically তার model download করবে (~100MB) — এটা একবারই হবে।

---

## ⚙️ API Endpoints

Backend FastAPI server `http://127.0.0.1:8000` এ চলে।

| Method | Endpoint | বিবরণ |
|---|---|---|
| GET | `/` | API status check |
| GET | `/health` | Health check |
| POST | `/analyze` | Frames analyze করে emotion + voice return করে |
| GET | `/emotions` | Supported emotions এর list |

### `/analyze` Request Body

```json
{
  "frames": ["base64_image_1", "base64_image_2"],
  "user_name": "নাইমুর"
}
```

### `/analyze` Response

```json
{
  "dominant_emotion": "happy",
  "avg_scores": { "happy": 92.5, "neutral": 5.2, "sad": 2.3 },
  "frame_count": 5,
  "response_text": "নাইমুর, তোমার হাসিটা কত সুন্দর তুমি কি জানো?",
  "audio_url": "/static/audio/abc123.mp3"
}
```

---

## 🔬 Methodology

### Emotion Detection Pipeline

DeepFace library ব্যবহার করে pre-trained FER (Facial Expression Recognition) model দিয়ে emotion detect করা হয়। প্রতিটি frame এ 7টি base emotion এর probability score বের করা হয় এবং সব frame এর dominant emotion এর majority vote নেওয়া হয়।

### Multi-Frame Strategy

Single frame এ noise বা partial occlusion এর কারণে ভুল detection হতে পারে। তাই 3–10টি frame capture করে সব frame এর dominant emotion এর মধ্যে সবচেয়ে বেশিবার আসা emotion কে final result হিসেবে নেওয়া হয়।

### Voice Response System

Microsoft Edge TTS এর `bn-BD-NabanitaNeural` voice ব্যবহার করা হয়েছে — এটি Bangladeshi Bangla এর জন্য Microsoft এর neural voice যা free এবং natural শোনায়। Response text গুলো pure Bangla Unicode তে লেখা যাতে TTS সঠিকভাবে pronounce করতে পারে।

---

## 📈 Future Plans

- [ ] **Custom Dataset Training** — নিজস্ব dataset দিয়ে model fine-tune করা
- [ ] **Offline Voice** — Internet ছাড়া local TTS model integrate করা
- [ ] **Emotion History** — Session এর emotion timeline track করা
- [ ] **Multi-Face Detection** — একসাথে একাধিক মুখের emotion detect করা
- [ ] **Mobile App** — Android/iOS version তৈরি করা
- [ ] **Mental Health Integration** — দীর্ঘমেয়াদী emotion pattern বিশ্লেষণ
- [ ] **Custom Voice Training** — নিজস্ব Bangla voice model train করা
- [ ] **Emotion-Based Music** — Detected emotion অনুযায়ী background music play করা
- [ ] **Report Generation** — Daily/weekly emotion report তৈরি করা

---

## 📦 requirements.txt

```txt
fastapi==0.111.0
uvicorn==0.29.0
python-multipart==0.0.9
opencv-python==4.9.0.80
deepface==0.0.93
tf-keras==2.16.0
numpy==1.26.4
Pillow==10.3.0
edge-tts==7.2.8
PyQt6==6.7.0
```

---

## 🤝 Contributing

1. Fork করো
2. Feature branch তৈরি করো: `git checkout -b feature/NewFeature`
3. Commit করো: `git commit -m 'Add NewFeature'`
4. Push করো: `git push origin feature/NewFeature`
5. Pull Request খোলো

---

## 📄 License

**MIT License** — বিস্তারিত [LICENSE](LICENSE) দেখো।

---

## 👨‍💻 Author

**MD Naimur Hamim**

Department of IoT and Robotics Engineering
University of Frontier Technology, Gazipur-1750, Bangladesh

[![GitHub](https://img.shields.io/badge/GitHub-naimurhamim-181717?style=for-the-badge&logo=github)](https://github.com/naimurhamim)

---

*Built with ❤️ for Mental Health Awareness & Human-Computer Interaction Research*

⭐ **If you found this project helpful, please give it a star!** ⭐
