#!/bin/bash
# Run script for Files-On

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado."
    echo "Execute primeiro: ./setup.sh"
    exit 1
fi

# Activate virtual environment and run
source venv/bin/activate
python main.py
