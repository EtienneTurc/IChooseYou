from server.tests.helper import match_object


def assert_modal_has_expected_block(modal, expected_block):
    blocks = modal["blocks"]
    expected_block_id = expected_block["block_id"]
    blocks_ids = [
        block.get("block_id") if block.get("block_id") else None for block in blocks
    ]
    assert expected_block_id in blocks_ids

    block = blocks[blocks_ids.index(expected_block_id)]
    match_object(block, expected_block)
