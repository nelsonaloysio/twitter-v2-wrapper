twitter-v2-wrapper
---

Base class and CLI wrapper for [Twitter v2](https://blog.twitter.com/developer/en_us/topics/tools/2021/enabling-the-future-of-academic-research-with-the-twitter-api) API usage (aimed at academic research).

### Requirements

* **[Python 3.9+](https://www.python.org/downloads/)¹**
* pandas>=0.25
* searchtweets-v2>=1.1.1

### Usage

```
usage: twitter_v2_wrapper.py [-h] [--granularity GRANULARITY]
                             [--start-time START_TIME] [--end-time END_TIME]
                             [--since-id SINCE_ID] [--until-id UNTIL_ID]
                             [--interval INTERVAL] [--max-requests MAX_PAGES]
                             [--max-results RESULTS_PER_CALL]
                             [--max-tweets MAX_TWEETS] [--output OUTPUT]
                             [--output-format OUTPUT_FORMAT]
                             [--expansions EXPANSIONS]
                             [--tweet-fields TWEET_FIELDS]
                             [--user-fields USER_FIELDS]
                             [--media-fields MEDIA_FIELDS]
                             [--place-fields PLACE_FIELDS]
                             [--poll-fields POLL_FIELDS]
                             [--extra-headers EXTRA_HEADERS]
                             query

positional arguments:
  query                 required (leave parameter as blank to ignore)

optional arguments:
  -h, --help            show this help message and exit
  --granularity GRANULARITY
                        count interval (default: "day"
  --start-time START_TIME
                        timestamp format "YYYY-MM-DDTHH:MM"
  --end-time END_TIME   timestamp format "YYYY-MM-DDTHH:MM"
  --since-id SINCE_ID   first tweet ID to capture
  --until-id UNTIL_ID   last tweet ID to capture
  --interval INTERVAL   polling interval (minutes, default: 5)
  --max-requests MAX_PAGES
                        maximum number of requests (pages) per batch
  --max-results RESULTS_PER_CALL
                        maximum results (API default is 10, customly set to
                        100)
  --max-tweets MAX_TWEETS
                        maximum number of tweets per batch
  --output OUTPUT       output unprocessed results to JSON file
  --output-format OUTPUT_FORMAT
                        output format: [a]tomic, [r]equest, [m]essage stream
  --expansions EXPANSIONS
                        Specified expansions results in full objects in the
                        'includes' response object
  --tweet-fields TWEET_FIELDS
                        Tweet JSON attributes to include in endpoint responses
                        (default: "id,text")
  --user-fields USER_FIELDS
                        User JSON attributes to include in endpoint responses
                        (default: "id")
  --media-fields MEDIA_FIELDS
                        media JSON attributes to include in endpoint responses
                        (default: "id")
  --place-fields PLACE_FIELDS
                        Twitter Place JSON attributes to include in endpoint
                        responses (default: "id")
  --poll-fields POLL_FIELDS
                        Twitter Poll JSON attributes to include in endpoint
                        responses (default: "id")
  --extra-headers EXTRA_HEADERS
                        JSON-formatted str representing a dict of additional
                        HTTP request headers
```

### Importing as a library

After installing requirements (`pip install -r requirements.txt`) and configuring your credentials, just initialize the class and start collecting:

```
from twitter_v2_wrapper import TwitterWrapper
tw = TwitterWrapper()
```

#### Get tweets from a specific date interval

```
tw.stream(query="#Twitter", start_date="2020-06-20T00:00", end_date="2020-02-30T00:00")
```

#### Get statistics from the last 30 days

```
tw.stream(query="#Twitter", granularity="day")
```

#### Configuring API credentials

By default, the script tries to read a file stored in `~/.twitter_keys.yaml` as per convention:

```
search_tweets_v2:
  endpoint:  https://api.twitter.com/2/tweets/search/recent
  consumer_key: <CONSUMER_KEY>
  consumer_secret: <CONSUMER_SECRET>
  bearer_token: <BEARER_TOKEN>
```

For API-usage related questions, please check the [official documentation](https://github.com/twitterdev/search-tweets-python/tree/v2).
___

¹ See [PEP 584](https://www.python.org/dev/peps/pep-0584/). If you require older version compatibility, take a look at `twitter_v2_wrapper.py:_gen_params()`.