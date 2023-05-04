import datetime
import json
import os
import requests
from pathlib import Path
from urllib.parse import urljoin, urlencode
BLUESKY_HOST = os.environ.get("BLUESKY_HOST")
BLUESKY_USERNAME = os.environ.get("BLUESKY_IDENTIFIER")
BLUESKY_PASSWORD = os.environ.get("BLUESKY_PASSWORD")


def hello():
    print('Hello from the API')
    print(f'{BLUESKY_HOST=}')
    print(f'{BLUESKY_USERNAME=}')
    print(f'{BLUESKY_PASSWORD=}')


def demo():
    host = BLUESKY_HOST
    username = BLUESKY_USERNAME
    password = BLUESKY_PASSWORD

    print("#### Created session:")
    created_session = session_create(host=host, username=username, password=password)
    sesh = created_session.json()
    print(json.dumps(sesh, indent=2))

    print("\n\n")
    print("#### Refresh session:")
    resp = session_refresh(host=host, token=sesh['refreshJwt'])
    print(json.dumps(resp.json(), indent=2))

    print("\n\n")
    print("#### Get session info:")
    resp = session_get(host=host, token=sesh['accessJwt'])
    print(json.dumps(resp.json(), indent=2))

    print("\n\n")
    print("#### Get post:")
    post_url = 'https://staging.bsky.app/profile/did:plc:oky5czdrnfjpqslsw2a5iclo/post/3juhjpcvvr524'
    author_id = 'did:plc:oky5czdrnfjpqslsw2a5iclo'
    post_id = '3juhjpcvvr524'


    resp = post_get(host=host, token=sesh['accessJwt'], author_id=author_id, post_id=post_id)
    print(json.dumps(resp.json(), indent=2))





def build_url(host, path="", params={}):
    if not params:
        url = urljoin(host, path)
    else:
        url = urljoin(host, path) + '?' + urlencode(params)

    return url


def session_create(host=BLUESKY_HOST, username=BLUESKY_USERNAME, password=BLUESKY_PASSWORD):
    """
    {
      "did": "did:plc:oz2XXXXXXw5",
      "handle": "XXX.bsky.social",
      "email": "XXX@gmail.com",
      "accessJwt": "eyXXXX.eYYYYY.sZZZZZ",
      "refreshJwt": "eAAAA.eBBBB.gWWWWW"
    }
    """
    atp_endpoint = "/xrpc/com.atproto.server.createSession"
    payload = {
        'identifier': username,
        'password': password
    }
    endpoint_url = build_url(host, atp_endpoint)

    response = requests.post(endpoint_url, json=payload)
    return response



def session_get(host, token):
    """
    session_token is accessJwt
    {"handle": "xxx.bsky.social", "did": "did:plc:xxx", "email": "xxx@gmail.com"}

    """
    atp_endpoint = "/xrpc/com.atproto.server.getSession"
    endpoint_url = build_url(host, atp_endpoint)
    headers = {"Authorization": "Bearer " + token}

    resp = requests.get(
        endpoint_url,
        headers=headers
    )

    return resp



def session_refresh(host, token):
    """
    token is a string and comes from refreshJwt in the session object
    """
    atp_endpoint = "/xrpc/com.atproto.server.refreshSession"
    endpoint_url = build_url(host, atp_endpoint)
    headers = {"Authorization": "Bearer " + token}

    resp = requests.post(
        endpoint_url,
        headers=headers
    )

    return resp



def extract_from_post_url(url):
    """
    TODO
    given post url
    https://staging.bsky.app/profile/did:plc:oky5czdrnfjpqslsw2a5iclo/post/3juhjpcvvr524
    host id:
    bsky.app
    author_id is:
    did:plc:oky5czdrnfjpqslsw2a5iclo
    post id is:
    3juhjpcvvr524
    """
    pass


def post_get(host, token, author_id, post_id):
    """
    given post url
    https://staging.bsky.app/profile/did:plc:oky5czdrnfjpqslsw2a5iclo/post/3juhjpcvvr524
    author_id is:
    did:plc:oky5czdrnfjpqslsw2a5iclo
    post id is:
    3juhjpcvvr524
    session_token is accessJwt

    result:

    {
      "posts": [
        {
          "uri": "at://did:plc:oky5czdrnfjpqslsw2a5iclo/app.bsky.feed.post/3juhjpcvvr524",
          "cid": "bafyreido5u7od4d2qsapcnafs457vvrbt3ggczpklfraiii3bobzup7lvi",
          "author": {
            "did": "did:plc:oky5czdrnfjpqslsw2a5iclo",
            "handle": "jay.bsky.team",
            "displayName": "Jay 🦋",
            "avatar": "https://cdn.bsky.social/imgproxy/ogSgUNedsoOiSf3Tu_rixfF3Ku4lJPeBJV_oam5TKqU/rs:fill:1000:1000:1:0/plain/bafkreihquydaf5xer53afkmdefp2hpwbtqcgurxo2hsdkrpwpvm6uhkyg4@jpeg",
            "viewer": {
              "muted": false,
              "blockedBy": false,
              "following": "at://did:plc:USER_DID/app.bsky.graph.follow/abc",
              "followedBy": "at://did:plc:AUTHOR_DID/app.bsky.graph.follow/xyz"
            },
            "labels": []
          },
          "record": {
            "text": "We've started to use invite chains as an input for reputation. Invites are private to servers, and can be tooling for server admins to protect their community.\n\nAfter today, if a banned/actioned account invited you or you invited them, your posts may temporarily not show up in the What’s Hot feed.",
            "$type": "app.bsky.feed.post",
            "reply": {
              "root": {
                "cid": "bafyreibc7bec77etpxmcp5krm44nv7svzyhxalqru4i45bfkgpkzoiglsm",
                "uri": "at://did:plc:oky5czdrnfjpqslsw2a5iclo/app.bsky.feed.post/3juhirhlz2l24"
              },
              "parent": {
                "cid": "bafyreiex67slrkznmhqfq35fh7f7w3okpidsx7jg23wjxis6ostbdlbvwq",
                "uri": "at://did:plc:oky5czdrnfjpqslsw2a5iclo/app.bsky.feed.post/3juhjkceg4t2m"
              }
            },
            "createdAt": "2023-04-28T21:11:27.006Z"
          },
          "replyCount": 44,
          "repostCount": 98,
          "likeCount": 527,
          "indexedAt": "2023-04-28T21:11:27.229Z",
          "viewer": {},
          "labels": []
        }
      ]
    }
    """
    # atp_endpoint = "/xrpc/com.atproto.server.getSession"
    atp_endpoint = "/xrpc/app.bsky.feed.getPosts"
    uri = "at://{}/app.bsky.feed.post/{}".format(author_id, post_id)
    headers = {"Authorization": "Bearer " + token}

    endpoint_url = build_url(host, atp_endpoint, params={'uris': uri})

    resp = requests.get(
        endpoint_url,
        headers=headers
    )

    return resp



if __name__ == '__main__':
    hello()
