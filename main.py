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
    filters = [["project", "is", {"type": "Project", "id": project_id}]]
    fields = [
        "id",
        "code",
    ]
    sequences = sg.find("Sequence", filters, fields)

    return sequences


def find_all_shots_for_sequence(sequence_id):
    # Function to find all shots for a specific sequence
    filters = [["sg_sequence", "is", {"type": "Sequence", "id": sequence_id}]]
    fields = ["id", "code"]
    shots = sg.find("Shot", filters, fields)

    return shots


def schema_query(field_schema, sequence_id):
    entity_type = field_schema["query"]["value"]["entity_type"]
    path = field_schema["query"]["value"]["filters"]["conditions"][0]["path"]
    relation = field_schema["query"]["value"]["filters"]["conditions"][0][
        "relation"]
    type = field_schema["query"]["value"]["filters"]["conditions"][0][
        "values"][0]["type"]
    summary_default = field_schema["summary_default"]["value"]
    summary_field = field_schema["summary_field"]["value"]

    print(f"Summarizing {summary_field}...")
    summary_value = sg.summarize(
        entity_type=entity_type,
        filters=[[path, relation, {
            "type": type,
            "id": sequence_id
        }]],
        summary_fields=[{
            "field": summary_field,
            "type": summary_default,
        }],
    )

    pprint(summary_value)
    return summary_value


def find_one_shot_version(field_schema, id, order):
    entity_type = field_schema["query"]["value"]["entity_type"]
    path = field_schema["query"]["value"]["filters"]["conditions"][0]["path"]
    relation = field_schema["query"]["value"]["filters"]["conditions"][0][
        "relation"]
    type = field_schema["query"]["value"]["filters"]["conditions"][0][
        "values"][0]["type"]
    summary_field = field_schema["summary_field"]["value"]
    summary_value = field_schema["summary_value"]["value"]["column"]

    print(f"Find one {summary_field}...")
    data = sg.find_one(
        entity_type=entity_type,
        filters=[
            [path, relation, {
                "type": type,
                "id": id
            }],
        ],
        fields=[summary_field, summary_value],
        order=order,
    )

    pprint(data)
    return data


def find_latest_version(sequence_id):
    print("\nFind sg_latest_version for each Shot...")
    filters = [["sg_sequence", "is", {"type": "Sequence", "id": sequence_id}]]
    fields = ["id"]
    shots = sg.find("Shot", filters, fields)

    pprint(f"\nShots for Sequence {sequence_id}:")
    find_latest_version = {}
    for shot in shots:
        pprint(f"ID: {shot['id']}")

        latest_version = sg.find_one(
            entity_type="Version",
            filters=[
                ["entity", "is", {
                    "type": "Shot",
                    "id": shot["id"]
                }],
                ["sg_status_list", "is_not", "na"],
            ],
            fields=["code", "created_at"],
            order=[{
                "field_name": "created_at",
                "direction": "desc"
            }],
        )
        find_latest_version[shot["id"]] = latest_version
        pprint(latest_version)

    return find_latest_version


# Main execution
(
    properties_cut_duration,
    properties_ip_versions,
    properties_latest_version,
) = schema_field_read()
sequences = find_all_sequences(project_id)

sg_cut_duration = {}
sg_ip_versions = {}
latest_version_summary = {}

for sequence in sequences:
    sequence_id = sequence["id"]
    # get_summary_for_field
    sg_cut_duration = schema_query(properties_cut_duration, sequence_id)
    sg_ip_versions = schema_query(properties_ip_versions, sequence_id)

    shots = find_all_shots_for_sequence(sequence_id)
    for shot in shots:
        shot_id = shot["id"]
        # find_one_for_field
        code_data = find_one_shot_version(
            properties_latest_version,
            shot_id,
            [{
                "field_name": "created_at",
                "direction": "desc"
            }],
        )
        latest_version_summary[shot_id] = code_data


def generate_html_file(result_cut_duration, result_ip_versions,
                       latest_version_summary):
    # HTML content with double curly braces for CSS
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Shotgun API Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Shotgun API Results</h1>

        <h2>Cut Duration Summary</h2>
        <table>
            <tr>
                <th>Field</th>
                <th>Average</th>
            </tr>
            <tr>
                <td>sg_cut_duration</td>
                <td>{cut_duration_avg}</td>
            </tr>
        </table>

        <h2>IP Versions Summary</h2>
        <table>
            <tr>
                <th>Field</th>
                <th>Record Count</th>
            </tr>
            <tr>
                <td>code</td>
                <td>{ip_versions_count}</td>
            </tr>
        </table>

        <h2>Latest Version Summary</h2>
        <table>
            <tr>
                <th>Shot ID</th>
                <th>Latest Version Code</th>
                <th>Created At</th>
            </tr>
            {latest_version_rows}
        </table>
    </body>
    </html>
    """

    print("\nGenerating HTML content...")

    # Extract the summary data
    cut_duration_avg = result_cut_duration['summaries'].get(
        'sg_cut_duration', 'N/A')
    ip_versions_count = result_ip_versions['summaries'].get('code', 'N/A')

    latest_version_rows = ""
    for shot_id, version_info in latest_version_summary.items():
        if version_info:
            version_code = version_info.get('code', 'N/A')
            created_at = version_info.get('created_at', 'N/A')
        else:
            version_code = "N/A"
            created_at = "N/A"
        latest_version_rows += f"<tr><td>{shot_id}</td><td>{version_code}</td><td>{created_at}</td></tr>"

    # Format the HTML content with dynamic values
    formatted_html = html_content.format(
        cut_duration_avg=cut_duration_avg,
        ip_versions_count=ip_versions_count,
        latest_version_rows=latest_version_rows)

    # Write the HTML content to a file
    with open("output.html", "w") as f:
        f.write(formatted_html)

    print("HTML file 'output.html' has been created successfully.")


# Generate HTML
generate_html_file(sg_cut_duration, sg_ip_versions, latest_version_summary)
