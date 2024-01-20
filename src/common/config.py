from src.common.types import *
import os

# Storage configuration information
LOCAL_STORAGE_PATH = "./data"

# AWS Setup information
AWS_ACCESS_KEY_ID = os.environ.get("ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("SECRET_KEY")
# Only needed for temp creds.  TODO
AWS_SESSION_TOKEN = os.environ.get("SESSION_TOKEN")

# NOAA information
SAT_INFO: SatInfoList = [
    ("NOAA15", "25338U"),
    ("NOAA18", "28654U"),
    ("NOAA19", "33591U")
]

# Ground station location constants
LOCATION = "Bath, PA"
LATITUDE_DEG = 40.74
LONGITUDE_DEG = -75.31
ELEVATION_METERS = 0
TIMEZONE = "America/New_York"

# Celestrak info
CELESTRAK_API_ENDPOINT = "https://celestrak.org/NORAD/elements/gp.php"

# SDR Setup
SDR_DEVICE = ""
