# Deployment Guide - Streamlit Cloud

## Files Ready for Deployment

All necessary files are ready:
- ✓ app.py
- ✓ requirements.txt
- ✓ packages.txt (for FFmpeg)
- ✓ .env.example
- ✓ All Python modules

## Step-by-Step Deployment

### 1. Push to GitHub

If not already done:

```bash
git add .
git commit -m "Ready for deployment"
git push
```

### 2. Deploy on Streamlit Cloud

1. **Go to:** https://share.streamlit.io/

2. **Sign in** with your GitHub account

3. **Click "New app"** button

4. **Configure deployment:**
   - **Repository:** Select your `lecture2notes` repository
   - **Branch:** `main` (or `master`)
   - **Main file path:** `app.py`

5. **Add Secrets (IMPORTANT):**
   - Click **"Advanced settings"**
   - In the **"Secrets"** section, paste:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   ```
   - Replace `your_actual_groq_api_key_here` with your real API key from https://console.groq.com/keys

6. **Click "Deploy"**

7. **Wait 2-3 minutes** for deployment to complete

8. **Your app will be live at:**
   ```
   https://yourusername-lecture2notes-app-xxxxx.streamlit.app
   ```

## Important Notes

### FFmpeg Installation
- `packages.txt` tells Streamlit Cloud to install FFmpeg automatically
- No manual configuration needed

### API Key Security
- Never commit `.env` file to GitHub (it's in .gitignore)
- Always use Streamlit Cloud Secrets for API keys
- Get free API key from: https://console.groq.com/keys

### File Size Limits
- Streamlit Cloud has upload size limits
- Maximum file size: 200MB per file
- For larger files, consider using Render or Railway

## Troubleshooting

### Deployment Fails

**Check:**
1. All files are pushed to GitHub
2. `requirements.txt` is present
3. `packages.txt` is present
4. API key is added in Secrets

### App Crashes

**Check:**
1. Streamlit Cloud logs (click "Manage app" → "Logs")
2. API key is correct in Secrets
3. All dependencies are in `requirements.txt`

### FFmpeg Not Found

**Solution:**
- Ensure `packages.txt` contains `ffmpeg`
- Redeploy the app

## Alternative Deployment Options

### Option 1: Render.com (If Streamlit Cloud doesn't work)

1. Create account on https://render.com/
2. Click "New" → "Web Service"
3. Connect GitHub repository
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Add environment variable: `GROQ_API_KEY`
6. Deploy

### Option 2: Railway.app

1. Create account on https://railway.app/
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add environment variable: `GROQ_API_KEY`
5. Railway auto-detects Streamlit apps
6. Deploy

### Option 3: Hugging Face Spaces

1. Create account on https://huggingface.co/
2. Create "New Space"
3. Select "Streamlit" as SDK
4. Upload all files
5. Add `GROQ_API_KEY` in Settings → Repository secrets
6. Space will auto-deploy

## Free Tier Limitations

### Streamlit Cloud (Free)
- 1 private app
- Unlimited public apps
- 1GB RAM
- Shared CPU

### Render (Free)
- 750 hours/month
- Sleeps after 15 min inactivity
- 512MB RAM

### Railway (Free Trial)
- $5 free credit
- No sleep mode
- Good performance

### Hugging Face (Free)
- Unlimited public spaces
- 2 CPU cores
- 16GB RAM

## Post-Deployment

### Share Your App
Your live URL will be:
```
https://yourapp.streamlit.app
```

### Monitor Usage
- Check Streamlit Cloud dashboard
- Monitor Groq API usage at https://console.groq.com/

### Update App
```bash
git add .
git commit -m "Update app"
git push
```
App auto-updates on Streamlit Cloud!

## Need Help?

- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Forum: https://discuss.streamlit.io/
- GitHub Issues: Open issue on your repository
