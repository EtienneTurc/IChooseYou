import os

from flask import make_response
from slack_sdk.signature import SignatureVerifier

signature_verifier = SignatureVerifier(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)


# Verify incoming requests from Slack
# https://api.slack.com/authentication/verifying-requests-from-slack
def check_incoming_request_is_valid(request):
    if not signature_verifier.is_valid(
        body=request.get_data(),
        timestamp=request.headers.get("X-Slack-Request-Timestamp"),
        signature=request.headers.get("X-Slack-Signature"),
    ):
        return make_response("invalid request", 403)
