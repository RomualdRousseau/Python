""" Test on Cloud Function and GCS
"""

import os
import json

from google.cloud import pubsub_v1
from google.cloud import storage

import deepsealoader

PROJECT_ID = os.environ["PROJECT_ID"]
OUTPUT = os.environ["OUTPUT"]
TOPIC = os.environ["TOPIC"]

DSL_BASE_URL = os.environ["DSL_BASE_URL"]
DSL_TOKEN = os.environ["DSL_TOKEN"]


def validate_message(message, param):
    """ Validate a given message
    """

    var = message.get(param)
    if not var:
        raise ValueError(
            f"{param} is not provided. Make sure you have \
                property {param} in the request"
        )
    return var


def publish_message(publisher, topic, message):
    """ Publish a given message to a given topic
    """

    topic_path = publisher.topic_path(PROJECT_ID, topic)
    message_data = json.dumps(message).encode("utf-8")
    
    futures = []
    future = publisher.publish(topic_path, data=message_data)
    futures.append(future)
    for future in futures:
        future.result()


def on_new_file_inbox(file, _context):
    """ Send the file to DSL ML and save the result in GCS
    """

    # Collect info about the new file

    bucket_name = validate_message(file, "bucket")
    file_name = validate_message(file, "name")
    metadata = validate_message(file, "metadata")
    collection_name = validate_message(metadata, "collection")
    batch_date = validate_message(metadata, "batchdate")
    output_file_name = f"{collection_name}/{collection_name}-{batch_date}.csv"

    # Connect to the various services

    publisher = pubsub_v1.PublisherClient()
    dsl_client = deepsealoader.Client(DSL_BASE_URL, DSL_TOKEN)
    storage_client = storage.Client()

    # Tag the new file using DSL ML

    print(f"Processing gs://{bucket_name}/{file_name} ...")

    blob = storage_client.get_bucket(bucket_name).blob(file_name)
    with storage.fileio.BlobReader(blob) as gcs_file:
        collection_id = dsl_client.get_collection(collection_name).get("id")
        file_data = dsl_client.sample_file(collection_id, gcs_file)

    # Save the tagged file in GCS

    print(f"Saving gs://{OUTPUT}/{output_file_name} ...")

    blob = storage_client.get_bucket(OUTPUT).blob(output_file_name)
    with storage.fileio.BlobWriter(blob) as gcs_file:
        for chunk in file_data.iter_content(chunk_size=1024):
            gcs_file.write(chunk)

    # Publish the avaibility of the tagged file

    print(f"Notifying {TOPIC} ...")

    publish_message(publisher, TOPIC, {
            "bucket": OUTPUT,
            "file_name": output_file_name
        })
