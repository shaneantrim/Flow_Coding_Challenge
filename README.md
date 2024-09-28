# Shotgrid Coding Challenge

Python script that queries Shotgrid fields sg_cut_duration, sg_ip_versions and sg_latest_version for a given project ID without knowing the query fields filter conditions in advance. 

# Installation
-Create virtual env with required version python 3.11 -m venv venv
-Install required packages pip install git+https://github.com/shotgunsoftware/python-api.git <br />
-Create separate connection.py file to connect to the Shotgrid site and access the script using the following format: <br />
`shotgun_url = "your_shotgun_url"` <br />
`script_name = "your_script_name"` <br />
`api_key = "your_api_key"` <br />

# Result
Running the script will create an output.html file in the same folder where the script lives that can be opened in a browser and will display all of the results for sg_cut_duration, sg_ip_versions and sg_latest_version in a table.
 
<img width="1405" alt="results" src="https://github.com/user-attachments/assets/616daf74-e06d-444b-9b90-db5e56e36307">
