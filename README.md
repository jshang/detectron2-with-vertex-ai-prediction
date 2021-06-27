# detectron2-with-vertex-ai-prediction

## Configure gcloud command

```
$ export GCP_PROJECT_ID=<YOUR PROJECT ID>
$ gcloud auth login --project $GCP_PROJECT_ID
```

## Build a new docker image

```
$ gcloud builds submit --config cloudbuild.yml . --project $GCP_PROJECT_ID --timeout=60m --async
```
