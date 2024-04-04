
from os import getenv
from json import dumps
from datetime import datetime

from astropy.coordinates import EarthLocation, AltAz, SkyCoord, get_body, AltAz
from astropy.time import Time, TimeDelta
import astropy.units as u
from astropy.coordinates import Angle

from ip_loc import get_ip_location
from ip_loc import IpLookUpError  # export

def BAD_REQ_RES(err, addtional_info=""):
    d = dict(err=str(err),  # get err message
            addtional_info=addtional_info
            )
    
    return dumps(d).encode('ascii')

def to_earth_loc(lat, lon):
    return EarthLocation.from_geodetic(lat=lat, lon=lon)

def deg_float_to_earth_loc(lat: float, lon: float):
    return to_earth_loc(lat = lat * u.deg, lon = lon * u.deg)

def ang_str_to_earch_loc(lat: str, lon: str):

    alat = Angle(lat)
    alon = Angle(lon)

    latitude = alat
    longitude = alon

    location = to_earth_loc(lat=latitude, lon=longitude)
    return location

def _demo_loc():
    return ang_str_to_earch_loc('''40°42′51″ N''', '''74°00′21″ W''')

def get_def_location() -> 'EarthLocation|None':
    slon = getenv('MOONS_OBS_LON')
    slat = getenv('MOONS_OBS_LAT')
    if slon is None or slat is None:
        try:
            lon = float(slon)
            lat = float(slat)
            return deg_float_to_earth_loc(lat=lat, lon=lon)
        except ValueError:
            return ang_str_to_earch_loc(lat=slat, lon=slon)


def get_location(ip: str) -> EarthLocation:
    loc_d = get_ip_location(ip)

    lat = loc_d['lat']
    lon = loc_d['lon']

    location = deg_float_to_earth_loc(lat=lat, lon=lon)
    return location


def norm_off(s):
    'see https://docs.astropy.org/en/stable/api/astropy.time.TimeDeltaQuantityString.html#astropy.time.TimeDeltaQuantityString'
    res = ''
    for c in s:
        if c == 'y':
            res += 'yr'
        elif c == 'h':
            res += 'hr'
        elif c == 'm':
            res += 'min'
        else:
            res += c
    return res

def _(): # no use
    # calc the moon's loc
    moon = SkyCoord.from_name('Moon')

    # equatorial coordinate -> Altazimuth
    alt_az = moon.transform_to(AltAz(obstime=time, location=location))

def get_alt_az(name='moon', time: 'str|Time' = None, off: str = None, lon = None, lat = None, ip = None) -> SkyCoord:
    # obs time (UTC)
    if not name: name = 'moon'
    if time is None: time = Time.now()
    elif isinstance(time, str): time = Time(time)

    if off is not None:
        off = norm_off(off)
        time += TimeDelta(off)


    #Time('2024-04-02 12:00:00')

    moon = get_body(name, time) #, location)

    if lon is not None and lat is not None:
        location = EarthLocation(lon=lon, lat=lat)
    else:
        if ip is not None:
            # XXX: use `try:` to handle error
            location = get_location(ip)
        else:
            location = get_def_location()
            if location is None:
                location = _demo_loc()

    # equatorial coordinate -> Altazimuth
    alt_az = moon.transform_to(AltAz(location=location))

    return alt_az

def jsonify(alt_az) -> str:
    az = alt_az.az.degree  # Azimuth
    alt = alt_az.alt.degree  # Altitude

    d = dict(az=az, alt=alt)
    res = dumps(d)
    return res

def json_alt_az(*arg, **kw) -> bytes:
    return jsonify(get_alt_az(*arg, **kw)).encode()

DEF_CALL = json_alt_az

if __name__ == '__main__':
    res = json_alt_az()
    print(res)


