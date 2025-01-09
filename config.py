import os
from configparser import ConfigParser

config_file = "config.ini"
config = ConfigParser()

# Check if config.ini exists and create one if it doesnt.
if not os.path.exists(config_file):
    with open(config_file, "w") as file:
        file.write("""
[DEFAULT]
TACTICAL_CALL = BBS
STANDARD_CALL = TC2BBS
KISS_HOST = 127.0.0.1
KISS_PORT = 8001
BULLETIN_EXPIRATION_DAYS = 7
APRS_PATH = WIDE1-1,WIDE2-1
""")

config.read(config_file)

TACTICAL_CALL = config.get("DEFAULT", "TACTICAL_CALL", fallback="BBS")
STANDARD_CALL = config.get("DEFAULT", "STANDARD_CALL", fallback="TC2BBS")
KISS_HOST = config.get("DEFAULT", "KISS_HOST", fallback="127.0.0.1")
KISS_PORT = config.getint("DEFAULT", "KISS_PORT", fallback=8001)
BULLETIN_EXPIRATION_DAYS = config.getint("DEFAULT", "BULLETIN_EXPIRATION_DAYS", fallback=7)
APRS_PATH = config.get("DEFAULT", "APRS_PATH", fallback="WIDE1-1").split(",")
RAW_PACKET_DISPLAY = config.getboolean("DEFAULT", "RAW_PACKET_DISPLAY", fallback=False)
