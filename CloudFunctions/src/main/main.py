""" Test on Cloud Function and GCS
"""

import time
import requests
import cloudstorage as gcs
#import pandas as pd

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


def validate_message(message, param):
    """ validate_message
    """

    var = message.get(param)
    if not var:
        raise ValueError(
            f"{param} is not provided. Make sure you have \
                property {param} in the request"
        )
    return var


def on_new_file_inbox(file, _context):
    """ Send the file to DSL ML and save the result in GCS
    """

    bucket = validate_message(file, "bucket")
    filename = validate_message(file, "name")
    metadata = validate_message(file, "metadata")
    collection = validate_message(metadata, "collection")
    batchdate = validate_message(metadata, "batchdate")

    headers_with_auth = dsl_get_auth_header(DEEPSEA_BASE_URL, USER_NAME, USER_PASS)

    collection_id = dsl_get_collection(DEEPSEA_BASE_URL, headers_with_auth, collection)["id"]

    with gcs.open(f"gs://{bucket}/{filename}") as gcs_file:
        file_id = dsl_send_file(DEEPSEA_BASE_URL, headers_with_auth, collection_id, gcs_file)

    # Check if result is ready

    ready = False
    while not ready:
        time.sleep(1)
        status = requests.get(
            f"{DEEPSEA_BASE_URL}/ftp/files/{file_id}",
            headers=headers_with_auth
            ).json()
        ready = status["ready"]

    # Download the result

    result = requests.get(
        f"{DEEPSEA_BASE_URL}/ftp/files/{file_id}/asfile",
        headers=headers_with_auth,
        stream=True
        )
    with gcs.open(f"gs://outbox-gcp4affi/{collection}/{collection}-{batchdate}.csv", "w") as gcs_file:
        for chunk in result.iter_content(chunk_size=128): 
            gcs_file.write(chunk)
