#!/bin/bash

echo "🔄 Checking for updates..."
git fetch origin main

LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "🚀 New update found! Updating APKnife..."
    git pull origin main
    echo "✅ Update completed successfully!"
else
    echo "👍 APKnife is already up to date."
fi
