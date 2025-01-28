"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        Links NEOs and close approaches together by associating each close
        approach with its corresponding NEO.

        :param neos: A collection of `NearEarthObject` instances.
        :param approaches: A collection of `CloseApproach` instances.
        """
        self._neos = neos
        self._approaches = approaches

        # Auxiliary data structures for quick lookup
        self._neos_by_designation = {neo.designation: neo for neo in neos}
        self._neos_by_name = {neo.name: neo for neo in neos if neo.name}

        # Link NEOs and their close approaches
        for approach in self._approaches:
            neo = self._neos_by_designation.get(approach._designation)
            if neo:
                approach.neo = neo  # Link the NEO to the close approach
                neo.approaches.append(approach)  # Add the close approach to the NEO's list

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        Each NEO in the dataset has a unique primary designation, as a string.
        The matching is exact, so check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the given primary designation, or `None`.
        """
        return self._neos_by_designation.get(designation)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        Not every NEO in the dataset has a name. The matching is exact, so check
        for spelling and capitalization if no match is found.

        :param name: The name of the NEO to search for, as a string.
        :return: The `NearEarthObject` with the given name, or `None`.
        """
        return self._neos_by_name.get(name)

    def query(self, filters=()):
        """Generate close approaches that match a collection of filters.

        This method yields `CloseApproach` objects that satisfy all the provided
        filters. If no filters are provided, it yields all known close approaches.

        The `CloseApproach` objects are generated in internal order, which is not
        guaranteed to be meaningfully sorted, although it is often sorted by time.

        :param filters: An iterable of filter functions to apply to close approaches.
        :return: A generator yielding matching `CloseApproach` objects.
        """
        for approach in self._approaches:
            if all(f(approach) for f in filters):
                yield approach