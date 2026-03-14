#!/bin/bash

FILE_PATH=$1

if [ -z "$FILE_PATH" ]; then
    echo "Usage: ./scripts/process-post.sh content/blog/title/index.en.md"
    exit 1
fi

echo "🤖 Processing $FILE_PATH with Gemini..."

# This command tells the Gemini CLI to execute the SOP defined in GEMINI.md
gemini "Read $FILE_PATH. Edit it for medical authority based on my GEMINI.md. 
        Then, translate it. If the input is English, save the translation as the .bm.md version. 
        If it is Bahasa, save as .en.md. Keep both in $(dirname $FILE_PATH)."

echo "✅ Editing and Translation complete."