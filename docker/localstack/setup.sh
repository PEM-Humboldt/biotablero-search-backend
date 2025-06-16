#!/bin/bash
set -e

BUCKET="biotablero-download-files"

if ! awslocal s3api head-bucket --bucket "$BUCKET" 2>/dev/null; then
  echo "Bucket $BUCKET not found. Creating it..."
  awslocal s3api create-bucket --bucket "$BUCKET"
  awslocal s3api put-bucket-cors \
    --bucket "$BUCKET" \
    --cors-configuration file:///etc/localstack/cors.json
else
  echo "Bucket $BUCKET exists. Skipping creation."
fi
