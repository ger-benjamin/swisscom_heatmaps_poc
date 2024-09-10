from swisscom.query_swisscom_heatmaps_api import get_dwell_density

class Entry():
    def get_dwell_density(self):
        result = get_dwell_density();
        print(result);
        return result;