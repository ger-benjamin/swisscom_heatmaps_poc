import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from datetime import datetime, timedelta
from swisscom.tile_id_to_coordinates import tile_id_to_ll

from env import CLIENT_CRED

BASE_URL = "https://api.swisscom.com/layer/heatmaps/demo"
TOKEN_URL = "https://consent.swisscom.com/o/oauth2/token"
MAX_NB_TILES_REQUEST = 100
headers = {"scs-version": "2"}  # API version
client_id = CLIENT_CRED['ID']  # customer key in the Swisscom digital market place
client_secret = CLIENT_CRED['SECRET']  # customer secret in the Swisscom digital market place

def get_dwell_density(postal_code:int, day:int, time: int):
    print(postal_code, day, time)
    # Fetch an access token
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    oauth.fetch_token(token_url=TOKEN_URL, client_id=client_id,
                      client_secret=client_secret)

    # Get all the first MAX_NB_TILES_REQUEST tile ids associated with the postal code of interest
    muni_tiles_json = oauth.get(
        BASE_URL + "/grids/postal-code-areas/{0}".format(postal_code), headers=headers
    ).json()
    tile_ids = [t["tileId"] for t in muni_tiles_json["tiles"]][
        :MAX_NB_TILES_REQUEST
    ]

    start_time = datetime(year=2022, month=10, day=day, hour=0, minute=0)
    date = start_time + timedelta(hours=time)

    api_request = (
        BASE_URL
        + "/heatmaps/dwell-density/hourly/{0}".format(date.isoformat())
        + "?tiles="
        + "&tiles=".join(map(str, tile_ids))
    )
    result = oauth.get(api_request, headers=headers)
    print(result.status_code)
    content = result.json()
    geo_content = {
        "type": "FeatureCollection",
        "features": []
    }
    for element in content["tiles"]:
        coordinate = tile_id_to_ll(element["tileId"])
        geo_content["features"].append({
            "type": "Feature",
            "properties": {"score": element["score"]},
            "geometry": {
                "type": "Point",
                "coordinates": list(coordinate)
            }
        })
    return json.dumps(geo_content)

    # define a start time and request the density for the following given number of hours
    # start_time = datetime(year=2022, month=10, day=10, hour=0, minute=0)
    # dates = [(start_time + timedelta(hours=delta)) for delta in range(24)]
    # date2score = dict()

    # for dt in dates:
    #     api_request = (
    #         BASE_URL
    #         + "/heatmaps/dwell-density/hourly/{0}".format(dt.isoformat())
    #         + "?tiles="
    #         + "&tiles=".join(map(str, tile_ids))
    #     )
    #     result = oauth.get(api_request, headers=headers)
    #     print(result.status_code)
    #     print(result.json())
    #     daily_total_density = sum(
    #         map(
    #             lambda t: t["score"],
    #             result.json()["tiles"],
    #         )
    #     )
    #     date2score[dt.isoformat()] = daily_total_density
    # return date2score

  # # print the daily density for every date
  # print("The average hourly density for postal code {0}".format(postal_code))
  # pprint.PrettyPrinter(indent=4).pprint(date2score)
