""" Test on Cloud Function and GCS
"""

import os
import time
import requests

import pandas as pd

from google.cloud import pubsub_v1
from google.cloud import storage


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

    result = list(
            filter(
                lambda c: collection_name == c["fileName"],
                collections
                )
            )

    return result[0] if result else None


def dsl_upload_file(base_url, headers_with_auth, collection_id, file):
    """ Upload a file for tagging
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


def dsl_download_file(base_url, headers_with_auth, file_id):
    """ Download a file
    """

    # Check if result is ready

    ready = False
    while not ready:
        time.sleep(1)
        status = requests.get(
            f"{base_url}/ftp/files/{file_id}",
            headers=headers_with_auth
            ).json()
        ready = status["ready"]

    # Download the result

    return requests.get(
        f"{base_url}/ftp/files/{file_id}/asfile",
        headers=headers_with_auth,
        stream=True
        )


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


def publish_message(publisher, topic, message):
    """ Publish a message to a topic
    """

    project_id = os.environ["GCP_PROJECT"]
    topic_path = publisher.topic_path(project_id, topic)
    message_data = message.encode("utf-8")

    futures = []
    future = publisher.publish(topic_path, data=message_data)
    futures.append(future)
    for future in futures:
        future.result()


def on_new_file_inbox(file, _context):
    """ Send the file to DSL ML and save the result in GCS
    """

    bucket_name = validate_message(file, "bucket")
    file_name = validate_message(file, "name")
    metadata = validate_message(file, "metadata")
    collection_name = validate_message(metadata, "collection")
    batch_date = validate_message(metadata, "batchdate")

    publisher = pubsub_v1.PublisherClient()
    storage_client = storage.Client()

    headers_with_auth = dsl_get_auth_header(
            DEEPSEA_BASE_URL, USER_NAME, USER_PASS)
    collection_id = dsl_get_collection(
            DEEPSEA_BASE_URL, headers_with_auth, collection_name).get("id")

    blob = storage_client.get_bucket(bucket_name).blob(file_name)
    with storage.fileio.BlobReader(blob) as gcs_file:
        file_id = dsl_upload_file(
                DEEPSEA_BASE_URL, headers_with_auth, collection_id, gcs_file)

    file_data = dsl_download_file(DEEPSEA_BASE_URL, headers_with_auth, file_id)
    bucket = storage_client.get_bucket("outbox-gcp4affi")
    blob = bucket.blob(f"{collection_name}/{collection_name}-{batch_date}.csv")
    with storage.fileio.BlobWriter(blob) as gcs_file:
        for chunk in file_data.iter_content(chunk_size=128):
            gcs_file.write(chunk)

    data = pd.read_csv(
            f"gs://outbox-gcp4affi/{collection_name}/{collection_name}-{batch_date}.csv")
    data.rename(columns={
        '$id': 'id',
        '$rowNum': 'rowNum',
        '$sheetName': 'sheetName',
        'date ($date)': 'date',
        'customerCode ($customerCode)': 'customerCode',
        'customerName ($customerName)': 'customerName',
        'productCode ($productCode)': 'productCode',
        'productName ($productName)': 'productName',
        'address ($address)': 'address',
        'quantity ($quantity)': 'quantity'
        }, inplace=True)
    publish_message(publisher, "new-file-outbox", data.head(1).to_json(orient="records"))
