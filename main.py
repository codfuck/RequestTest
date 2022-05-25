from requests import get
import json

def convert_degree(in_degree):
	# function to convert numeric value of wind direction into direction
	segment = in_degree // 45
	left = in_degree % 45
	if left > 22.5:
		segment += 1
	if segment == 8:
		segment = 0
	directions = ['North', 'North-West', 'West', 'South-West', 'South', 'South-East', 'East', 'North-East']
	return directions[segment]

# getting current ip address
ip_response = get('https://api.myip.com').text
ip = json.loads(ip_response)['ip']

# getting name and location of our ip address
location_response = json.loads(get(f'http://ip-api.com/json/{ip}').text)

lat = location_response['lat']
lon = location_response['lon']
country = location_response['country']
city = location_response['city']

# getting current weather at our location
weather_response = json.loads(get(f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}',
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"}).text)


# collecting measure units wind_speed, degrees and pressure
ws_units = weather_response['properties']['meta']['units']['wind_speed']
pressure_units = weather_response['properties']['meta']['units']['air_pressure_at_sea_level']
if weather_response['properties']['meta']['units']['air_temperature'] == 'celsius':
	temp_units = '°C'
else:
	temp_units = '°F'


# collecting weather conditions
pressure = weather_response['properties']['timeseries'][0]['data']['instant']['details']['air_pressure_at_sea_level']
temperature = weather_response['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
wind_dir = convert_degree(int(weather_response['properties']['timeseries'][0]['data']['instant']['details']['wind_from_direction']))
wind_speed = weather_response['properties']['timeseries'][0]['data']['instant']['details']['wind_speed']

# printing
print(f'''Your IP address is {ip}, located in {city}, {country}
Current weather at your location is:
Temperature: {temperature}{temp_units}
Pressure: {pressure} {pressure_units}
Wind direction: {wind_dir}
Wind speed: {wind_speed}{ws_units}''')
