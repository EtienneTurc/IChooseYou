from server.blueprint.event.mapping import BLUEPRINT_EVENT_ACTION_TO_DATA_FLOW
from server.blueprint.interactivity.mapping import (
    BLUEPRINT_INTERACTIVITY_ACTION_TO_DATA_FLOW,
)
from server.blueprint.slash_command.mapping import (
    BLUEPRINT_SLASH_COMMAND_ACTION_TO_DATA_FLOW,
)


BLUEPRINT_ACTION_TO_DATA_FLOW = {
    **BLUEPRINT_SLASH_COMMAND_ACTION_TO_DATA_FLOW,
    **BLUEPRINT_INTERACTIVITY_ACTION_TO_DATA_FLOW,
    **BLUEPRINT_EVENT_ACTION_TO_DATA_FLOW,
}
