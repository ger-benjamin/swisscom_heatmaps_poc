# Swisscom heatmaps POC

Based on Swisscom Mobility Insights Platform (MIP)

Aim: display Swisscom heatmap in an Openlayers layer dynamically.

Do not try to use it for now.

## Run POC

If you want a quick frontend/backend demo, checkout the poc branch.

## Run backend

Set up your OAuth credentials and variable.
Create a file `.env` at the root of the project with this content:

```
SWISSCOM_CLIENT_ID=xxx
SWISSCOM_CLIENT_SECRET=xxx
```

Run then

```
make build-all
docker compose up
```

The api will be available at `localhost:8000/`

## Config

In the `docker-compose.yaml` file, you can also set these env:

```
BASE_MONTH=10
BASE_YEAR=2022
MAX_NB_TILES_REQUEST=100
```

## TODO

 - Filter accepted hosts
 - Explain / better views regarding the Swisscom API
   - Use open api?
 - Add a CI
 - push image?
 - Add cache?
 - More OGC like api?
