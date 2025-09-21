# SmartCourt

SmartCourt is a web application that analyzes padel matches using AI. It integrates your Dahua NVR / IP camera setup to capture court video, detect players & ball trajectories, generate analytics, and display them in a user-friendly dashboard. Think of it as a lightweight version of what sites like Spash.com do.

---

## 🛠 Features

- Capture live stream from Dahua NVR via RTSP  
- Player & ball detection + tracking  
- Rally statistics: count, length, shot types  
- Heatmaps of player positioning & ball placement zones  
- Rule-based insight/tip generation (e.g. net play, consistency, serve performance)  
- Web frontend with templates for analysis, technique, tactics, singles, highlights, download

---

## 🚀 Tech Stack

| Component            | Technology                                                   |
|----------------------|---------------------------------------------------------------|
| Backend (AI + API)   | Python, FastAPI                                             |
| Computer Vision / AI | OpenCV, YOLO (via Ultralytics or similar), tracking & filters |
| Frontend             | HTML, JS, CSS (static templates)                             |
| Deployment           | Replit, or any server with Python support & RTSP access       |

---

## 🧾 Repository Structure

SmartCourt/
├── frontend/
│ ├── analysis.html
│ ├── technique.html
│ ├── tactical.html
│ ├── highlights.html
│ ├── singles.html
│ ├── download.html
│ └── static/ ← JS, CSS, images etc.
├── backend/
│ ├── ai_pipeline.py ← detection / tracking / stats logic
│ ├── insights.py ← tip & insight generation
│ └── utils.py ← helpers: heatmap, ball trajectory etc.
├── main.py ← server entrypoint (FastAPI)
├── requirements.txt ← Python dependencies
└── README.md ← this file

yaml
Copy code

---

## ⚙ Setup & Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/SmartCourt254/SmartCourt.git
   cd SmartCourt
Set up Python environment

Use venv or conda:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure camera stream

Get your Dahua NVR RTSP URL.
Example:

bash
Copy code
rtsp://username:password@<NVR_IP>:554/cam/realmonitor?channel=1&subtype=0
Update backend/ai_pipeline.py with this URL or pass it via environment variable (recommended).

Run the server

bash
Copy code
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
View dashboard

Open your browser to http://localhost:8000/

You can also visit other templates:

/analysis.html

/technique.html

/tactics.html

/highlights.html etc.

Fetch stats

API endpoint GET /api/stats returns JSON with latest analytics + tips.

🔧 How it Works (High-Level)
Video Ingestion
The backend pulls frames from your Dahua NVR (RTSP feed) via OpenCV or FFmpeg.

Player & Ball Detection
Use a YOLO model (or fine-tuned version) to detect players and the ball in each frame.

Tracking
Assign consistent IDs to players across frames (tracker like DeepSORT / ByteTrack). Track the ball’s motion using a Kalman Filter or optical flow.

Statistics & Insights
Compute metrics like rally length, court occupancy, shot distribution. Then apply rule-based logic to generate textual tips.

Frontend
Static HTML/JS reads the stats API, draws charts/heatmaps, shows insights & visuals.

🎯 Usage Tips
Use a high-quality video stream (main stream) for better detection accuracy. If bandwidth is a problem, the sub-stream works but with reduced fidelity.

Calibrate your camera / court line detection so court layout is accurate (helps heatmaps & shot placements).

Run on a machine with GPU (if possible) if you want near-real-time performance; otherwise, you might get lag.

Collect sample labeled data for your specific court, lighting, ball colour etc. to improve accuracy.

🧪 Tests & Examples
You can add these as you build them

Sample matches with recorded video to test detection/tracking.

Prebuilt demo stats (JSON) to mock frontend working.

Unit tests for insight rules (e.g., “should recommend net play if net win rate < X”).

🙋 Roadmap
Real-time video playback with overlayed bounding boxes

More advanced event classification: lobs, smashes, defensive plays

Player comparison (compare two players’ styles/metrics)

Mobile UI / responsive design

Exportable reports & video highlights clipping

📄 License & Attribution
You may want to add license here if you have one.

👏 Contributing
Pull requests are welcome! Suggestions/corrections for detection models, UI/UX, insights are especially appreciated.

If you fix a bug, add a feature, or improve model accuracy, please document what changed.

📬 Contact
For questions, suggestions, or partnerships:

GitHub issues in this repo

Or email: smartcourt33@gmail.com
