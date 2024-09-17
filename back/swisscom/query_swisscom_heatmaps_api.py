import json
from typing import List

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from datetime import datetime, timedelta
from swisscom.tile_id_to_coordinates import tile_id_to_ll

from env import CLIENT_CRED, BASE_MONTH, BASE_YEAR, MAX_NB_TILES_REQUEST

BASE_URL = "https://api.swisscom.com/layer/heatmaps/demo"
TOKEN_URL = "https://consent.swisscom.com/o/oauth2/token"
headers = {"scs-version": "2"}  # API version
CLIENT_ID = CLIENT_CRED['ID']  # customer key in the Swisscom digital marketplace
CLIENT_SECRET = CLIENT_CRED['SECRET']  # customer secret in the Swisscom digital marketplace


def auth()->OAuth2Session:
    # Fetch an access token
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)
    oauth.fetch_token(token_url=TOKEN_URL, client_id=CLIENT_ID,
                      client_secret=CLIENT_SECRET)
    return oauth


def get_tiles_ids(oauth: OAuth2Session, postal_code: int)->List[int] | int:
    # For muni/district id, see https://www.atlas.bfs.admin.ch/maps/13/fr/17804_229_228_227/27579.html
    # Municipalities and Districts doesn't work well probably because of the free plan
    # Get all the first MAX_NB_TILES_REQUEST tile ids associated with the postal code of interest
    muni_tiles_json = oauth.get(
        BASE_URL + "/grids/postal-code-areas/{0}".format(postal_code), headers=headers
    )
    if muni_tiles_json.status_code != 200:
        print("No tiles")
        return muni_tiles_json.status_code
    tiles = muni_tiles_json.json()["tiles"]
    print(f"Nb tiles received: {len(tiles)}")
    return [t["tileId"] for t in muni_tiles_json.json()["tiles"]][:MAX_NB_TILES_REQUEST]


def get_date(day: int, time: int)->datetime:
    start_time = datetime(year=BASE_YEAR, month=BASE_MONTH, day=day, hour=0, minute=0)
    return start_time + timedelta(hours=time)


def query_api_generic(oauth: OAuth2Session, path: str, postal_code:int, day:int, time: int)->str | int:
    print(postal_code, day, time)
    tile_ids = get_tiles_ids(oauth, postal_code)
    if type(tile_ids) == int:
        return tile_ids  # return error or 204
    date = get_date(day, time)
    return (
            BASE_URL
            + "/heatmaps/{0}/{1}".format(path, date.isoformat())
            + "?tiles="
            + "&tiles=".join(map(str, tile_ids))
    )


def response_to_geojson_result(result)->dict[str, str] | int:
    if result.status_code != 200:
        print("No Content")
        return result.status_code
    content = result.json()
    geo_content = {
        "type": "FeatureCollection",
        "features": []
    }
    for element in content["tiles"]:
        coordinate = tile_id_to_ll(element["tileId"])
        geo_content["features"].append({
            "type": "Feature",
            "properties": element,
            "geometry": {
                "type": "Point",
                "coordinates": list(coordinate)
            }
        })
    return json.dumps(geo_content)


def get_dwell_density(postal_code:int, day:int, time: int):
    oauth = auth()
    api_request = query_api_generic(oauth, "/dwell-density/hourly", postal_code, day, time)
    if type(api_request) == int:
        return api_request  # return error or 204
    response = oauth.get(api_request, headers=headers)
    return response_to_geojson_result(response)


def get_dwell_demographics(postal_code:int, day:int, time: int):
    oauth = auth()
    api_request = query_api_generic(oauth, "/dwell-demographics/hourly", postal_code, day, time)
    if type(api_request) == int:
        return api_request  # return error or 204
    response = oauth.get(api_request, headers=headers)
    return response_to_geojson_result(response)