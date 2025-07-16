# AgriMind 🌿

**AgriMind** is an AI-powered mental health assistant built specifically for farmers and agricultural workers. It leverages sentiment analysis to detect emotional states from user input and offers empathetic, AI-generated responses. This tool helps address stress, anxiety, and depression common in rural communities, contributing to UN SDG 3 (Good Health & Well-being) and SDG 2 (Zero Hunger).

The app is deployed and it is live on streamlit cloud: https://final-project-agrimind-project-jscg2qikwlc6qutqptsyar.streamlit.app/

The pitchdeck link: https://gamma.app/docs/AgriMind-AI-Powered-Mental-Health-Assistant-for-Farmers-xh2qq99fm8gt130

## 🚀 Features

- 🌾 Farmer-focused mental health assistant
- 🤖 AI-powered mood detection using NLP
- 💬 Voice-enabled chatbot feedback
- 📈 Admin dashboard with mood analytics and charts
- 🗃️ Mood history logs and CSV download for users/admin
- 🔐 Supabase-authenticated admin access
- 🎨 Streamlit UI with a clean green-agriculture design


## 🧠 How It Works

1. **User Input:** A farmer types how they feel.
2. **AI Model:** A pre-trained sentiment model classifies it as positive, neutral, or negative.
3. **Response Engine:** Provides supportive feedback and speaks the message aloud.
4. **Logging:** Data is saved to Supabase for future analysis.
5. **Admin Panel:** Allows for registration/login and access to mood statistics with visualizations.


## 🛠️ Tech Stack

| Layer          | Technology               |
|----------------|---------------------------|
| Frontend       | Streamlit (Python UI)     |
| Backend        | Python, Scikit-learn      |
| ML Model       | Tfidf + Logistic Regression |
| Authentication | Supabase Auth             |
| Database       | Supabase Postgres         |
| Hosting        | Local / Streamlit Cloud   |



## 📂 Project Structure

AgriMind/
├── streamlit_app.py              # Main app interface
├── model/
│   └── sentiment_model.pkl       # Trained ML model
├── utils/
│   ├── predict.py                # Mood prediction logic
│   └── supabase_client.py        # Supabase DB/Auth interface
├── .env                          # Supabase credentials (not shared)
└── README.md
`

## 🔐 Admin Usage

- Admins can register/login via the sidebar using Supabase Auth
- After login, they can:
  - View mood logs
  - Analyze mood trends
  - Download entire records in CSV format



## ✅ Setup Instructions

1. **Clone the Repo**

```bash
git clone https://github.com/your-username/agrimind.git
cd agrimind
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Add Supabase Credentials**

Create a `.env` file in the root:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

4. **Run the App**

```bash
streamlit run streamlit_app.py
```


## 🧪 Example Model Training (Optional)

To retrain the sentiment model:

```bash
python utils/train_model.py
```


## 📊 Admin Dashboard Charts

- **Bar chart**: Total count of each mood type
- **Line chart**: Daily mood trends over time


## 🧾 License

This project is for educational purposes under the PLP Academy and is open for non-commercial use. All rights reserved © Jefther Afuyo 2025.


## 👨🏽‍💻 Developed by

**Jefther Simeon Afuyo**  
Email: afuyojefther@gmail.com

Built with ❤️ to support farmers' mental health.
