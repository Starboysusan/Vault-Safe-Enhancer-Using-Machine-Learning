

---


📦 Vault Safe Enhancer Using Machine Learning

Real-time security surveillance system using **YOLOv8** and **Streamlit**.  
Detects unauthorized human activity in restricted areas, captures evidence, and sends email alerts with images. Designed to enhance vault or secure area safety using AI.

---

 🛠 Features

- **Live camera streaming** from IP cameras with start/stop functionality  
- **Human detection** using YOLOv8 with bounding boxes  
- **Automatic email alerts** with captured images as evidence  
- **Alarm sound** for instant notification  
- **Evidence gallery** with images displayed in a neat grid and download option  
- **Simple and clean UI** with location tag  

---
 💻 Tech Stack

- **Python 3.10+**  
- **Streamlit** – Interactive web app UI  
- **Ultralytics YOLOv8** – Object detection  
- **OpenCV** – Video capture & image processing  
- **Pygame** – Alarm sound playback  
- **SMTP / Gmail** – Email notifications  
- **Python-dotenv** – Manage sensitive credentials securely  

---

 ⚙️ Installation & Setup

1. **Clone the repository**  

```bash
git clone https://github.com/<your-username>/vault-safe-enhancer.git
cd vault-safe-enhancer
````

2. **Create virtual environment**

```bash
python -m venv venv
```

3. **Activate virtual environment**

* **Windows**:

```bash
venv\Scripts\activate
```

* **Mac/Linux**:

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Create `.env` file** in the project root:

```env
SENDER_EMAIL=yourgmail@gmail.com
RECEIVER_EMAIL=receiver@gmail.com
EMAIL_PASSWORD=your16digitapppassword
```

> ⚠️ Never push `.env` to GitHub. Keep credentials secure.

---

## 🚀 How to Run

```bash
streamlit run app.py
```

* Open the Streamlit app in your browser
* Enter your **IP camera URL**
* Click **Start Streaming** to begin surveillance
* Click **Stop Streaming** to pause
* Captured evidence appears in the **Evidence Tab**

---

## 📸 Evidence Gallery

* Shows captured images in a **grid layout**
* Each image has a **Download button** for records
* Images are timestamped automatically

---

## 🔔 Alerts

* Sends an **email with captured image** when human activity is detected
* Plays an **alarm sound** instantly
* Cooldown period ensures emails are not sent repeatedly

---

## 📂 Folder Structure

```
VaultSafeEnhancer/
├─ app.py                 # Main Streamlit app
├─ venv/                  # Python virtual environment (ignored in git)
├─ evidence_images/       # Captured images (ignored in git)
├─ .env                   # Environment variables (ignored in git)
├─ requirements.txt       # Python dependencies
└─ README.md              # Project documentation
```

---

## 🌟 Future Enhancements

* Multiple camera support
* Real-time dashboard with analytics
* Integration with SMS alerts
* Advanced AI models for specific object detection

---

## 👤 Author

**Sudharsan K** – AI & Python Enthusiast
Contact: [iamsudharsan43@gmail.com](mailto:imasudharsan43@gmail.com)

