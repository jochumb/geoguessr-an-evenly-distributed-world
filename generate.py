import math
import countries
from global_land_mask import globe

earth_radius = 6378137.0 #in meters

cc = countries.CountryChecker('TM_WORLD_BORDERS-0.3.shp')

covered_countries = [
  'AD','AE','AL','AQ','AR','AS','AT','AU','AX',
  'BD','BE','BG','BM','BO','BR','BT','BW',
  'CA','CC','CH','CL','CO','CW','CX','CZ',
  'DE','DK','DO','EC','EE','ES','FI','FK','FO','FR',
  'GB','GH','GI','GL','GR','GS','HK','HR','HU',
  'ID','IE','IL','IM','IN','IO','IS','IT',
  'JE','JO','JP','KE','KG','KH','KR',
  'LA','LI','LK','LS','LT','LU','LV',
  'MC','ME','MG','MK','MN','MO','MP','MT','MX','MY',
  'NG','NL','NO','NZ',
  'PE','PH','PL','PM','PN','PR','PS','PT',
  'RE','RO','RS','RU',
  'SE','SG','SI','SJ','SK','SM','SN','SZ',
  'TH','TN','TR','TW','UA','UG','UM','US','UY',
  'VI','VN','ZA'
]

def fibonacci_sphere(samples=1000):
    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius = math.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius
        z = math.sin(theta) * radius

        points.append((x, y, z))

    return points

def points_to_ecef(points):
  return [(x * earth_radius, y * earth_radius, z * earth_radius) for (x, y, z) in points]

def ecef_to_geodetic(ecef_coords):
  geodetic_coords = []

  a = earth_radius #in meters
  b = 6356752.314245 #in meters
  f = (a - b) / a
  f_inv = 1.0 / f

  e_sq = f * (2 - f)                       
  eps = e_sq / (1.0 - e_sq)

  for (x, y, z) in ecef_coords:
    p = math.sqrt(x * x + y * y)
    q = math.atan2((z * a), (p * b))

    sin_q = math.sin(q)
    cos_q = math.cos(q)

    sin_q_3 = sin_q * sin_q * sin_q
    cos_q_3 = cos_q * cos_q * cos_q

    phi = math.atan2((z + eps * b * sin_q_3), (p - e_sq * a * cos_q_3))
    lam = math.atan2(y, x)

    v = a / math.sqrt(1.0 - e_sq * math.sin(phi) * math.sin(phi))
    h   = (p / math.cos(phi)) - v

    lat = math.degrees(phi)
    lon = math.degrees(lam)

    geodetic_coords.append((lat,lon))
  
  return geodetic_coords

def remove_water_coords(coords):
  land_coords = []
  for (lat,lon) in coords:
    if (globe.is_land(lat, lon)):
      land_coords.append((lat,lon))
  return land_coords

def remove_no_converage_coords(coords):
  coverage_coords = []
  for (lat,lon) in coords:
    country = cc.getCountry(countries.Point(lat, lon))
    if (country != None):
      code = country.iso
      if (code in covered_countries):
        coverage_coords.append((lat,lon))
      # else:
      #   print(f'No coverage for {lat},{lon} in country: {code}')
  return coverage_coords

points = fibonacci_sphere(100000)
ecef = points_to_ecef(points)
coords = ecef_to_geodetic(ecef)
land_coords = remove_water_coords(coords)
coverage_coords = remove_no_converage_coords(land_coords)

for lat, lon in coverage_coords:
  print("{},{}".format(lon, lat))