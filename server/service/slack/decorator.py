import json
import os

from flask import make_response, request
from slack_sdk.signature import SignatureVerifier

signature_verifier = SignatureVerifier(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)


def is_signature_valid(request):
    return signature_verifier.is_valid(
        body=request.get_data(),
        timestamp=request.headers.get("X-Slack-Request-Timestamp"),
        signature=request.headers.get("X-Slack-Signature"),
    )


def validate_signature(func):
    def validate_signature_wrapper(*args, **kwargs):
        if not is_signature_valid(request):
            return make_response("invalid request", 403)
        return func(*args, **kwargs)

    return validate_signature_wrapper


def validate_challenge(func):
    def validate_challenge_wrapper(*args, **kwargs):
        payload = request.get_data()
        body = json.loads(payload)

        if body and body.get("challenge"):
            return make_response(body.get("challenge"), 200)
        return func(*args, **kwargs)

    return validate_challenge_wrapper
