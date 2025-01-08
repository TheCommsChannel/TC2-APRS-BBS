import time
from threading import Lock

import aprs
import os
import json
import requests

import commands
import config

# Global dictionary to track unacknowledged messages
unacknowledged_messages = {}
unack_lock = Lock()

# Message numbering for ACKS
message_counter = 1

from datetime import datetime

JSON_URL = "https://aprs-deviceid.aprsfoundation.org/tocalls.pretty.json"

def fetch_device_data():
    local_file = "tocalls_cache.json"

    if os.path.exists(local_file):
        try:
            if time.time() - os.path.getmtime(local_file) > 7 * 24 * 60 * 60: # Check if the JSON is older than 7 days
                print("Cache is outdated. Refreshing...")
                raise Exception("Cache expired")

            with open(local_file, "r") as file:
                print("Loading device data from cache...")
                return json.load(file)
        except Exception as e:
            print(f"Error with cache: {e}")

    print("Fetching device data online...")
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data = response.json()

        with open(local_file, "w") as file:
            json.dump(data, file, indent=4)
        return data
    except Exception as e:
        print(f"Error fetching device data: {e}")
        return {}


def get_device_info(destination, device_data):
    tocalls = device_data.get("tocalls", {})
    for pattern, info in tocalls.items():
        if pattern.replace("?", "") in destination:
            model = info.get("model", "Unknown Model")
            vendor = info.get("vendor", "Unknown Vendor")
            device_class = info.get("class", "Unknown Class")
            return f"{vendor} {model}, {device_class.capitalize()}"
    return "Unknown Device Type"


def send_ack(ki, aprs_frame):
    try:
        source_callsign = aprs_frame.source.callsign.decode('utf-8') if isinstance(aprs_frame.source.callsign,
                                                                                   bytes) else aprs_frame.source.callsign
        source_ssid = aprs_frame.source.ssid
        source = f"{source_callsign}-{source_ssid}" if source_ssid else source_callsign

        message_number = aprs_frame.info.number.decode('utf-8') if isinstance(aprs_frame.info.number, bytes) else str(
            aprs_frame.info.number)

        ack_info = f":{source:<9}:ack{message_number}".encode('utf-8')

        frame = aprs.APRSFrame.ui(
            destination=source,
            source=config.MYCALL,
            path=config.APRS_PATH,
            info=ack_info,
        )
        ki.write(frame)
    except Exception as e:
        print(f"Failed to send ACK: {e}")


def send_bulletin(bulletin_id, bulletin_text):
    """Send an APRS bulletin in BLN format."""
    try:
        frame_info = f":{bulletin_id:<9}:{bulletin_text}".encode('utf-8')

        frame = aprs.APRSFrame.ui(
            destination="BLN",
            source=config.MYCALL,
            path=config.APRS_PATH,
            info=frame_info
        )

        ki = aprs.TCPKISS(host=config.KISS_HOST, port=config.KISS_PORT)
        ki.start()
        ki.write(frame)
        print(f"Urgent bulletin transmitted: {bulletin_text}")
        ki.stop()

    except Exception as e:
        print(f"Failed to send urgent bulletin: {e}")


def start():
    ki = aprs.TCPKISS(host=config.KISS_HOST, port=config.KISS_PORT)
    ki.start()

    device_data = fetch_device_data()

    print("Listening for APRS frames...\n")

    COLOR_SEPARATOR = "\033[96m"  # Cyan
    COLOR_TIMESTAMP = "\033[92m"  # Green
    COLOR_MESSAGE = "\033[94m"    # Blue
    COLOR_DEVICE = "\033[93m"     # Yellow
    COLOR_RAW = "\033[91m"        # Bright Red
    COLOR_RESET = "\033[0m"       # Reset to Default

    separator_line = f"{COLOR_SEPARATOR}{'=' * 110}{COLOR_RESET}"
    sub_separator_line = f"{COLOR_SEPARATOR}{'-' * 110}{COLOR_RESET}"

    def normalize_callsign(callsign):
        return callsign.split('-')[0].upper() if callsign else ""

    my_callsign = normalize_callsign(config.MYCALL)
    print(f"BBS Callsign: {my_callsign}")

    while True:
        for frame in ki.read(min_frames=1):
            try:
                if config.RAW_PACKET_DISPLAY:
                    print(f"{COLOR_RAW}RAW PACKET:{COLOR_RESET} {frame}")

                aprs_frame = aprs.APRSFrame.from_bytes(bytes(frame))

                if isinstance(aprs_frame.info, aprs.Message):
                    message_text = aprs_frame.info.text.decode('utf-8') if isinstance(aprs_frame.info.text,
                                                                                      bytes) else aprs_frame.info.text

                    if message_text.startswith("ack"):
                        ack_number = message_text[3:].strip()  # Extract the message number after "ack"

                        # Ensure ACK is intended for this BBS
                        recipient = aprs_frame.info.addressee.decode('utf-8').strip() if isinstance(
                            aprs_frame.info.addressee, bytes) else aprs_frame.info.addressee.strip()
                        if normalize_callsign(recipient) != my_callsign:
                            continue

                        with unack_lock:
                            for tracked_recipient, (msg, msg_num) in unacknowledged_messages.items():
                                if str(msg_num) == ack_number:
                                    print(
                                        f"ACK received for {tracked_recipient}'s message #{msg_num}. Removing from tracking.")
                                    del unacknowledged_messages[tracked_recipient]
                        continue

                if isinstance(aprs_frame.info, aprs.Message):
                    recipient = aprs_frame.info.addressee.decode('utf-8') if isinstance(aprs_frame.info.addressee, bytes) else aprs_frame.info.addressee
                    recipient = recipient.strip()
                    # print(f"DEBUG: Extracted recipient from addressee: {recipient}")

                    normalized_recipient = normalize_callsign(recipient)
                    # print(f"DEBUG: Normalized recipient: {normalized_recipient}, My callsign: {my_callsign}")

                    if normalized_recipient != my_callsign:
                        continue

                    source_callsign = aprs_frame.source.callsign.decode('utf-8') if isinstance(aprs_frame.source.callsign, bytes) else aprs_frame.source.callsign
                    source_ssid = aprs_frame.source.ssid
                    source = normalize_callsign(f"{source_callsign}-{source_ssid}")

                    message = aprs_frame.info.text.decode('utf-8') if isinstance(aprs_frame.info.text, bytes) else aprs_frame.info.text

                    send_ack(ki, aprs_frame)

                    destination = aprs_frame.destination.callsign.decode('utf-8') if isinstance(aprs_frame.destination.callsign, bytes) else str(aprs_frame.destination.callsign)
                    device_info = get_device_info(destination, device_data)

                    iso_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    print(separator_line)
                    print(f"{COLOR_TIMESTAMP}{iso_timestamp}{COLOR_RESET} {COLOR_MESSAGE}Message from {source}: {message}{COLOR_RESET}")
                    print(f"{COLOR_DEVICE}({device_info}){COLOR_RESET}")
                    print(sub_separator_line)

                    responses = commands.handle_command(source, message)

                    if isinstance(responses, str):
                        responses = [responses]

                    for response in responses:
                        dec_timestamp = datetime.now().strftime("%b%d %H:%M")

                        response_info = f":{source:<9}:{response}".encode('utf-8')
                        response_frame = aprs.APRSFrame.ui(
                            destination=source,
                            source=config.MYCALL,
                            path=config.APRS_PATH,
                            info=response_info,
                        )
                        ki.write(response_frame)

                        print(f"{COLOR_TIMESTAMP}{iso_timestamp}{COLOR_RESET} Response to {source}: {response}")

                    print(separator_line, "\n")

            except Exception as e:
                print(f"Error processing frame: {e}")

def send_direct_message(recipient, message):
    """Send a direct APRS message to a recipient without ACK request."""
    try:
        frame_info = f":{recipient:<9}:{message}".encode('utf-8')

        frame = aprs.APRSFrame.ui(
            destination=recipient.upper(),
            source=config.MYCALL,
            path=config.APRS_PATH,
            info=frame_info
        )
        ki = aprs.TCPKISS(host=config.KISS_HOST, port=config.KISS_PORT)
        ki.start()
        ki.write(frame)
        print(f"Direct message sent to {recipient}: {message}")
        ki.stop()

    except Exception as e:
        print(f"Failed to send direct message to {recipient}: {e}")


def wait_for_ack(ki, recipient, message_number, timeout=5):
    """Wait for an acknowledgment from the recipient."""
    try:
        start_time = time.time()

        while time.time() - start_time < timeout:
            for frame in ki.read(min_frames=1):
                aprs_frame = aprs.APRSFrame.from_bytes(bytes(frame))

                if isinstance(aprs_frame.info, aprs.Message):
                    message_text = aprs_frame.info.text.decode('utf-8') if isinstance(aprs_frame.info.text, bytes) else aprs_frame.info.text

                    if message_text.startswith("ack"):
                        ack_number = message_text[3:].strip()
                        if ack_number == str(message_number):
                            print(f"ACK received from {recipient} for message #{message_number}.")
                            return True
        print(f"Timeout reached: No ACK received from {recipient} for message #{message_number}.")
        return False

    except Exception as e:
        print(f"Error while waiting for ACK: {e}")
        return False
