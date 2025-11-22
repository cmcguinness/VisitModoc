# Deploying Visit Modoc to Railway

This guide will walk you through deploying the Visit Modoc County website to Railway.

## Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)
- This code pushed to a GitHub repository

## Files Created for Deployment

The following files have been created to enable Railway deployment:

1. **requirements.txt** - Python dependencies (Flask, Gunicorn)
2. **Procfile** - Tells Railway how to start the app
3. **runtime.txt** - Specifies Python version (3.11.7)
4. **.gitignore** - Prevents committing unnecessary files
5. **app.py** - Updated with production configuration

## Step-by-Step Deployment

### 1. Push Code to GitHub

If you haven't already:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Visit Modoc County website"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/visit-modoc.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Railway

1. **Go to Railway:** https://railway.app
2. **Sign in** with your GitHub account
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your Visit Modoc repository**
6. **Railway will automatically:**
   - Detect it's a Python app
   - Install dependencies from requirements.txt
   - Use the Procfile to start the app with Gunicorn
   - Assign a public URL

### 3. Configure Environment Variables (Optional)

If you want to add Google Analytics or other secrets:

1. Go to your project in Railway
2. Click on your service
3. Go to "Variables" tab
4. Add environment variables:
   - `GA_MEASUREMENT_ID` - Your Google Analytics tracking ID
   - Any other secrets you need

### 4. Custom Domain (Optional)

Railway provides a free `.railway.app` domain, but you can add a custom domain:

1. In Railway, go to your service
2. Click "Settings" tab
3. Scroll to "Domains"
4. Click "Generate Domain" for a Railway subdomain
5. Or click "Custom Domain" to add your own (e.g., visit-modoc.com)

**For visit-modoc.com:**
1. Add custom domain in Railway
2. Railway will give you DNS records
3. Add these to your domain registrar:
   - CNAME record pointing to Railway's URL
   - Or A record with Railway's IP

### 5. Update URLs in Code

Once deployed, you'll need to update hardcoded URLs:

**Files to update:**
- `templates/base.html` - Update meta tags with actual domain
- `static/sitemap.xml` - Update all URLs to your actual domain
- `static/robots.txt` - Update sitemap URL

**Find and replace:**
- `https://visit-modoc.com/` → `https://your-actual-domain.com/`
- Or use your Railway URL: `https://your-project.up.railway.app/`

### 6. Verify Deployment

After deployment:

1. **Visit your site** at the Railway URL
2. **Check all pages** work correctly
3. **Test forms and links**
4. **Verify sitemap:** `https://your-domain.com/sitemap.xml`
5. **Verify robots.txt:** `https://your-domain.com/robots.txt`

## Post-Deployment Tasks

### Update SEO URLs

Once you have your final domain:

1. Update all `visit-modoc.com` references in:
   - `templates/base.html` (meta tags)
   - `static/sitemap.xml`
   - `static/robots.txt`

2. Commit and push changes:
```bash
git add .
git commit -m "Update URLs to production domain"
git push
```

Railway will automatically redeploy.

### Submit to Search Engines

1. **Google Search Console:**
   - Add your domain
   - Verify ownership
   - Submit sitemap: `https://your-domain.com/sitemap.xml`

2. **Bing Webmaster Tools:**
   - Add site
   - Submit sitemap

### Set Up Google Analytics

1. Create GA4 property at https://analytics.google.com
2. Get your Measurement ID (G-XXXXXXXXXX)
3. Update in Railway:
   - Go to Variables tab
   - Add: `GA_MEASUREMENT_ID` = your ID
4. Or directly edit `templates/base.html` and commit

## Monitoring & Logs

### View Logs

In Railway:
1. Go to your project
2. Click on your service
3. Click "Deployments" tab
4. Click on latest deployment
5. View real-time logs

### Check Status

Railway dashboard shows:
- Service status (running/stopped)
- Resource usage (CPU, memory)
- Recent deployments
- Build logs

## Troubleshooting

### Build Fails

**Check:**
- `requirements.txt` has correct dependencies
- `Procfile` syntax is correct
- Python version in `runtime.txt` is supported

**View build logs** in Railway to see the error.

### Site Not Loading

**Check:**
- Service is running (Railway dashboard)
- No errors in deployment logs
- Environment variables are set correctly
- Port binding (Gunicorn handles this via Procfile)

### 500 Errors

**Check:**
- Application logs in Railway
- All template files are committed to git
- Static files are in the correct directory
- No hardcoded file paths (use `url_for()`)

### Static Files Not Loading

Flask serves static files from `/static/` automatically. Verify:
- Images are in `static/` directory
- Using `url_for('static', filename='...')` in templates
- Files are committed to git

## Railway-Specific Notes

### Free Tier Limits

Railway free tier includes:
- 500 hours/month of usage
- Shared CPU
- 512MB RAM
- 1GB disk

This is plenty for a small tourism website.

### Auto-Deploy

Railway automatically deploys when you push to your main branch. To disable:
1. Go to project settings
2. Toggle off "Auto Deploy"

### Environment Detection

The app checks for `RAILWAY_ENVIRONMENT` variable to enable production mode:
- Debug mode OFF
- Production error handling
- Optimized settings

## Estimated Deployment Time

- **Initial setup:** 5-10 minutes
- **Build time:** 1-2 minutes
- **First deployment:** 3-5 minutes
- **Subsequent deploys:** 1-2 minutes

## Support

**Railway Documentation:** https://docs.railway.app
**Railway Discord:** https://discord.gg/railway
**Flask Documentation:** https://flask.palletsprojects.com

## Checklist

Before going live:

- [ ] Code pushed to GitHub
- [ ] Railway project created and deployed
- [ ] All pages load correctly
- [ ] Images display properly
- [ ] Forms work (if any)
- [ ] URLs updated to production domain
- [ ] sitemap.xml accessible
- [ ] robots.txt accessible
- [ ] Google Analytics configured
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active (automatic with Railway)
- [ ] Sitemap submitted to Google/Bing
- [ ] Test on mobile devices
- [ ] Test all external links
- [ ] Backup project to local machine

## Cost

**Railway Pricing:**
- **Free Tier:** $0/month (with limits)
- **Hobby Plan:** $5/month (more resources)
- **Pro Plan:** $20/month (team features)

For Visit Modoc, the free tier should be sufficient unless you get significant traffic.

## Alternative: Deploy with Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

This is an alternative to deploying via GitHub.

---

**Ready to deploy?** Follow the steps above and your site will be live in minutes!
