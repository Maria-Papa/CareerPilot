#!/bin/bash
set -e

echo "--- Bootstrapping CareerPilot Environment ---"

# 1. Backend Setup
echo "Setting up Python Virtual Environment..."
python -m venv /workspace/backend/.venv
/workspace/backend/.venv/bin/pip install --upgrade pip setuptools wheel
/workspace/backend/.venv/bin/pip install -r /workspace/backend/requirements.txt

# 2. Frontend Setup
echo "Installing Frontend Dependencies..."
cd /workspace/frontend
npm install --yes

# 3. Automation Setup (Playwright)
echo "Installing Playwright Browsers..."
npx -y playwright install chromium --with-deps

echo "--- ✅ Setup Complete! ---"
