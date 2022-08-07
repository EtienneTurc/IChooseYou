import io
import json
from contextlib import redirect_stdout


def call_webhook(
    client,
    user_id="4321",
    text="1234",
    callback_id=None,
    action_id=None,
    action_value=None,
    action_block_id=None,
    type=None,
    inputs=None,
    view_state_inputs=None,
    view_metadata=None,
):
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            response = client.post(
                "/interactivity",
                data=mock_slack_api_data(
                    text=text,
                    user_id=user_id,
                    callback_id=callback_id,
                    action_id=action_id,
                    action_value=action_value,
                    action_block_id=action_block_id,
                    type=type,
                    inputs=inputs,
                    view_state_inputs=view_state_inputs,
                    view_metadata=view_metadata,
                ),
                follow_redirects=True,
            )
    except Exception as err:
        print(f.getvalue())
        raise (err)

    slack_message = f.getvalue()
    return response, slack_message


def mock_slack_api_data(
    team_id="1337",
    channel_id="1234",
    channel_name="youplaboom",
    user_id="4321",
    user_name="patoche",
    text="1234",
    ts="1624201203.000200",
    response_url="https://whatever.com",
    trigger_id="1234",
    workflow_step_edit_id="1234",
    inputs=None,
    callback_id=None,
    action_id=None,
    action_value=None,
    action_block_id=None,
    type=None,
    view_state_inputs=None,
    view_metadata=None,
):
    payload = {
        "team": {"id": team_id},
        "user": {"id": user_id, "name": user_name},
        "channel": {"id": channel_id, "name": channel_name},
        "message": {"text": text, "ts": ts},
        "actions": [{"value": text}],
        "response_url": response_url,
        "trigger_id": trigger_id,
        "workflow_step": {"workflow_step_edit_id": workflow_step_edit_id},
    }
    if callback_id:
        payload["callback_id"] = callback_id
    if action_id:
        payload["actions"][0]["action_id"] = action_id
    if action_value:
        payload["actions"][0]["value"] = action_value
        payload["actions"][0]["selected_option"] = {"value": action_value}
    if action_block_id:
        payload["actions"][0]["block_id"] = action_block_id
    if type:
        payload["type"] = type
    if inputs:
        payload["workflow_step"]["inputs"] = inputs
    if view_state_inputs or view_metadata:
        payload["view"] = {}
        if view_state_inputs:
            payload["view"]["state"] = {"values": view_state_inputs}
        if view_metadata:
            payload["view"]["private_metadata"] = json.dumps(view_metadata)

    return {"payload": json.dumps(payload)}
