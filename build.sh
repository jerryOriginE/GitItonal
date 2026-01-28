#!/bin/bash

set -e

APP_NAME="GitItonal"
ENTRY_POINT="app/run.py"

echo "Cleaning old builds..."
rm -rf build dist __pycache__ *.spec

echo "Building with PyInstaller..."

pyinstaller \
  --name $APP_NAME \
  --onefile \
  --clean \
  --noconfirm \
  --add-data "app/templates:app/templates" \
  --add-data "app/static:app/static" \
  --hidden-import fastapi \
  --hidden-import uvicorn \
  --hidden-import uvicorn.logging \
  --hidden-import uvicorn.loops \
  --hidden-import uvicorn.protocols \
  --hidden-import uvicorn.protocols.http \
  --hidden-import uvicorn.protocols.websockets \
  --hidden-import uvicorn.lifespan \
  --hidden-import app.gitutils \
  --hidden-import app.git_sync \
  $ENTRY_POINT

echo "Build complete!"
echo "Binary located at: dist/$APP_NAME"