Shotgrid Coding Challenge

Python script that querys Shotgrid fields sg_cut_duration, sg_ip_versions and sg_latest_version without knowing the query fields filter conditions in advance. 

Installation
Install required packages pip install git+https://github.com/shotgunsoftware/python-api.git
Create separate connection.py file to connect to the Shotgrid site and access the script using the following format:
shotgun_url = "your shotgrid site"
script_name = "your script name"
api_key = "your api key"

Done!

Running the script will create an output.html file in the same folder where the script lives that can be opened in a browser and will display all of the results for sg_cut_duration, sg_ip_versions and sg_latest_version in a table.
 
