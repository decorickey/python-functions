#!/bin/bash

STAGE=$1
AWS_ACCOUNT_ID=$2
IMAGE_REPOSITORY="$AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com/python-serverless-app"

if [ -z "$STAGE" ]; then
  echo "STAGE is required."
  exit 1
fi

if [ -z "$AWS_ACCOUNT_ID" ]; then
  echo "AccountID is required."
  exit 1
fi

sam build --parameter-overrides Stage=$STAGE

sam deploy --parameter-overrides Stage=$STAGE \
  --stack-name "python-serverless-app-$STAGE" \
  --resolve-s3 \
  --image-repository $IMAGE_REPOSITORY \
  --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
  --no-fail-on-empty-changeset \
