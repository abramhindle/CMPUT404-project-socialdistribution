import requests
import logging

logger = logging.getLogger(__name__)

def http_request(method, url, expected_status=requests.codes.ok, timeout=5, **kwargs):
    try:
        r = requests.request(method, url, timeout=timeout, **kwargs)
        if r.status_code != expected_status:
            logger.error(f"{method} request to {url} failed due to unexpected status code {r.status_code}")
            return None
        # assumes that all requests will return json responses
        return r.json()
    except requests.Timeout as e:
        logger.error(f'{method} request to {url} timed out. Full error - {e}')
    except requests.exceptions.RequestException as e:
        logger.error(e)
    return None
