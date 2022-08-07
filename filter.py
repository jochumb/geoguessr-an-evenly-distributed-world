import requests
from requests.exceptions import HTTPError

api_key = "ADD_KEY_HERE"

def closest_road_coords(lat, lng):
  try: 
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&location_type=ROOFTOP|RANGE_INTERPOLATED|GEOMETRIC_CENTER|APPROXIMATE&result_type=street_address|route|intersection&key={}".format(lat, lng, api_key))
    json = response.json()
    if (json['status'] == "OK"):
      options = []
      for result in json['results']:
        updated_coords = result['geometry']['location']
        options.append((updated_coords['lat'], updated_coords['lng']))
      return options
    else:
      raise ValueError('No road found for {},{} ({})'.format(lat, lng, json['status']))
  except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
    raise ValueError(f'No road found for {lat},{lng}')
  except Exception as err:
    print(f'Other error occurred: {err}')
    raise ValueError(f'No road found for {lat},{lng}')

def has_street_view(options):
  found = False
  i = 0
  while (found == False and i < len(options)):
    (lat, lng) = options[i]
    found = has_street_view_coords(lat, lng)
    if (found):
      return (lat, lng)
    else:
      i = i+1
  
  raise ValueError("No streetview found for any option: {}".format(options))

def has_street_view_coords(lat, lng):
  try: 
    response = requests.get("https://maps.googleapis.com/maps/api/streetview/metadata?location={},{}&key={}".format(lat, lng, api_key))
    json = response.json()
    print(json)
    if (json['status'] == "OK"):
      return True
    else:
      print('Not street view for coords: {},{}, ({})'.format(lat, lng, json['status']))
      return False
  except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')  # Python 3.6
    return False
  except Exception as err:
    print(f'Other error occurred: {err}')  # Python 3.6
    return False



road_coords = []
streetview_coords = []

with open('none.csv') as f:
  coords = [line.rstrip().split(',') for line in f]
  for (lng, lat) in coords:
    try:
      options = closest_road_coords(lat, lng)
      road_coords.append(options)

      (updated_lat, updated_lng) = has_street_view(options)
      streetview_coords.append((updated_lat, updated_lng))

      print(f"Point {lat},{lng} update to: {updated_lat},{updated_lng}, has streetview!")
    except Exception as err:
      print(err)
  
print("")

print("Roads:")
for options in road_coords:
  print(options)

print("")

print("Streetview:")
for (lat, lng) in streetview_coords:
  print(f'{lat},{lng}')
  

