

#!/bin/bash

PROFILE=$1

if [ -z "$PROFILE" ]; then
  echo "Usage: ./deploy.sh <aws-profile-name>"
  exit 1
fi

echo "Building SAM application with profile: $PROFILE"
sam build --use-container --profile "$PROFILE"

if [ $? -ne 0 ]; then
  echo "Build failed. Exiting."
  exit 1
fi

echo "Deploying SAM application with profile: $PROFILE"
sam deploy --guided --profile "$PROFILE"