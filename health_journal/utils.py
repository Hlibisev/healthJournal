def change_text_notion(notion, page_id, text):
    """
    Change text in first block of notion page

    Args:
        notion (notion_client.Client): Notion client
        page_id (str): Notion page id
        text (str): New text
    """
    current_blocks = notion.blocks.children.list(block_id=page_id)["results"]

    first_id = current_blocks[0]["id"]
    notion.blocks.update(block_id=first_id, **text_block(text))


def text_block(text):
    """
    Return notion text block
    """
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }
