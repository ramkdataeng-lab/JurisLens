# 🚀 Deployment Guide: Elastic JurisLens

This guide explains how to deploy the **JurisLens** application for the Elastic Hackathon submission.

## Option 1: ZERO-HASSLE Deployment (Streamlit Community Cloud) 🏆
This is the recommended method. It gives you a live URL (`https://your-app.streamlit.app`) to share with judges.

1.  **Push to GitHub**:
    *   Initialize a git repository in this folder (`c:\Projects\AA\Hackathon\Elasticsearch\JurisLens`).
    *   Push it to a new public GitHub repository named `jurislens`.

2.  **Deploy on Streamlit Cloud**:
    *   Go to [share.streamlit.io](https://share.streamlit.io/).
    *   Sign in with GitHub.
    *   Click **"New app"**.
    *   Select your `jurislens` repository.
    *   **Main file path:** `app.py`.
    *   Click **"Deploy!"**.

3.  **Configure Secrets (CRITICAL)**:
    *   Once deployed, the app will fail because it doesn't have your API keys.
    *   Go to your app's **Settings** -> **Secrets**.
    *   Paste the contents of your `.env` file here in TOML format:
        ```toml
        OPENAI_API_KEY = "sk-..."
        ELASTIC_CLOUD_ID = "..."
        ELASTIC_API_KEY = "..."
        ```
    *   Save. The app will restart automatically and work!

---

## Option 2: Local Demo (Video Recording) 🎥
If you prefer not to deploy publicly, you can record a demo video running it locally.

1.  **Run Locally**:
    ```powershell
    cd c:\Projects\AA\Hackathon\Elasticsearch\JurisLens
    streamlit run app.py
    ```

2.  **Record**:
    *   Use Loom, OBS, or QuickTime.
    *   Show the following flow:
        1.  Upload a PDF (Use a sample policy document).
        2.  Click "Process & Index".
        3.  Ask a question: *"Does this policy cover third-party vendors?"*.
        4.  Show the Agent thinking and citing the source.
        5.  Ask a risk calculation: *"What is the risk of a $50k transfer to France?"*.
        6.  Show the Risk Tool result.

3.  **Upload**:
    *   Upload the video to YouTube (Unlisted) or Loom.
    *   Submit the link on Devpost.

---

## 📦 Project Structure for Submission

Ensure your repo looks like this:
```
JurisLens/
├── app.py             # Main Application Logic
├── ingest.py          # PDF Indexing Script
├── requirements.txt   # Dependencies
├── README.md          # Documentation
├── tools/             # Custom Agent Tools
│   ├── regulation_search.py
│   └── risk_calc.py
└── .env.example       # Example Config (Don't commit real .env!)
```
