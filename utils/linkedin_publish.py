# utils/linkedin_publish.py
"""
Stub: publishing to LinkedIn requires OAuth2.0 flow and access token with w_member_social scope.
This module is a placeholder. Use this high-level flow:

1) Direct the user to LinkedIn OAuth URL to grant permissions.
2) Exchange authorization code for access token.
3) Use POST https://api.linkedin.com/v2/ugcPosts with required JSON payload.

I am not including a full LinkedIn OAuth implementation here because it requires
redirect URIs and app setup. If you'd like, I can add a full FastAPI OAuth flow later.

Below is a helper to POST once you have an access token.

"""

import requests

def publish_to_linkedin(access_token, author_urn, text, visibility="PUBLIC"):
    """
    access_token: LinkedIn OAuth token with w_member_social
    author_urn: "urn:li:person:XXXXXXXX" (from LinkedIn profile)
    text: the post content (string)
    """
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility}
    }
    resp = requests.post(url, headers=headers, json=payload)
    return resp.status_code, resp.text
