import os
import re
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom


def slugify(title: str) -> str:
    """Converts a title into a lowercase dash-separated ID (e.g., 'Crossy Road!' -> 'crossy-road')."""
    text = title.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)  # Remove special characters
    text = re.sub(r"[\s_]+", "-", text)  # Replace spaces and underscores with hyphens
    return re.sub(r"-+", "-", text)  # Remove redundant hyphens


def create_html_file(game_id: str, title: str):
    """Creates an HTML file inside the games/ folder using the game's ID."""
    games_dir = "games"
    os.makedirs(games_dir, exist_ok=True)  # Create 'games' folder if it doesn't exist

    html_path = os.path.join(games_dir, f"{game_id}.html")

    if os.path.exists(html_path):
        print(f"HTML file already exists: {html_path}")
        return

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <p>Welcome to {title}!</p>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"Created HTML file: {html_path}")


def add_game_to_xml(title: str, xml_filename: str = "games.xml"):
    game_id = slugify(title)
    path = f"/games/{game_id}.html"

    # Load existing XML or create a new root element
    if os.path.exists(xml_filename):
        tree = ET.parse(xml_filename)
        root = tree.getroot()
    else:
        root = ET.Element("games")

    # Check if game ID already exists in XML
    game_exists = False
    for existing_game in root.findall("game"):
        existing_id = existing_game.find("id")
        if existing_id is not None and existing_id.text == game_id:
            print(f"Game with ID '{game_id}' already exists in {xml_filename}.")
            game_exists = True
            break

    if not game_exists:
        # Create new <game> XML structure
        new_game = ET.SubElement(root, "game")

        id_elem = ET.SubElement(new_game, "id")
        id_elem.text = game_id

        title_elem = ET.SubElement(new_game, "title")
        title_elem.text = title

        path_elem = ET.SubElement(new_game, "path")
        path_elem.text = path

        # Format and write to XML file
        rough_string = ET.tostring(root, encoding="utf-8")
        parsed_xml = minidom.parseString(rough_string)

        pretty_xml = "\n".join(
            [
                line
                for line in parsed_xml.toprettyxml(indent="  ").splitlines()
                if line.strip()
            ]
        )

        with open(xml_filename, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

        print(f"Successfully added '{title}' ({game_id}) to {xml_filename}!")

    # Create the corresponding HTML file
    create_html_file(game_id, title)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python add.py "TITLE"')
        sys.exit(1)

    title_input = sys.argv[1]
    add_game_to_xml(title_input)