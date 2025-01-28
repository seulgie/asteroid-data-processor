"""This module contains classes that define Near-Earth Objects (NEOs) and their close approaches to Earth."""

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.
    """
    
    def __init__(self, **info):
        """Create a new `NearEarthObject`."""
        # Assigning values from the dictionary to instance attributes
        self.designation = info.get("designation", "")
        self.name = info.get("name", None) # None if no name
        self.diameter = info.get("diameter", float('nan')) # Default to NaN if no diameter
        self.hazardous = info.get("hazardous", False)

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} ({self.name})"
        return self.designation

    def __str__(self):
        """Return `str(self)`."""
        hazardous_str = "is" if self.hazardous else "if not"
        return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and {hazardous_str} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
    
    def serialize(self):
        """Return a dictionary representation of this NEO."""
        return {
            'designation': self.designation,
            'name': self.name or '', # Empty string for missing name
            'diameter_km': self.diameter if self.diameter is not None else float('nan'),
            'potentially_hazardous': self.hazardous
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.
    """
    
    def __init__(self, **info):
        """Create a new `CloseApproach`."""
        self._designation = info.get("designation", "")
        self.time = cd_to_datetime(info.get("time", ""))
        self.distance = info.get("distance", 0.0)
        self.velocity = info.get("velocity", 0.0)

        # Initially, the neo attribute is None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time."""
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"On {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
    
    def serialize(self):
        """Return a dictionary representation of this CloseApproach."""
        return {
            'datetime_utc': datetime_to_str(self.time),
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'neo': self.neo.serialize() # Include associated NEO data
        }
