from shotgun_api3 import Shotgun
from pprint import pprint
import connection

# Connect to Shotgun site using imported credentials
sg = Shotgun(connection.shotgun_url, connection.script_name, connection.api_key)
project_id = 85

def schema_field_read():
    # Retrieve the schema configuration for each field
    field_schema_cut_duration = sg.schema_field_read('Sequence', 'sg_cut_duration')['sg_cut_duration']
    field_schema_ip_versions = sg.schema_field_read('Sequence', 'sg_ip_versions')['sg_ip_versions']
    field_schema_latest_version = sg.schema_field_read('Shot', 'sg_latest_version')['sg_latest_version']

    # Extract the 'properties' section from each schema
    properties_cut_duration = field_schema_cut_duration['properties']
    properties_ip_versions = field_schema_ip_versions['properties']
    properties_latest_version = field_schema_latest_version['properties']

    # Print the extracted schema properties for debugging
    print("Schema for Sequence.sg_cut_duration:")
    pprint(properties_cut_duration)

    print("\nSchema for Sequence.sg_ip_versions:")
    pprint(properties_ip_versions)

    print("\nSchema for Shot.sg_latest_version:")
    pprint(properties_latest_version)

    return properties_cut_duration, properties_ip_versions, properties_latest_version

def find_all_sequences(project_id):
    # Function to find all sequences for a given project
    filters = [['project', 'is', {'type': 'Project', 'id': project_id}]]
    fields = ['id', 'code', 'sg_cut_duration', 'sg_ip_versions']
    sequences = sg.find('Sequence', filters, fields)
    
    return sequences

def find_all_shots_for_sequence(sequence_id):
    # Function to find all shots for a specific sequence
    filters = [['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence_id}]]
    fields = ['id', 'code', 'sg_latest_version']
    shots = sg.find('Shot', filters, fields)
    
    return shots

# Main execution
properties_cut_duration, properties_ip_versions, properties_latest_version = schema_field_read()
sequences = find_all_sequences(project_id)
