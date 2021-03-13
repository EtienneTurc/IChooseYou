import os

from slack_sdk.signature import SignatureVerifier

signature_verifier = SignatureVerifier(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)


# Verify incoming requests from Slack
# https://api.slack.com/authentication/verifying-requests-from-slack
def slack_signature_valid(request):
    return signature_verifier.is_valid(
        body=request.get_data(),
        timestamp=request.headers.get("X-Slack-Request-Timestamp"),
        signature=request.headers.get("X-Slack-Signature"),
    )
