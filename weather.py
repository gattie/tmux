import requests
import argparse
import json
import urllib.parse
import sys

API_KEY=""

def weather_icon(weather_category):
    """Get bytecode of emoji based on the weather category

    Arguments:
        weather_category {int} -- Weather category value provided by
        openweathermap API.

    Returns:
        decoded bytecode -- bytecode decoded into it's utf-8 emoji
    """
    if 200 <= weather_category <= 299:
        weather_category = 200
    elif 300 <= weather_category <= 399:
        weather_category = 300
    elif 500 <= weather_category <= 599:
        weather_category = 500
    elif 600 <= weather_category <= 699:
        weather_category = 600
    elif 700 <= weather_category <= 799:
        weather_category = 700

    icons = {
        200: b'\xe2\x9b\x88',             # Thunderstorm
        300: b'\xf0\x9f\x8c\xa6',         # Drizzle
        500: b'\xf0\x9f\x8c\xa7',         # Rain
        600: b'\xf0\x9f\x8c\xa8',         # Snow
        700: b'\xf0\x9f\x92\xa8',         # Atmosphere (Smoke, Haze, Fog, etc.)
        800: b'\xe2\x98\x80\xef\xb8\x8f', # Clear
        801: b'\xe2\x9b\x85',             # Few Clouds
        802: b'\xe2\x9b\x85\xef\xb8\x8f', # Scattered Clouds
        803: b'\xe2\x98\x81\xef\xb8\x8f', # Broken Clouds
        804: b'\xe2\x98\x81\xef\xb8\x8f', # Overcast Clouds
    }

    value = icons.get(weather_category)

    return value

def geocode(address):
    """ Retrieves the latitude and longitude based on the address provided
    {'alt': {},
     'elevation': {},
     'latt': '38.89876',
     'longt': '-77.03512',
     'standard': {'addresst': 'Nw Pennsylvania Ave',
                  'city': 'Washington',
                  'confidence': '1',
                  'countryname': 'United States of America',
                  'postal': '20503',
                  'prov': 'US',
                  'region': 'DC',
                  'stnumber': '1600',
                  'zip': '20503'}}

    Arguments:
        address {string} -- Full street address

    Returns:
        tuple -- City, Latitude, and Longitude
    """
    geo_data = requests.get("https://geocode.xyz/{}?json=1".format(
        urllib.parse.quote_plus(address)))
    geo_json = json.loads(geo_data.content)

    return geo_json['standard']['city'], geo_json['latt'], geo_json['longt']

def get_weather(latitude, longitude, units):
    """ Retrieves the weather based on the latitude and longitude provided.
    {'base': 'stations',
     'clouds': {'all': 20},
     'cod': 200,
     'coord': {'lat': 33.32, 'lon': -111.73},
     'dt': 1583720426,
     'id': 5295903,
     'main': {'feels_like': 16.11,
              'humidity': 40,
              'pressure': 1015,
              'temp': 19.62,
              'temp_max': 21.67,
              'temp_min': 17.22},
     'name': 'Gilbert',
     'sys': {'country': 'US',
             'id': 4553,
             'sunrise': 1583675146,
             'sunset': 1583717374,
             'type': 1},
     'timezone': -25200,
     'visibility': 16093,
     'weather': [{'description': 'few clouds',
                  'icon': '02n',
                  'id': 801,
                  'main': 'Clouds'}],
     'wind': {'deg': 270, 'speed': 3.6}}

    Arguments:
        latitude {[type]} -- [description]
        longitude {[type]} -- [description]
        units {[type]} -- [description]

    Returns:
        tuple -- Weather category, temperature, and wind speed
    """
    global API_KEY
    qs = {
        'lat': latitude,
        'lon': longitude,
        'APPID': API_KEY,
        'units': units
    }
    qs = urllib.parse.urlencode(qs)
    url = "http://api.openweathermap.org/data/2.5/weather?{}".format(qs)
    weather = requests.get(url)
    weather_json = json.loads(weather.content)
    category = weather_json['weather'][0]['id']
    temp = weather_json['main']['temp']
    wind_speed = weather_json['wind']['speed']

    return category, temp, wind_speed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        dest='city',
        help="The display name of the weather location"
    )
    parser.add_argument(
        '-a',
        dest='address',
        help="Look up geocode by street address \
            (e.g. 3400 E Sky Harbor Blvd, Phoenix, AZ 85034)"
    )
    parser.add_argument(
        '-l',
        dest='latitude',
        help="Latitude coordinates of weather location"
    )
    parser.add_argument(
        '-L',
        dest='longitude',
        help="Longitude coordinates of weather location"
    )
    parser.add_argument(
        '-u',
        dest='units',
        choices=['metric', 'imperial'],
        default='metric',
        help="celcius or farenheit"
    )
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    temp_unit = 'C' if args.units == 'metric' else 'F'

    if args.address:
        city, lat, lon = geocode(args.address)
        print("python {} -c {} -l {} -L {}".format(
            parser.prog, city.replace(" ", "\\ "), lat, lon))
    else:
        category, temp, wind_speed = get_weather(
            args.latitude, args.longitude, args.units)
        icon = weather_icon(category)
        # print(icon.decode('utf-8'))
        print("{}:{}  {}°{}, {}ms".format(
            args.city,
            icon.decode('utf-8'),
            round(temp),
            temp_unit,
            round(wind_speed)
        ))

if __name__ == "__main__":
    main()