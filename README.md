# detectron2-with-vertex-ai-prediction

This repository is an example code for Vertex AI Prediction + Detectron 2. This README shows how to deploy a detectron2 demo application on Vertex AI Prediction.

## Configure gcloud command

```console
$ export GCP_PROJECT_ID=<YOUR PROJECT ID>
$ gcloud auth login --project ${GCP_PROJECT_ID}
```

## Build a new docker image

```console
$ gcloud builds submit \
  --config cloudbuild.yml . \
  --project ${GCP_PROJECT_ID} \
  --timeout=60m --async
```

## Create a custom model on Vertex AI

```console
$ gcloud beta ai models upload \
  --region=us-west1 \
  --display-name=detectron2-demo \
  --container-image-uri=gcr.io/${GCP_PROJECT_ID}/detectron2-with-vertex-ai-prediction:latest \
  --container-ports=5000 \
  --container-health-route=/healthcheck \
  --container-predict-route=/predict
```
## Create an endpoint on Vertex AI Prediction

```console
$ gcloud beta ai endpoints create \
  --region=us-west1 \
  --display-name=detectron2-demo-app
```


## Deploy a custom model on Vertex AI Prediction

```console
$ export VERTEX_AI_ENDPOINT_ID="$(gcloud beta ai endpoints list --region=us-west1 | grep detectron2-demo-app | awk '{print $1}')"
$ export VERTEX_AI_MODEL_ID="$(gcloud beta ai models list --region=us-west1 | grep detectron2-demo | awk '{print $1}')"
$ gcloud beta ai endpoints deploy-model  ${VERTEX_AI_ENDPOINT_ID} \
  --region=us-west1 \
  --model=${VERTEX_AI_MODEL_ID} \
  --display-name=detectron2-demo-app \
  --machine-type=n1-standard-2 \
  --accelerator=count=1,type=nvidia-tesla-t4 \
  --min-replica-count=1 \
  --max-replica-count=1 \
  --traffic-split=0=100
```

## Send a request to the endpoint

```console
$ export GCP_PROJECT_NUMBER="$(gcloud projects list | grep ${GCP_PROJECT_ID} | awk '{print $3}')"
$ wget http://images.cocodataset.org/val2017/000000439715.jpg -q -O input.jpg
$ echo '{"data": {"b64":"'$(base64 input.jpg)'"}}' | tee req.json
$ curl -X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://us-west1-aiplatform.googleapis.com/v1/projects/${GCP_PROJECT_NUMBER}/locations/us-west1/endpoints/${VERTEX_AI_ENDPOINT_ID}:predict \
-d @req.json
```


## Clean up the custom model

```console
$ gcloud beta ai endpoints delete $VERTEX_AI_ENDPOINT_ID --region=us-west1
$ gcloud beta ai models delete $VERTEX_AI_ENDPOINT_ID --region=us-west1
```
