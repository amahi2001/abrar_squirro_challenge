"""
Skeleton for Squirro Delivery Hiring Coding Challenge
August 2021
"""
import argparse
import time
import logging
from typing import List, Generator

import requests

log = logging.getLogger(__name__)

class NYTimesSource(object):
    """
    A data loader plugin for the NY Times API.
    """

    def __init__(self):
        self.URI = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

    def connect(self, inc_column=None, max_inc_value=None):
        log.debug("Incremental Column: %r", inc_column)
        log.debug("Incremental Last Value: %r", max_inc_value)

    def disconnect(self):
        """Disconnect from the source."""
        # Nothing to do
        pass

    def flatten_dict(self, article_data: dict, parent_key="") -> dict:
        """Given a dictionary, flatten it into a single level dictionary recursively.
        Can also Flatten nested lists as well. i.e (List[dict[dict[...]]])
        CANNOT handle lists in nested lists. i.e (List[List[...]])

        Args:
            article_data (dict): The article data to flatten
            parent_key (str, optional): Keeps track of parent Key during recursive call. Defaults to "".

        Returns:
            dict: Flattened article data
        """
        res = {}

        for key, value in article_data.items():
            # new key is parent_key.key, if in recursion
            # helps to keep track of nested keys in recursive calls
            new_key = f"{parent_key}.{key}" if parent_key else key

            # if nested dict -> recursively flatten
            if isinstance(value, dict):
                # Recursively flatten the nested dictionary
                flattened_sub = self.flatten_dict(value, new_key)
                res.update(flattened_sub)

            # if list -> flatten each element if it is a dictionary
            elif isinstance(value, list):
                # iterate through list
                for i, elem in enumerate(value):
                    # new keys uses index of list
                    new_key = f"{parent_key}.{key}.{i}" if parent_key else f"{key}.{i}"

                    # if elem is nested dict -> recursively flatten
                    if isinstance(elem, dict):
                        flattened_sub = self.flatten_dict(elem, f"{new_key}")
                        res.update(flattened_sub)

                    # if not nested dict -> add to items
                    else:
                        res[f"{new_key}"] = elem
            # if not dict or list -> add to items
            else:
                res[new_key] = value

        return res

    def getDataBatch(self, batch_size: int) -> Generator[List[dict], None, None]:
        """
        Generator - Get data from source in batches.
        :returns One list for each batch. Each of those is a list of dictionaries with the defined rows.
        """
        page = 0
        batch_ = []

        while True:
            params = {"q": self.args.query, "api-key": self.args.api_key, "page": page}
            try:
                # Get Article Data from NY Times API
                response = requests.get(self.URI, params=params, timeout=10)
                response.raise_for_status()  # This will raise an exception for 4XX or 5XX errors
                articles = response.json().get("response", {}).get("docs", [])

                # If no articles are returned (i.e last page), break the loop
                # return the batch if it is not empty
                if not articles:
                    if batch_:
                        yield batch_
                    break

                # Flatten the article data, and add to the batch
                for article in articles:
                    flattened = self.flatten_dict(article)
                    batch_.append(flattened)

                    # Yield the batch if it reaches the batch size -> reset batch
                    if len(batch_) == batch_size:
                        yield batch_
                        batch_ = []

            # If we reach a rate limit, wait for 60 seconds before retrying
            except requests.exceptions.HTTPError as e:
                # Typically, 429 status code is used for rate limiting
                if response.status_code != 429:
                    raise e
                print("Rate limit exceeded. Waiting before retrying...")
                time.sleep(5)  # Wait for 60 seconds before retrying
                continue  # Retry the current page (next iteration without incrementing page)

            # If there's no exception, increment the page number
            else:
                page += 1

        # Once we break the while loop (i.e no more articles), yield the last batch (if not empty)
        if batch_:
            yield batch_

    def getSchema(self):
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the source
        """
        schema = [
            "title",
            "body",
            "created_at",
            "id",
            "summary",
            "abstract",
            "keywords",
        ]
        return schema


if __name__ == "__main__":
    config = {
        "api_key": "K9LplMlcChFkmKBSm0H4YAEjVD9AwR3u",
        "query": "Silicon Valley",
    }
    source = NYTimesSource()
    # This looks like an argparse dependency - but the Namespace class is just a simple way to create an object holding attributes.
    source.args = argparse.Namespace(**config)
    # source.getDataBatch(10)

    # results = source.getDataBatch(10)

    # # save to json file
    # with open("output.json", "w", encoding="utf-8") as f:
    #     json.dump(list(results), f, indent=4)

    for idx, batch in enumerate(source.getDataBatch(10)):
        print(f"{idx} Batch of {len(batch)} items")
        for item in batch:
            print(item)
            break
            # print(f" - {item['_id']} - {item['headline.main']}")
        test
