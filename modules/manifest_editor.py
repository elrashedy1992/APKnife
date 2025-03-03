import curses
import os
import tempfile
import xml.etree.ElementTree as ET
import zipfile

from androguard.core.axml import AXMLPrinter


def extract_manifest_from_apk(apk_path, output_dir):
    """Extracts AndroidManifest.xml from an APK file."""
    with zipfile.ZipFile(apk_path, "r") as zip_ref:
        if "AndroidManifest.xml" in zip_ref.namelist():
            zip_ref.extract("AndroidManifest.xml", output_dir)
            return os.path.join(output_dir, "AndroidManifest.xml")
        else:
            raise FileNotFoundError("AndroidManifest.xml is missing inside the APK.")


def decode_binary_xml(binary_xml_path):
    """Converts AndroidManifest.xml from binary (AXML) to readable XML."""
    with open(binary_xml_path, "rb") as f:
        binary_xml = f.read()
    axml = AXMLPrinter(binary_xml)
    xml_data = axml.get_xml()

    if xml_data is None:
        raise ValueError("Failed to decode AXML. The file may be corrupted.")

    return xml_data.decode("utf-8")


def save_backup(original_path):
    """Creates a backup of the original APK before modification."""
    backup_path = original_path + ".backup"
    if not os.path.exists(backup_path):
        os.rename(original_path, backup_path)
    return backup_path


def encode_binary_xml(xml_str, output_path):
    """Converts readable XML back to AXML format."""
    with open(output_path, "wb") as f:
        f.write(xml_str.encode("utf-8"))


def update_apk_with_manifest(apk_path, manifest_path):
    """Updates an APK with the modified AndroidManifest.xml."""
    backup_path = save_backup(apk_path)

    with zipfile.ZipFile(backup_path, "r") as zip_ref:
        zip_ref.extractall("temp_apk")

    with zipfile.ZipFile(apk_path, "w") as zip_ref:
        for root, _, files in os.walk("temp_apk"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "temp_apk")
                zip_ref.write(file_path, arcname)

    print("✅ APK successfully updated!")


def start_editor(stdscr, manifest_path):
    """A curses-based editor for modifying AndroidManifest.xml."""
    try:
        curses.curs_set(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

        stdscr.clear()
        stdscr.refresh()

        with open(manifest_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        cursor_x, cursor_y = 0, 0
        max_y, max_x = stdscr.getmaxyx()

        instructions = "↑↓←→ Move - ENTER New Line - BACKSPACE Delete - S Save - Q Exit"

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, instructions, curses.A_BOLD)

            for i, line in enumerate(lines[: max_y - 2]):
                stdscr.addstr(i + 1, 0, line[: max_x - 1])

            stdscr.move(cursor_y + 1, cursor_x)
            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and cursor_y > 0:
                cursor_y -= 1
            elif key == curses.KEY_DOWN and cursor_y < len(lines) - 1:
                cursor_y += 1
            elif key == curses.KEY_LEFT and cursor_x > 0:
                cursor_x -= 1
            elif key == curses.KEY_RIGHT and cursor_x < len(lines[cursor_y]) - 1:
                cursor_x += 1
            elif key == ord("\n"):
                lines.insert(cursor_y + 1, "\n")
                cursor_y += 1
                cursor_x = 0
            elif key == 127 or key == curses.KEY_BACKSPACE:
                if cursor_x > 0:
                    lines[cursor_y] = (
                        lines[cursor_y][: cursor_x - 1] + lines[cursor_y][cursor_x:]
                    )
                    cursor_x -= 1
                elif cursor_y > 0:
                    lines[cursor_y - 1] += lines[cursor_y]
                    del lines[cursor_y]
                    cursor_y -= 1
                    cursor_x = len(lines[cursor_y])
            elif key == ord("s"):
                try:
                    with open(manifest_path, "w", encoding="utf-8") as f:
                        f.writelines(lines)
                    stdscr.addstr(
                        max_y - 1, 0, "✅ Changes saved! Press any key to continue."
                    )
                    stdscr.refresh()
                    stdscr.getch()
                except Exception as e:
                    stdscr.addstr(
                        max_y - 1, 0, f"❌ Save error: {e}", curses.color_pair(1)
                    )
                    stdscr.refresh()
                    stdscr.getch()
            elif key == ord("q"):
                break
            elif 32 <= key <= 126:
                lines[cursor_y] = (
                    lines[cursor_y][:cursor_x] + chr(key) + lines[cursor_y][cursor_x:]
                )
                cursor_x += 1
    except Exception as e:
        stdscr.addstr(max_y - 1, 0, f"❌ Error: {e}", curses.color_pair(1))
        stdscr.refresh()
        stdscr.getch()


def edit_manifest(file_path):
    """Edits AndroidManifest.xml inside an APK or a decompiled app folder."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            if file_path.endswith(".apk"):
                # Extract manifest from APK
                manifest_path = extract_manifest_from_apk(file_path, temp_dir)
                print("✅ Extracted AndroidManifest.xml successfully.")

                # Decode AXML
                decoded_xml = decode_binary_xml(manifest_path)
                decoded_xml_path = os.path.join(temp_dir, "decoded_AndroidManifest.xml")

                with open(decoded_xml_path, "w", encoding="utf-8") as f:
                    f.write(decoded_xml)
                print("✅ Converted AndroidManifest.xml to readable text.")

            else:
                # If it's a folder, assume the manifest is already extracted
                manifest_path = os.path.join(file_path, "AndroidManifest.xml")
                if not os.path.exists(manifest_path):
                    raise FileNotFoundError(
                        "AndroidManifest.xml not found in the given folder."
                    )

                decoded_xml_path = manifest_path  # Directly edit it

            # Open editor
            curses.wrapper(lambda stdscr: start_editor(stdscr, decoded_xml_path))

            # Read modified XML
            with open(decoded_xml_path, "r", encoding="utf-8") as f:
                modified_xml = f.read()

            # Convert back to AXML
            encoded_xml_path = os.path.join(temp_dir, "encoded_AndroidManifest.xml")
            encode_binary_xml(modified_xml, encoded_xml_path)
            print("✅ Converted AndroidManifest.xml back to AXML successfully.")

            # If it's an APK, update it
            if file_path.endswith(".apk"):
                update_apk_with_manifest(file_path, encoded_xml_path)
                print("✅ Updated APK with modified AndroidManifest.xml.")

        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


# Example Usage:
# edit_manifest("/path/to/app.apk")   -> Modify APK Manifest
# edit_manifest("/path/to/decompiled_app/") -> Modify extracted manifest
