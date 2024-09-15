from shotgun_api3 import Shotgun
from pprint import pprint
import connection 

# Connect to Shotgun site using imported credentials
sg = Shotgun(connection.shotgun_url, connection.script_name, connection.api_key)
project_id = 85