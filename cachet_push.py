import time
from json import dumps
from requests import Session
from os import environ as env

PLEX_URL = env.get('PLEX_URL')
PLEX_LATENCY_METRIC_ID = env.get('PLEX_LATENCY_METRIC_ID')

CACHET_URL = env.get('CACHET_URL')
CACHET_API_KEY = env.get('CACHET_API_KEY')

TAUTULLI_URL = env.get('TAUTULLI_URL')
TAUTULLI_API_KEY = env.get('TAUTULLI_API_KEY')
TAUTULLI_STREAMS_METRIC_ID = env.get('TAUTULLI_STREAMS_METRIC_ID')


class CachetMetrics(object):
    def __init__(self):
        self.t_session = Session()
        self.t_session.params = {'apikey': TAUTULLI_API_KEY, 'cmd': 'get_activity'}
        self.tautulli_stream_count = 0

        self.p_session = Session()

        self.c_session = Session()
        self.c_session.headers = {'Content-Type': 'application/json', 'X-Cachet-Token': CACHET_API_KEY}


    def get_tautulli_stream_count(self):
        endpoint = '/api/v2'

        # Get stream count from tautulli
        count = self.t_session.get(TAUTULLI_URL + endpoint).json()['response']['data']['stream_count']

        self.post(TAUTULLI_STREAMS_METRIC_ID, count)

    def get_plex_response_time(self):
        endpoint = '/identity'

        # Get plex response time
        get = self.p_session.get(PLEX_URL + endpoint)

        response_time = get.elapsed.total_seconds()
        response_ms = (response_time * 1000)

        if get.status_code != 200:
            response_ms = 0

        self.post(PLEX_LATENCY_METRIC_ID, response_ms)

    def post(self, metric, value):
        v = value
        m = metric
        timestamp = time.time()
        rounded_time = int(timestamp // 60 * 60)

        endpoint = '/api/v1/metrics/{metric}/points'
        # Post stream info to cachet

        data = {
            "value": v,
            "timestamp": rounded_time
        }

        full_url = CACHET_URL + endpoint.format(metric=m)
        post = self.c_session.post(full_url, data=dumps(data)).content

        print('Data sent: {}'.format(post))





if __name__ == "__main__":
    CACHET = CachetMetrics()

    CACHET.get_tautulli_stream_count()
    CACHET.get_plex_response_time()
