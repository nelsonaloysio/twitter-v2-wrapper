#!/usr/bin/env python3

from argparse import ArgumentParser
from os import environ, getpid
from time import sleep, time

import logging as log
import pandas as pd
from searchtweets import (ResultStream,
                          load_credentials,
                          gen_params_from_config)

CREDENTIALS = load_credentials(
    filename="%s/.twitter_keys.yaml" % dict(environ)["HOME"],
    yaml_key="search_tweets_v2",
)

class TwitterWrapper():

    def __init__(self):
        ''' Initializes class. '''

    def stream(self, **params):
        return list(
            self._ResultStream(**params)
                .stream()
        )

    @staticmethod
    def _ResultStream(**params):
        return ResultStream(
            tweetify=params.get("tweetify", False),
            **self._gen_params(**params)
        )

    @staticmethod
    def _gen_params(**params):
        return gen_params_from_config(CREDENTIALS | params)


def main(**args):
    tt = Twitter()

    if args["granularity"]:
        rs = tt.stream(**args)
        print('Returned %s tweets for query "%s".' % sum(r["meta"]["total_tweet_count"] for r in rs))

        # Convert to data frame
        df = pd.concat([pd.DataFrame(r["data"]) for r in rs])
        df.index = [x[:10] for x in df.start]
        df = df.sort_index()["tweet_count"]
        print(df.describe().apply(lambda x: f'{x:.2f}'))

        # Store results
        if args["output"]:
            df.to_json(f'{args["output"]}')

    else:
        captured = 0
        args.pop("granularity", None)

        with open(output, "w") as j:
            while True:
                start = time()

                rs = tt.stream(**args)
                if rs is None:
                    break

                # Store results in JSON file
                list(json.dump(r, j) for r in rs)
                args["since_id"] = rs[0]["id"]

                # Sleep for a bit
                duration = time() - start
                sleep_interval = (float(args["interval"]) * 60) - duration
                if sleep_interval < 0:
                    sleep_interval = (float(args["interval"]) * 60)
                sleep(sleep_interval)


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("query", help="required (leave parameter as blank to ignore)")
    argparser.add_argument("--granularity", default="day", help='count interval (default: "day"')

    argparser.add_argument("--start-time", help='timestamp format "YYYY-MM-DDTHH:MM"')
    argparser.add_argument("--end-time", help='timestamp format "YYYY-MM-DDTHH:MM"')

    argparser.add_argument("--since-id", help="first tweet ID to capture")
    argparser.add_argument("--until-id", help="last tweet ID to capture")

    argparser.add_argument("--interval", default=5, help="polling interval (minutes, default: 5)")
    argparser.add_argument("--max-requests", dest="max_pages", type=int, help="maximum number of requests (pages) per batch")
    argparser.add_argument("--max-results", default=100, dest="results_per_call", type=int, help="maximum results (API default is 10, customly set to 100)")
    argparser.add_argument("--max-tweets", default=100, type=int, help="maximum number of tweets per batch")

    argparser.add_argument("--output", default=f"tweets_{getpid()}", help="output unprocessed results to JSON file")
    argparser.add_argument("--output-format", help="output format: [a]tomic, [r]equest, [m]essage stream", default="r")

    argparser.add_argument("--expansions", help="Specified expansions results in full objects in the 'includes' response object")
    argparser.add_argument("--tweet-fields", help='Tweet JSON attributes to include in endpoint responses (default: "id,text")')
    argparser.add_argument("--user-fields", help='User JSON attributes to include in endpoint responses (default: "id")')
    argparser.add_argument("--media-fields", help='media JSON attributes to include in endpoint responses (default: "id")')
    argparser.add_argument("--place-fields", help='Twitter Place JSON attributes to include in endpoint responses (default: "id")')
    argparser.add_argument("--poll-fields", help='Twitter Poll JSON attributes to include in endpoint responses (default: "id")')
    argparser.add_argument("--extra-headers", help="JSON-formatted str representing a dict of additional HTTP request headers")

    args = vars(argparser.parse_args())
    main(**args)