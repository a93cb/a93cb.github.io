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


def delete_html_file(game_id: str):
    """Deletes the HTML file inside the games/ folder using the game's ID."""
    html_path = os.path.join("games", f"{game_id}.html")

    if os.path.exists(html_path):
        os.remove(html_path)
        print(f"Deleted HTML file: {html_path}")
    else:
        print(f"HTML file not found: {html_path}")


def remove_game_from_xml(game_input: str, xml_filename: str = "games.xml"):
    """
    Removes a game from games.xml by title or slug ID, then removes its HTML file.
    """
    game_id = slugify(game_input)

    if not os.path.exists(xml_filename):
        print(f"XML file '{xml_filename}' does not exist.")
        delete_html_file(game_id)
        return

    tree = ET.parse(xml_filename)
    root = tree.getroot()

    game_to_remove = None

    for game in root.findall("game"):
        id_elem = game.find("id")
        title_elem = game.find("title")

        # Match either exact slug ID or original title
        if (id_elem is not None and id_elem.text == game_id) or (
            title_elem is not None and title_elem.text.lower() == game_input.lower()
        ):
            game_to_remove = game
            break

    if game_to_remove is not None:
        root.remove(game_to_remove)

        # Format and update XML file
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

        print(f"Successfully removed '{game_input}' ({game_id}) from {xml_filename}!")
    else:
        print(f"Game '{game_input}' not found in {xml_filename}.")

    # Delete the corresponding HTML file
    delete_html_file(game_id)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python remove.py "TITLE_OR_ID"')
        sys.exit(1)

    input_target = sys.argv[1]
    remove_game_from_xml(input_target)