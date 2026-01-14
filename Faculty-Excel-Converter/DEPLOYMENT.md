# Deployment Guide

This guide covers deploying the Faculty Excel Converter application with:
- **Backend (Flask API)** on Render
- **Frontend (React 3D UI)** on Netlify

## Step 1: Deploy Backend to Render

### Option A: Deploy via Render Dashboard (Recommended)

1. **Push your code to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push
   ```

2. **Go to [Render](https://render.com)** and sign in

3. **Click "New +" → "Web Service"**

4. **Connect your GitHub repository**

5. **Configure the service:**
   - **Name**: `faculty-excel-converter-api` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

6. **Add environment variables** (optional):
   - `PYTHON_VERSION`: `3.11.0`
   - `FLASK_ENV`: `production`

7. **Click "Create Web Service"**

8. **Wait for deployment** - Render will build and deploy your app

9. **Copy your API URL** - It will look like: `https://faculty-excel-converter-api.onrender.com`

### Option B: Deploy via render.yaml Blueprint

1. Push code to GitHub
2. In Render dashboard, go to **"Blueprints"**
3. Click **"New Blueprint Instance"**
4. Connect your repository
5. Render will automatically detect `render.yaml` and deploy

### Important Notes for Render:

- **Free tier sleeps after 15 minutes of inactivity** - first request may be slow
- **Uploads folder**: Render's free tier has ephemeral storage. Files in `/uploads` will be deleted on redeploy
- **For production**: Consider upgrading to paid tier or using external storage (AWS S3, Cloudinary, etc.)

## Step 2: Deploy Frontend to Netlify

### Option A: Deploy via Netlify Dashboard (Recommended)

1. **Go to [Netlify](https://app.netlify.com)** and sign in

2. **Click "Add new site" → "Import an existing project"**

3. **Connect your GitHub repository**

4. **Configure build settings** (auto-detected from `netlify.toml`):
   - **Build command**: `cd frontend && npm run build`
   - **Publish directory**: `frontend/build`
   - **Node version**: `20`

5. **Add environment variable**:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: Your Render API URL (e.g., `https://faculty-excel-converter-api.onrender.com`)

6. **Click "Deploy site"**

7. **Wait for build and deployment**

8. **Your site is live!** - URL will be like: `https://your-site-name.netlify.app`

### Option B: Deploy via Netlify CLI

1. **Install Netlify CLI** (if not already):
   ```bash
   npm install -g netlify-cli
   ```

2. **Build the frontend**:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

3. **Deploy**:
   ```bash
   netlify deploy --prod --dir=build
   ```

4. **Follow the prompts**:
   - Log in to Netlify
   - Create new site or link existing
   - Confirm build directory

5. **Set environment variable** in Netlify dashboard:
   - Go to **Site settings → Environment variables**
   - Add `VITE_API_BASE_URL` with your Render API URL

6. **Rebuild** (trigger redeploy to use the new env variable)

## Step 3: Verify Deployment

1. **Visit your Netlify site URL**

2. **Test the features**:
   - Upload faculty data files
   - Analyze changes
   - Update Excel files
   - Create templates

3. **Check browser console** for any errors

4. **Monitor Render logs** for backend errors:
   - Go to Render dashboard → Your service → Logs

## Updating Your Deployment

### Update Backend (Render):
1. Push changes to GitHub
2. Render auto-deploys on git push (if auto-deploy is enabled)
3. Or manually deploy from Render dashboard

### Update Frontend (Netlify):
1. Push changes to GitHub
2. Netlify auto-builds and deploys
3. Or trigger manual deploy from Netlify dashboard

## Environment Variables Reference

### Frontend (Netlify):
- `VITE_API_BASE_URL` - Your Render backend URL (e.g., `https://faculty-excel-converter-api.onrender.com`)

### Backend (Render):
- `PYTHON_VERSION` - `3.11.0` (optional)
- `FLASK_ENV` - `production` (optional)

## Troubleshooting

### Frontend can't connect to backend:
- ✓ Check `VITE_API_BASE_URL` is set correctly in Netlify
- ✓ Rebuild frontend after setting env variable
- ✓ Ensure Render backend is running (not sleeping)
- ✓ Check CORS settings in `app.py`

### Render service keeps sleeping:
- This is normal on free tier
- First request wakes it up (may take 30-60 seconds)
- Consider upgrading to paid tier for always-on service

### File uploads not working:
- ✓ Check file size limits (16MB max)
- ✓ Verify file extensions (.txt, .xlsx, .xls)
- ✓ Check Render logs for errors

### Build fails on Netlify:
- ✓ Check Node version (should be 20)
- ✓ Verify `frontend/package.json` has all dependencies
- ✓ Check build logs for specific errors

## Custom Domain (Optional)

### For Netlify:
1. Go to **Site settings → Domain management**
2. Click **Add custom domain**
3. Follow DNS configuration instructions

### For Render:
1. Go to your service → **Settings**
2. Click **Add Custom Domain**
3. Configure DNS records as instructed

## Security Recommendations

1. **Change Flask secret key** in `app.py`:
   ```python
   app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')
   ```
   Add `SECRET_KEY` as environment variable in Render

2. **Enable HTTPS** (automatic on both Render and Netlify)

3. **Set up CORS properly** for production domains in `app.py`

4. **Monitor logs** for suspicious activity

## Cost Estimate

- **Render Free Tier**: $0/month
  - 750 hours/month
  - Sleeps after 15 min inactivity

- **Netlify Free Tier**: $0/month
  - 100GB bandwidth/month
  - 300 build minutes/month

- **Total**: **$0/month** for hobby/personal use

## Support

If you encounter issues:
1. Check this deployment guide
2. Review Render logs (backend issues)
3. Review Netlify build logs (frontend issues)
4. Check browser console (client-side errors)
