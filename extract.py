"""Extract and load data for near-Earth objects and close approaches.

This module provides functions to read near-Earth object (NEO) data from a CSV file
and close approach (CAD) data from a JSON file. The data is parsed and converted
into corresponding 'NearEarthObject' and 'CloseApproach' instances for further use.

Functions:
- load_neos: Reads NEO data from a CSV file and returns a list of 'NearEarthObject's.
- load_approaches: Reads CAD data from a JSON file and returns a list of 'CloseApproach'es.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    This function reads data from a CSV file containing information about NEOs and
    converts each entry into an instance of the 'NearEarthObject' class.

    :param neo_csv_path: str - A path to the CSV file containing NEO data.
    :return: list[NearEarthObject] - A list of `NearEarthObject` instances.
    """
    neos = []
    with open(neo_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            neos.append(NearEarthObject(
                designation=row.get('pdes',''),
                name=row.get('name') or None,
                diameter=float(row['diameter']) if row['diameter'] else float('nan'),
                hazardous=row['pha'] == 'Y'
            ))
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    This function reads data from a JSON file containing close approach details and
    converts each entry into an instance of the 'CloseApproach' class.

    :param cad_json_path: str - A path to a JSON file containing close approach data.
    :return: list[CloseApproach] - A list of 'CloseApproach' instances.
    """
    approaches = []
    with open(cad_json_path, 'r') as infile:
        contents = json.load(infile)
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
