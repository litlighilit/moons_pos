# Moons Location Getter

A combination of the moons position calcuator and a simple server.

## usage

GET `/`  -> `/moon`

GET `/{moon_name}`


### responce
MIME: `applcation/json`

#### success
status: `200`

returns
a object with key `az` and `alt`, meaning `Azimuth` and `Altitude`, in degrees, as float.

e.g.
```JSON
{
    "az": 254.59860152121138,
    "alt": -16.783285968098898
}
```
it means this moon is downside the horizon.

#### fail

status: `400`

```JSON
{
    "err": msg,
    "additional_info": msg
}
```

where `msg` is a string. For `additional_info`, it's maybe empty

e.g. when getting request from a local private ip, when `lon` and `lat` is not given, then it fails with:
```JSON
{
    "err": "reserved range",
    "addtional_info": "ip-loc look-up failed"
}
```

### query params
> All is optional

- lat: float/str, in degrees. latitude of obsolution point. If as str, See [`astropy.coordinates.Angle` doc][] for formats.
- lon: float/str, in degrees. longitude of obsolution point. If as str, See [`astropy.coordinates.Angle` doc][] for formats.
- time: str, e.g. `2000-01-01 00:00:00.000` (*NOTE*: this's UTC time). see [`astropy.time.Time` doc](https://docs.astropy.org/en/stable/time/index.html#time-format) for formats
- off: str. combination of digits and one-alpha unit, where `h` is hour, `m` is `min`, `s` is `second`...

[`astropy.coordinates.Angle` doc]: https://docs.astropy.org/en/stable/api/astropy.coordinates.Angle.html


## env

### `MOONS_SRV_PORT`
the server port (default: 3333)

### `MOONS_OBS_LAT` and `MOONS_OBS_LON`
latitude of obsolution point
longitude of obsolution point

used when `lat` and `lon` params are not given in URL.

