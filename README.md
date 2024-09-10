# Swisscom heatmaps POC

Based on Swisscom Mobility Insights Platform (MIP)

Aim: display Swisscom heatmap in an Openlayers layer dynamically.

Do not try to use it for now.

## Run it

You need to run the frontend and the backend separately.

### Backend

```
cd back
```

Set up your OAuth credentials. Create a file `env.py` here, in the `back` folder, with this content:

```
CLIENT_CRED = {
    'ID': "",
    'SECRET': ""
}
```

Then run: `python3 server.py`. The api will be available at `localhost:8000/`

## Front

Go in the front directory, install and run the examples:

```
cd front
npm install
npm run start
```
