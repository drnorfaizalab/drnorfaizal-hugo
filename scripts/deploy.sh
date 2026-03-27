#!/bin/bash

# 1. Load Secrets
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "❌ Error: .env file not found."
  exit 1
fi

# --- NEW SAFETY INTERLOCK ---
# 1b. Check if .env is being tracked by Git
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
    echo "🚨 SECURITY ALERT: .env is being tracked by Git!"
    echo "Removing .env from Git cache (keeping local file)..."
    git rm --cached .env
    echo ".env added to Git ignore list. Please commit this change."
    exit 1
fi
# -----------------------------

# 2. Clean & Build...

# 2. Clean & Build
echo "🏗️  Starting Hugo Build (Minified)..."
rm -rf public
hugo --gc --minify

# 3. Git Automation
echo "📦 Staging changes for GitHub..."
git add .

# Check if there are changes to commit
if git diff-index --quiet HEAD --; then
    echo "Check: No changes to commit."
else
    # Automatically generate a timestamped commit message if none provided
    read -t 5 -p "Enter commit message [Default: Site Update]: " msg
    msg=${msg:-"Site Update $(date +'%Y-%m-%d %H:%M')"}
    git commit -m "$msg"
    
    echo "🚀 Pushing to GitHub (Cloudflare Pages will auto-deploy)..."
    git push origin main
fi

# 4. Cloudflare Cache Purge
if [ -n "$CF_API_TOKEN" ] && [ -n "$CF_ZONE_ID" ]; then
    echo "🧹 Purging Cloudflare Edge Cache..."
    PURGE_RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
        -H "Authorization: Bearer ${CF_API_TOKEN}" \
        -H "Content-Type: application/json" \
        --data '{"purge_everything":true}')

    if echo "$PURGE_RESPONSE" | grep -q '"success":true'; then
        echo "✅ Cache Purged Successfully."
    else
        echo "⚠️  Cache Purge Failed. Response: $PURGE_RESPONSE"
    fi
fi

echo "🏁 Process Complete. Your clinical authority has compounded."