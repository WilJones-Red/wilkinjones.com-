# Resume Scorer - Render Deployment Guide

## Files Ready for Deployment ✅

Your project now has all the files needed for Render deployment:

- ✅ `app_flask.py` - Flask web application
- ✅ `resume_scorer.py` - Core scoring logic
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `.gitignore` - Git ignore rules

## Next Steps - What YOU Need to Do on Render

### 1. Push Your Code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Resume Scorer app"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/resume-scorer.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render

1. **Go to [render.com](https://render.com)** and sign in/sign up
2. **Click "New +"** → Select **"Web Service"**
3. **Connect your GitHub repository**:
   - Click "Connect account" to link GitHub
   - Find and select your `resume-scorer` repository
4. **Configure the service**:
   - **Name**: `resume-scorer` (or your preferred name)
   - **Region**: Choose closest to your location
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `gunicorn app_flask:app`
   - **Plan**: Select **Free**
5. **Click "Create Web Service"**

### 3. Wait for Deployment

- First deployment takes 5-10 minutes
- You'll see build logs in real-time
- Watch for the spaCy model download (~50MB)
- Once deployed, you'll get a URL like: `https://resume-scorer-XXXX.onrender.com`

### 4. Test Your Live App

Visit your Render URL and test:
- ✅ Page loads correctly
- ✅ Can paste job description
- ✅ Can upload resume file
- ✅ Scoring works and displays results

### 5. Add to Your Portfolio Website

Once deployed, integrate with your portfolio:

**Option A - Embed as iframe:**
```html
<iframe src="https://your-app.onrender.com" 
        width="100%" 
        height="800px" 
        style="border: none; border-radius: 10px;">
</iframe>
```

**Option B - Direct link:**
```html
<a href="https://your-app.onrender.com" 
   target="_blank" 
   class="project-link">
    Try My Resume Scorer
</a>
```

## Important Notes

⚠️ **Free Tier Limitations:**
- App sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month limit (sufficient for portfolio use)

💡 **Tips:**
- Test the app after deployment to ensure models loaded correctly
- The app URL is shareable and can be added to your resume/LinkedIn
- Monitor usage in Render dashboard

## Local Testing

Your Flask app is currently running locally at:
- http://localhost:8080

Test it before deploying to ensure everything works!

## Troubleshooting

If deployment fails:
1. Check build logs in Render dashboard
2. Verify all files are pushed to GitHub
3. Ensure `requirements.txt` has all dependencies
4. Check that Python version is compatible (3.8+)

---

**Ready to deploy? Follow the steps above and let me know if you need help!** 🚀
