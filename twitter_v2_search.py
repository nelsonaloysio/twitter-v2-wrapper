#!/usr/bin/env python3

import json
import logging as log
from argparse import ArgumentParser
from collections import defaultdict
from os import environ, mkdir
from os.path import dirname, isdir, splitext
from time import sleep, time

import requests

log.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=log.INFO,
)

BEARER_TOKEN = environ.get("BEARER_TOKEN")

ENDPOINT_DEFAULT = "https://api.twitter.com/2/tweets/{}/all"


class Twitter():

    def __init__(self):
        ''' Initializes class. '''

    def request(self, endpoint, bearer_token=BEARER_TOKEN, **params) -> dict:
        headers = self.__create_headers(bearer_token)
        response = self.__connect_to_endpoint(endpoint, headers, **params)
        return response

    @staticmethod
    def __connect_to_endpoint(endpoint, headers, **params) -> dict:
        response = requests.request(
            "GET", endpoint, headers=headers, params=params)
        if response.status_code != 200:
            log.error(f"{response.status_code}: {response.text}")
        return response

    @staticmethod
    def __create_headers(bearer_token) -> dict:
        return {"Authorization": f"Bearer {bearer_token}"}


class TwitterSearch(Twitter):

    def search(self, interval=1, limit=0, low_memory=False, output_file=None, **params) -> dict:
        '''
        Returns tweet data, loops until finished.
        '''
        def add_response(json_response):
            for key, item in json_response.items():
                if type(item) == list:
                    output_dict[key] += item
                elif type(item) == dict:
                    add_response(item)

        total = 0
        time_to_print = time()
        output_dict = defaultdict(list)

        if low_memory is True and output_file is None:
            raise ValueError("missing required OUTPUT_FILE parameter for LOW_MEMORY operations.")

        while True:
            response = self.request(
                endpoint=ENDPOINT_DEFAULT.format("search" if params.get("granularity") is None else "counts"),
                **self.__params(**params),
            )

            if response.status_code != 200:
                seconds = (30 if response.status_code == 429 else 5)
                log.info(f"Retrying in {seconds} seconds...")
                sleep(seconds)
                continue

            response = response.json()

            if low_memory is not True:
                add_response(response)

            if output_file is not None:
                self.__write_json(response, output_file, mode="a" if total else "w")

            total += response.get("meta", {}).get("result_count", response.get("meta", {}).get("total_tweet_count", 0))
            params["next_token"] = response.get("meta", {}).get("next_token", None)

            if (params["next_token"] is None) or (limit and total >= limit):
                break

            if (time() - time_to_print) > 10:
                log.info(f"Returned {total} tweets.")
                time_to_print = time()

            sleep(interval) if float(interval) > 0 else None

        log.info(f"Returned {total} total tweets.")
        return dict(output_dict)

    @staticmethod
    def __params(interval=None, limit=None, low_memory=False, output_file=None, **params) -> dict:
        '''
        Returns valid parameters only, ignores unrequired arguments from within class.
        '''
        return {
            key: value
            for key, value in params.items()
            if value is not None and (
                params.get("granularity") is None or key != "max_results"
            )
        }

    @staticmethod
    def __write_json(json_response, output_file, mode="w") -> None:
        '''
        Dumps responses to file, one record per line.
        '''
        def write_response(json_response):
            for key, item in json_response.items():
                if type(item) == list:
                    with open(f"{file_name}_{key}.json", mode) as j:
                        for response in item:
                            json.dump(response, j, sort_keys=True)
                            j.write('\n')
                elif type(item) == dict:
                    write_response(item)

        file_name = splitext(output_file)[0]
        folder_name = dirname(output_file)

        if folder_name and not isdir(folder_name):
            mkdir(folder_name)

        write_response(json_response)


def args() -> dict:
    argparser = ArgumentParser()
    argparser.add_argument("query", help="Required (leave parameter as blank to ignore)")
    argparser.add_argument("-o", "--output-file", default="RESULTS/tweets.json", dest="output_file", help="Write returned data to JSON file")
    argparser.add_argument("--days", action="store_const", const="day", dest="granularity", help='Returns daily tweet count')
    argparser.add_argument("--hours", action="store_const", const="hour", dest="granularity", help='Returns hourly tweet count')
    argparser.add_argument("--minutes", action="store_const", const="minute", dest="granularity", help='Returns tweet count per minute')
    argparser.add_argument("--start-time", help='Timestamp format "YYYY-MM-DDTHH:MM:SS+00:00:00"')
    argparser.add_argument("--end-time", help='Timestamp format "YYYY-MM-DDTHH:MM:SS+00:00:00"')
    argparser.add_argument("--since-id", help="First tweet ID to capture")
    argparser.add_argument("--until-id", help="Last tweet ID to capture")
    argparser.add_argument("--next-token", help="Pagination token to proceed with a previous query.")
    argparser.add_argument("--max-results", default=100, type=int, help="Maximum results (API default is 10, customly set to 100)")
    argparser.add_argument("--expansions", help="Specified expansions results in full objects in the 'includes' response object")
    argparser.add_argument("--tweet-fields", dest="tweet.fields", help='Tweet JSON attributes to include in endpoint responses (default: "id, text")')
    argparser.add_argument("--media-fields", dest="media.fields", help='Media JSON attributes to include in endpoint responses (default: "id")')
    argparser.add_argument("--poll-fields", dest="poll.fields", help='Twitter Poll JSON attributes to include in endpoint responses (default: "id")')
    argparser.add_argument("--place-fields", dest="place.fields", help='Twitter Place JSON attributes to include in endpoint responses (default: "id")')
    argparser.add_argument("--user-fields", dest="user.fields", help='User JSON attributes to include in endpoint responses (default: "id")')
    argparser.add_argument("--extra-headers", help="JSON-formatted str representing a dict of additional HTTP request headers")
    argparser.add_argument("--interval", default=1, type=float, help="Request interval (seconds, default: 1)")
    argparser.add_argument("--limit", default=None, type=int, help="Maximum number of tweets to capture")
    return vars(argparser.parse_args())


def main(**args) -> None:
    twitter = TwitterSearch()
    response = twitter.search(low_memory=True, **args)
    return response


if __name__ == "__main__":
    main(**args())
