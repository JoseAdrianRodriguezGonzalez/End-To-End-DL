#!/usr/bin/env bash

set -e

# Hyperparameter tuning
uv run python main.py tune \
  --trials 20 \
  --output_path artifacts/best_params.json

# Final training
uv run python main.py trainer \
  --params artifacts/best_params.json \
  --output_path artifacts/best_model.pth \
  --output_media artifacts/training

# ONNX export
uv run python main.py export \
  --model artifacts/best_model.pth \
  --name vgg11 \
  --labels 10 \
  --output serving/model_repository/cnn/1/model.onnx \
  --device cpu
