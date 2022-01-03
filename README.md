twitter-v2-search
---

Base class and CLI wrapper for [Twitter v2](https://blog.twitter.com/developer/en_us/topics/tools/2021/enabling-the-future-of-academic-research-with-the-twitter-api) API usage (aimed at academic research).

### Requirements

* **[Python 3.5+](https://www.python.org/downloads/)**
* requests (>=2.24)

### Usage

```
usage: twitter_v2_search.py [-h] [-o OUTPUT_FILE] [--days] [--hours]
                            [--minutes] [--start-time START_TIME]
                            [--end-time END_TIME] [--since-id SINCE_ID]
                            [--until-id UNTIL_ID] [--max-results MAX_RESULTS]
                            [--expansions EXPANSIONS]
                            [--tweet-fields TWEET_FIELDS]
                            [--media-fields MEDIA_FIELDS]
                            [--poll-fields POLL_FIELDS]
                            [--place-fields PLACE_FIELDS]
                            [--user-fields USER_FIELDS]
                            [--extra-headers EXTRA_HEADERS]
                            [--interval INTERVAL] [--limit LIMIT]
                            query

positional arguments:
  query                 Required (leave parameter as blank to ignore)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Write returned data to JSON file
  --days                Returns daily tweet count
  --hours               Returns hourly tweet count
  --minutes             Returns tweet count per minute
  --start-time START_TIME
                        Timestamp format "YYYY-MM-DDTHH:MM:SS+00:00:00"
  --end-time END_TIME   Timestamp format "YYYY-MM-DDTHH:MM:SS+00:00:00"
  --since-id SINCE_ID   First tweet ID to capture
  --until-id UNTIL_ID   Last tweet ID to capture
  --max-results MAX_RESULTS
                        Maximum results (API default is 10, customly set to
                        100)
  --expansions EXPANSIONS
                        Specified expansions results in full objects in the
                        'includes' response object
  --tweet-fields TWEET_FIELDS
                        Tweet JSON attributes to include in endpoint responses
                        (default: "id, text")
  --media-fields MEDIA_FIELDS
                        Media JSON attributes to include in endpoint responses
                        (default: "id")
  --poll-fields POLL_FIELDS
                        Twitter Poll JSON attributes to include in endpoint
                        responses (default: "id")
  --place-fields PLACE_FIELDS
                        Twitter Place JSON attributes to include in endpoint
                        responses (default: "id")
  --user-fields USER_FIELDS
                        User JSON attributes to include in endpoint responses
                        (default: "id")
  --extra-headers EXTRA_HEADERS
                        JSON-formatted str representing a dict of additional
                        HTTP request headers
  --interval INTERVAL   Request interval (seconds, default: 1)
  --limit LIMIT         Maximum number of tweets to capture
```

A [Jupyter notebook](twitter_v2_search.ipynb) is included with examples for the following scenarios below.

### Examples

#### Get original tweets from a specific date interval

Continues searching until collection is finished. Alternatively use `since_id` and `until_id` to paginate through results.

```
twitter_v2_search.py "#Twitter -is:retweet" --start-time "YYYY-MM-DDTHH:MM:SS+00:00:00" --end-time "YYYY-MM-DDTHH:MM:SS+00:00:00"
```

#### Get daily retweet count from the last 30 days

In order to write the results to a file, append e.g. `--output-file tweets.csv` to the command line below.

```
twitter_v2_search.py "#Twitter is:retweet" --days
```

### Importing as a library

After installing requirements (`pip install -r requirements.txt`), just initialize the class and start collecting:

```
from twitter_v2_search import TwitterSearch
twitter = TwitterSearch()
```

#### Request data from Twitter (default)

Requests data from a specific Twitter `endpoint`, such as the example below.

```
twitter.request(
  query="#Twitter",
  endpoint="https://api.twitter.com/2/tweets/search/all",
  bearer_token="<BEARER_TOKEN>",
)
```

**Note**: if both `BEARER_TOKEN` environment variable and `bearer_token` argument parameter are set, the latter will take precedence.

#### Get original tweets from a specific date interval

Queries the same `endpoint` as the example above, but paginates results until collection is finished.

```
twitter.search(
  query="#Twitter -is:retweet",
  start_date="2020-06-20T00:00:00+00:00:00",
  end_date="2020-02-30T00:00:00+00:00:00",
)
```

#### Get daily retweet count from the last 30 days

Returns number of tweets matching query, by default over the last month.

```
twitter.search(
  query="#Twitter is:retweet",
  granularity="day",
)
```

For API usage related questions, please also refer to the [official library documentation](https://github.com/twitterdev/search-tweets-python/tree/v2).

___

### References

* https://developer.twitter.com/en/products/twitter-api/academic-research

* https://github.com/twitterdev/search-tweets-python/tree/v2

* https://github.com/twitterdev/Twitter-API-v2-sample-code/
