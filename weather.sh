#!/bin/bash
#
# Weather
# =======
#
# By Jezen Thomas <jezen@jezenthomas.com>
# Modifications by Matthew Gaspar
#
# This script sends a couple of requests over the network to retrieve
# approximate location data, and the current weather for that location. This is
# useful if for example you want to display the current weather in your tmux
# status bar.

# There are three things you will need to do before using this script.
#
# 1. Install jq with your package manager of choice (homebrew, apt-get, etc.)
# 2. Sign up for a free account with OpenWeatherMap to grab your API key
# 3. Add your OpenWeatherMap API key where it says API_KEY

# OPENWEATHERMAP API KEY (place yours here)
API_KEY=""

set -e

# Not all icons for weather symbols have been added yet. If the weather
# category is not matched in this case statement, the command output will
# include the category ID. You can add the appropriate emoji as you go along.
#
# Weather data reference: http://openweathermap.org/weather-conditions
weather_icon() {
  if (($1>=200 && $1<=299))
  then
    echo ⛈i
  elif (($1>=300 && $1<=399))
  then
    echo 🌦
  elif (($1>=500 && $1<=599))
  then
    echo 🌧
  elif (($1>=600 && $1<=699))
  then
    echo 🌨
  elif (($1>=700 && $1<=799))
  then
    echo 💨
  elif (($1==800))
  then
    echo ☀️
  elif (($1==801))
  then
    echo 🌤
  elif (($1==802))
  then
    echo 🌥
  elif (($1==803 || $1==804))
  then
    echo ☁️ 
  fi
}

#$ curl -s 'https://geocode.xyz/Tucson,+Arizona?json=1' | jq '.'
#{
#  "standard": {
#    "stnumber": "1045",
#    "addresst": "Arizona Ave S",
#    "postal": {},
#    "region": "AZ",
#    "zip": {},
#    "prov": "US",
#    "city": "Tucson",
#    "countryname": "United States of America",
#    "confidence": "0.7"
#  },
#  "longt": "-110.96761",
#  "alt": {},
#  "elevation": {},
#  "latt": "32.21373"
#}
function geocode() {
  address=$1
  data=$(curl -s "https://geocode.xyz/${address}?json=1")
  echo $data
}


function usage() {
  cat <<EOL
  weather -c [city] -l [latitude] -L [longitude]

  -a [address]   : (optional) A postal address of weather location
  -c [city]      : (required if address isn't provided) The name of the city you want to print for display purposes
  -l [latitude]  : (required if address isn't provided) The latitude in signed degrees format DDD.dddd
  -L [longitude] : (required if address isn't provided) The longitude in signed degrees format DDD.dddd
  -u             : (optional) Units can be either 'metric' or 'imperial' (default: metric)
  -h             : prints this help message

  example: weather -c Lviv -l 49.844146 -L 23.996637
EOL
}

while getopts ":ha:c:l:L:u:" opt; do
  case ${opt} in
    h ) usage
        exit 0
      ;;
    a ) ADDRESS=$OPTARG;;
    c ) CITY=$OPTARG;;
    l ) LAT=$OPTARG;;
    L ) LON=$OPTARG;;
    u ) if [[ "$OPTARG" == "metric" || "$OPTARG" == "imperial" ]]
        then
          UNITS=$OPTARG
        else
          usage
          exit 0
        fi
      ;;
    : ) echo "Arguments must be passed"
        exit 1
      ;;
  esac
done

UNITS=${UNITS:=metric}

if [[ "${UNITS}" == "metric" ]]
then
  LETTER="C"
else
  LETTER="F"
fi

if [[ -n $ADDRESS ]]
then
  echo "Address has been given"
  geocoding=$(geocode "${ADDRESS}")
  echo $geocoding
  CITY=$(echo $geocoding | jq '.standard.city' | tr -d '"')
  REGION=$(echo $geocoding | jq '.standard.region' | tr -d '"')
  CITY=$(echo "${CITY}, ${REGION}")
  LAT=$(echo $geocoding | jq '.latt' | tr -d '"')
  LON=$(echo $geocoding | jq '.longt'| tr -d '"')
fi
echo $LAT
echo $LON
echo $CITY
WEATHER=$(curl --silent http://api.openweathermap.org/data/2.5/weather\?lat="$LAT"\&lon="$LON"\&APPID="$API_KEY"\&units="${UNITS}")

CATEGORY=$(echo "$WEATHER" | jq .weather[0].id)
TEMP="$(echo "$WEATHER" | jq .main.temp | cut -d . -f 1)°${LETTER}"
WIND_SPEED="$(echo "$WEATHER" | jq .wind.speed | awk '{print int($1+0.5)}')ms"
ICON=$(weather_icon "$CATEGORY")

printf "%s" "$CITY:$ICON  $TEMP, $WIND_SPEED"

