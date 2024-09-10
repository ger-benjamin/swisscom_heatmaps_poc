from swisscom.query_swisscom_heatmaps_api import get_dwell_density, get_dwell_demographics

class Entry():
    def get_dwell_density(self, postal_code: int, day: int, time: int):
        result = get_dwell_density(postal_code, day, time)
        return result

    def get_dwell_demographics(self, postal_code: int, day: int, time: int):
        result = get_dwell_demographics(postal_code, day, time)
        return result
