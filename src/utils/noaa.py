"""
Helpful terms - https://www.nlsa.com/definitions/aos_defined.html
- AOS stands for Acquisition of Signal (or Satellite). AOS is the time that a satellite rises above the horizon of an observer.
- TCA stands for Time of Closest Approach. This is the time when the satellite is closest to the observer and when Doppler shift is zero. This usually corresponds to the time that the satellite reaches maximum elevation above the horizon.
- LOS stands for Loss of Signal (or Satellite). LOS is the time that a satellite passes below the observer’s horizon.

Pass information - https://www.n2yo.com/passes/?s=28654#
Above can be used to double check below.  Library seems to match pretty closely to n2yo.
"""
import httpx
from passpredict.caches import BaseCache
from src.common.config import SAT_INFO, CELESTRAK_API_ENDPOINT, LOCATION, LATITUDE_DEG, LONGITUDE_DEG, ELEVATION_METERS, TIMEZONE
from src.common.types import PassMap
import datetime
from zoneinfo import ZoneInfo
from passpredict import CelestrakTLESource, Location, SGP4Propagator, Observer, TLE
import logging
import predict
import json


class CelestrakTLESourceFixed(CelestrakTLESource):
    '''
    This is a class that fixes the URL issue present in the original library.
    This overriden class can be fixed once the library gets patched.

    https://pypi.org/project/passpredict/
    '''

    def __init__(self, cache: BaseCache = None) -> None:
        super().__init__(cache)

    def _query_tle_from_celestrak(self, satid: int = None) -> TLE:
        # Need to override the URL here to fix the API.
        url = CELESTRAK_API_ENDPOINT
        params = {
            'CATNR': satid,
            'FORMAT': 'TLE',
        }
        r = httpx.get(url, params=params)
        if r.text.lower() in ("no tle found", "no gp data found") or r.status_code >= 300:
            raise Exception(f'Celestrak TLE for satellite {satid} not found')
        tle_strings = r.text.splitlines()
        tle = self.parse_tle(tle_strings)
        return tle

    def parse_tle(self, tle_lines) -> TLE:
        """
        Parse a single 2-line or 3-line TLE from celestrak
        """
        if len(tle_lines) == 2:
            tle1, tle2 = tle_lines
            name = ""
        elif len(tle_lines) == 3:
            tle0, tle1, tle2 = tle_lines
            name = tle0.strip()  # satellite name
        else:
            raise Exception(f"Invalid TLE strings {tle_lines}")
        satid = int(tle1[2:7])
        tle = TLE(satid, (tle1, tle2), name=name)
        return tle


def fetch_local_pass_times(debug=True) -> PassMap:
    pass_info: PassMap = {}
    for sat in SAT_INFO:
        location = Location(LOCATION, LATITUDE_DEG,
                            LONGITUDE_DEG, ELEVATION_METERS)
        date_start = datetime.datetime.now(tz=ZoneInfo(TIMEZONE))
        date_end = date_start + datetime.timedelta(days=1)
        source = CelestrakTLESourceFixed()
        tle = source.get_tle(satid=int(sat[1].strip("U")))
        satellite = SGP4Propagator.from_tle(tle)
        observer = Observer(location, satellite)
        passes = observer.pass_list(
            date_start, limit_date=date_end, visible_only=False)
        if debug:
            logging.debug("#" * 30)
            logging.debug(sat)
            for sat_pass in passes:
                logging.debug(str(sat_pass.__dict__) + "\n")
        pass_info[sat] = passes
    return pass_info


def fetch_local_pass_times_V2(debug=True):
    # TODO: Determine why the times on this one are really off compared to the original
    for sat in SAT_INFO:
        location = Location(LOCATION, LATITUDE_DEG,
                            LONGITUDE_DEG, ELEVATION_METERS)
        date_start = datetime.datetime.now(tz=ZoneInfo(TIMEZONE))
        date_end = date_start + datetime.timedelta(days=1)
        source = CelestrakTLESourceFixed()
        tle = source.get_tle(satid=int(sat[1].strip("U")))
        tle_text = sat[0] + "\n" + tle.lines[0] + "\n" + tle.lines[1]
        logging.debug(tle_text)
        predictions = predict.transits(tle_text, (location.lat, location.lon, location.h), int(
            date_start.timestamp()), int(date_end.timestamp()))
        if debug:
            logging.debug("#" * 30)
            logging.debug(location.lat)
            logging.debug(location.lon)
            logging.debug(location.h)
            logging.debug(date_start.timestamp())
            logging.debug(sat)
            for transit in predictions:
                logging.debug(json.dumps(transit.__dict__,
                                         sort_keys=True, indent=4,
                                         default=lambda o: f"<<non-serializable: {type(o).__qualname__}>>")
                              + "\n")
