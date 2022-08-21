""" DeepSea Loader Python API
"""

import time
import requests

DEFAULT_TAGS = "date, customerCode, customerName, productCode, \
        productName, quantity, amount"

class Client:
    """ DSL Client
    """

    def __init__(self, base_url, token):
        """ Build a DSLClient object
        """

        self._base_url = base_url
        self._token = token

        # Build Authentication header for all successive api calls

        self._headers_with_auth = {
            "Authorization": "Basic " + self._token
        }

    def get_collection(self, collection_name):
        """ Get collection info
        """

        # Find collection sales.monthly from lakefs root

        collections = requests.get(
            f"{self._base_url}/api/v1/lakefs/root",
            headers=self._headers_with_auth
            ).json()

        # filter collection by name

        def first(value):
            return value[0] if value else None
        
        return first(
                list(
                    filter(
                        lambda c: collection_name == c["fileName"],
                        collections
                        )
                    )
                )

    def download_file(self, file_id):
        """ Download a file
        """

        if file_id is None:
            return None

        # Check if result is ready

        ready = False
        while not ready:
            time.sleep(1)
            status = requests.get(
                f"{self._base_url}/ftp/files/{file_id}",
                headers=self._headers_with_auth
                ).json()
            ready = status["ready"]

        # Download the result

        return requests.get(
            f"{self._base_url}/ftp/files/{file_id}/asfile",
            headers=self._headers_with_auth,
            stream=True
            )

    def sample_file(self, collection_id, file, accept_tags = DEFAULT_TAGS):
        """ Sample a file for tagging
        """

        if collection_id is None:
            return None

        # Send a file to be tagged

        headers = {
            "Authorization": self._headers_with_auth["Authorization"],
            "Limits": "0",
            "Accept-Tags": accept_tags
            }
        files = {
            "file": file
            }
        file_id = requests.post(
            f"{self._base_url}/api/v1/lakefs/{collection_id}/samples/asfile",
            headers=headers,
            files=files
            ).text

        # Download the tagged file

        return self.download_file(file_id)
