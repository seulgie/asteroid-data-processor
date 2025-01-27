
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    with open(neo_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # Extract relevant fields and pass them to the NearEarthObject constructor
            neos.append(NearEarthObject(
                designation=row.get('pdes',''),
                name=row.get('name') or None,
                diameter=float(row['diameter']) if row['diameter'] else float('nan'),
                hazardous=row['pha'] == 'Y'
            ))
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approaches = []
    with open(cad_json_path, 'r') as infile:
        contents = json.load(infile)
        # The data is under the "data" key, and field names are mapped in the "fields" key
        fields = contents['fields']
        data = contents['data']

        # Map the data fields to their indices
        idx_designation = fields.index('des')
        idx_time = fields.index('cd')
        idx_distance = fields.index('dist')
        idx_velocity = fields.index('v_rel')

        for entry in data:
            approaches.append(CloseApproach(
                designation=entry[idx_designation],
                time=entry[idx_time],
                distance=float(entry[idx_distance]),
                velocity=float(entry[idx_velocity])
            ))
    return approaches
