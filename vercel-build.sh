#!/bin/bash

# 1. Handle API URL Injection
# We inject the Render backend URL into the config.js file during the build.
if [ -z "$RENDER_URL" ]; then
  echo "RENDER_URL not set. Using repo defaults."
else
  echo "Injecting RENDER_URL: $RENDER_URL"
  echo "window.ELITE_API_URL = '$RENDER_URL';" > frontend/js/config.js
fi

# 2. Generate Production Output
# Vercel needs an output directory when a build script is present.
echo "Building Elite Production Assets..."
mkdir -p public
cp -rv frontend/* public/

echo "Build Synchronized."
