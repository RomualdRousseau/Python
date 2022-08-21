""" Test on Cloud Function and GCS
"""

import sys
import time
import requests

DEEPSEA_BASE_URL = "https://deepsealoader.servier.com.cn"

USER_NAME = "black.mortimer@servier.com"

USER_PASS = "mortimer"


def dsl_get_auth_header(base_url, user, password):
    """ Get auth header from DSL
    """

    # Get the token to access DSL api

    token = requests.get(
        f"{base_url}/auth/token",
        {"user": user, "password": password}
        ).text

    print(token)

    # Build Authentication header for all successive api calls

    return {
        "Authorization": "Basic " + token
    }


def dsl_get_collection(base_url, headers_with_auth, collection_name):
    """ Get collection info
    """

    # Find collection sales.monthly from lakefs root

    collections = requests.get(
        f"{base_url}/api/v1/lakefs/root",
        headers=headers_with_auth
        ).json()

    # filter collection by name

    by_name = lambda n, c: n == c["fileName"]
    result = list(filter(lambda c: by_name(collection_name, c), collections))

    if not result:
        return None
    else:
        return result[0]


def dsl_send_file(base_url, headers_with_auth, collection_id, file):
    """ Send a file for tagging
    """

    # Send a file to be tagged

    headers = {
        "Authorization": headers_with_auth["Authorization"],
        "Limits": "0",
        "Accept-Tags": "date, customerCode, customerName, productCode, \
                productName, address, quantity"
    }

    return requests.post(
        f"{base_url}/api/v1/lakefs/{collection_id}/samples/asfile",
        headers=headers,
        files={"file": file}).text


def _main():
    collection_name = "sales.zuellig"
    headers_with_auth = dsl_get_auth_header(DEEPSEA_BASE_URL, USER_NAME, USER_PASS)
    collection = dsl_get_collection(DEEPSEA_BASE_URL, headers_with_auth, collection_name)
    if collection:
        print(collection["id"])

if __name__ == "__main__":
    sys.exit(_main())
