import json
import re
from pathlib import Path

import requests


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


def fetch_all_blocks(notion, block_id):
    """
    Change text in first block of notion page

    Args:
        notion (notion_client.Client): Notion client
        page_id (str): Notion block id

    Returns:
        dict: json created from block
    """
    block = notion.blocks.retrieve(block_id=block_id)
    block_data = {"block": block, "children": []}

    if block.get("has_children", False):
        children = notion.blocks.children.list(block_id=block_id)["results"]
        for child in children:
            block_data["children"].append(fetch_all_blocks(notion, child["id"]))

    return block_data


def save_files(page_data, folder=Path("backup")):
    """
    Save files from "url" key of notion page to folder

    Args:
        page_data (dict): Notion page data, which has "url" key
        folder (Path, optional): Folder with backup. Defaults to Path("backup").
    """
    if not isinstance(page_data, (dict, list)):
        return

    if isinstance(page_data, list):
        for child in page_data:
            save_files(child, folder)

        return

    if page_data.get("url", False):
        url = page_data["url"]
        response = requests.get(url)
        file_name = extraxt_mini_hash(url) + "-" + extract_name(url)

        with open(folder / file_name, "wb") as file:
            file.write(response.content)

    for child in page_data.values():
        save_files(child, folder)


def save_page(notion, page_id, folder=Path("backup")):
    """
    Save notion page to folder

    Args:
        notion (notion_client.Client): Notion client
        page_id (str): Notion block id
        folder (Path, optional): Folder with backup. Defaults to Path("backup").
    """
    folder = Path(folder) / page_id
    folder.mkdir(parents=True, exist_ok=True)

    for file in folder.iterdir():
        file.unlink()

    page_data = fetch_all_blocks(notion, page_id)

    with open(folder / "page.json", "w") as file:
        json.dump(page_data, file, indent=2, ensure_ascii=False)

    save_files(page_data, folder)


def extract_name(url):
    match = re.search(r"\/([^\/?]+)\?", url)
    if match:
        filename = match.group(1)
        return filename


def extraxt_mini_hash(url):
    uuid_regex = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    matches = re.findall(uuid_regex, url)

    if matches and len(matches) > 1:
        desired_uuid = matches[1][-5:]
        return desired_uuid
