# 🚀 Deployment Guide - Streamlit Cloud

Complete step-by-step guide to deploy the Student Answer Evaluator to **Streamlit Cloud**.

## 📋 Prerequisites

✅ GitHub account  
✅ Code pushed to GitHub repository  
✅ Google API Key (free)  
✅ Streamlit account (free)

## Step-by-Step Deployment

### 1️⃣ **Prepare Your GitHub Repository**

Ensure your repository contains:
```
Evaluate/
├── streamlit_app.py        (main app file)
├── requirements.txt        (dependencies)
├── README.md              (documentation)
├── .streamlit/
│   └── config.toml        (styling config)
├── .env.example           (template, don't commit .env!)
└── .gitignore            (prevent tracking secrets)
```

**Verify .env is in .gitignore:**
```bash
git status
```
Should NOT show `.env` if correctly ignored.

### 2️⃣ **Push Code to GitHub**

```bash
# Stage all files
git add .

# Commit changes
git commit -m "Add Streamlit app for answer evaluation"

# Push to main branch
git push origin main
```

Verify on GitHub that all files are present: https://github.com/sapnashuklapws/Evaluate

### 3️⃣ **Create Google API Key**

1. Visit: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. A new key will be generated
4. **Copy and save it securely** ⚠️ (Keep it secret!)

### 4️⃣ **Deploy on Streamlit Cloud**

1. Go to: [https://share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"** button
3. Fill in deployment details:
   - **GitHub repo**: `sapnashuklapws/Evaluate`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
4. Click **"Deploy!"**

Streamlit will begin building (takes 1-2 minutes).

### 5️⃣ **Add Secrets to Streamlit Cloud**

1. Once deployed, click the **"☰" menu** (top right)
2. Select **"Settings"**
3. Go to **"Secrets"** tab
4. Add your API key:
   ```
   GOOGLE_API_KEY=your_api_key_here_from_step_3
   ```
5. Click **"Save"**
6. App will automatically restart

### 6️⃣ **Verify Deployment**

1. Your app URL: `https://share.streamlit.io/sapnashuklapws/Evaluate/main/streamlit_app.py`
2. Or shorter: `https://[your-custom-app-name].streamlit.app`
3. Test the app:
   - Upload a question paper PDF
   - Upload an answer sheet PDF
   - Click "Evaluate Answers"
   - Verify results display correctly

### 7️⃣ **Customize App Name** (Optional)

In Streamlit Cloud dashboard:
1. Click your app
2. Go to **"Settings"**
3. Under **"General"**, change the app name
4. URL will update to match

## 📊 File Size Limits

Streamlit Cloud limits:
- Max upload size: **100MB per file**
- Max total app: **1GB**

For larger files, consider:
- Compressing PDFs
- Splitting large answer sheets
- Using Google Cloud Storage

## 🔒 Security Best Practices

✅ **DO:**
- Keep API keys in Streamlit Secrets, never in code
- Use `.env.example` template (without actual values)
- Add `.env` to `.gitignore`
- Regenerate API keys if compromised

❌ **DON'T:**
- Commit `.env` file to GitHub
- Share API keys publicly
- Hardcode secrets in source code

## ⚙️ Environment Variables

### Local Development
Create `.env` file:
```
GOOGLE_API_KEY=your_key_here
```

### Streamlit Cloud
Add via Secrets in Settings:
```
GOOGLE_API_KEY=your_key_here
```

The app automatically reads from both sources.

## 🐛 Troubleshooting

### **App shows "API key not found"**
- ✅ Go to Settings → Secrets
- ✅ Add `GOOGLE_API_KEY=your_key`
- ✅ Click Save
- ✅ Wait for app to restart

### **PDFs not uploading**
- ✅ Check file size < 100MB
- ✅ Verify PDF is not corrupted
- ✅ Try re-exporting the PDF

### **"Could not extract text"**
- ✅ Ensure PDFs have extractable text (not image-only)
- ✅ Try scanning with better resolution
- ✅ Use OCR tools if needed

### **Rate limit exceeded**
- ✅ Switch to `gemini-1.5-flash` (faster model)
- ✅ Wait 60 seconds before retrying
- ✅ Check API quota in Google AI Studio

### **App crashes during evaluation**
- ✅ Check app logs: Click "Manage" → "Logs"
- ✅ Ensure API key is valid
- ✅ Try with smaller PDF files
- ✅ Check Streamlit Cloud status: https://status.streamlit.io

## 📈 Monitoring & Analytics

Streamlit Cloud provides:
- **Logs**: Click "Manage app" → "Logs" to view errors
- **Metrics**: Session duration, user interactions
- **Rerun stats**: Track app performance

## 🔄 Updates & Redeployment

After making code changes:

1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: [describe changes]"
   git push origin main
   ```

2. Streamlit Cloud auto-redeploys within seconds
3. No manual action needed!

To force redeploy:
- Click **"Rerun"** button in app
- Or click **"Restart"** in app menu

## 💰 Costs

**Free Tier** (always free):
- Up to 5 apps
- Community support
- Compute: 100 units/month
- Storage: 1GB

**Pro Tier** (optional, paid):
- More compute units
- Priority support
- Custom domains

> Google's Gemini API also has a free tier! Check [aistudio.google.com](https://aistudio.google.com) for limits.

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Community**: https://discuss.streamlit.io
- **Google Gemini Docs**: https://ai.google.dev/docs
- **GitHub Issues**: https://github.com/sapnashuklapws/Evaluate/issues

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `.env` file is in `.gitignore`
- [ ] `requirements.txt` has all dependencies
- [ ] Google API Key generated
- [ ] App deployed on Streamlit Cloud
- [ ] API Key added to Streamlit Secrets
- [ ] App tested with sample PDFs
- [ ] URL shared with users

---

**🎉 Congratulations! Your app is live and ready to use!**

Share your app URL with students and teachers: `https://share.streamlit.io/sapnashuklapws/Evaluate/main/streamlit_app.py`
