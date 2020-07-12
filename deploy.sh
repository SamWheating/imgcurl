#!/bin/bash

SERVICE_NAME=raccooon
IMAGE=gcr.io/personalsite-264919/raccoon:latest

gcloud config set account samwheating@gmail.com
docker build -t $IMAGE .
docker push $IMAGE
gcloud run deploy $SERVICE_NAME --image $IMAGE --region us-central1 --platform managed --project personalsite-264919

