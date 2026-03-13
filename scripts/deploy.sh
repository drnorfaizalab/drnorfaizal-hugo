#!/bin/bash

# 1. Load Secrets
# Ensures your Cloudflare tokens are active for this session
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "❌ Error: .env file not found. Please create it with CF_ZONE_ID and CF_API_TOKEN."
  exit 1
fi

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
# This ensures your 300 million potential readers see the LATEST version immediately
if [ -n "$CF_API_TOKEN" ] && [ -n "$CF_ZONE_ID" ]; then
    echo "🧹 Purging Cloudflare Edge Cache..."
    PURGE_RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/purge_cache" \
        -H "Authorization: Bearer $CF_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{"purge_everything":true}')
    
    if echo "$PURGE_RESPONSE" | grep -q '"success":true'; then
        echo "✅ Cache Purged Successfully."
    else
        echo "⚠️  Cache Purge Failed. Check your API Token permissions."
        echo "$PURGE_RESPONSE"
    fi
else
    echo "ℹ️  Skipping Cache Purge: Credentials not set in .env"
fi

echo "🏁 Process Complete. Your clinical authority has compounded."