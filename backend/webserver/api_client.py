import requests
import logging
import aiohttp
import asyncio

logger = logging.getLogger(__name__)

def http_request(method, url, node, expected_status=requests.codes.ok, timeout=5, **kwargs):
    kwargs.pop("auth", None)
    try:
        r = requests.request(method, url, timeout=timeout, auth=(node.auth_username, node.auth_password), **kwargs)
        if expected_status in range(200, 300) and r.status_code not in range(200, 300):
            logger.error(f"{method} request to {url} failed due to unexpected status code {r.status_code}")
            return None, r.status_code
        # assumes that all requests will return json responses
        # TODO: convert that all requests return json responses
        return r.json(), r.status_code
    except requests.Timeout as e:
        logger.error(f'{method} request to {url} timed out. Full error - {e}')
    except requests.exceptions.JSONDecodeError as e:
        logger.warning(f'{method} request to {url} returned non-json response.')
        return 'success', r.status_code
    except requests.exceptions.RequestException as e:
        logger.error(e)
    return None, 500

async def async_http_request(method, url, node, expected_status=200, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, auth=aiohttp.BasicAuth(node.auth_username, node.auth_password), 
                                   **kwargs) as response:
            if response.status != expected_status:
                logger.error(f"{method} request to {url} failed due to unexpected status code {response.status}")
                return None, response.status
            try:
                return await response.json(), response.status
            except aiohttp.ContentTypeError as e:
                logger.warning(f'{method} request to {url} returned non-json response.')
                return None, response.status
