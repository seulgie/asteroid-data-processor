"""Provide filters for querying close approaches and limit the generated results.

This module contains tools for filtering and limiting results when querying
'CloseApproach' objects. Filters are created based on user-specified criteria
like date, distance, velocity, diameter, and whether an NEO is hazardous.

The primary functionalities include:
- 'create_filters': Constructs a collection of filters based on user inputs.
- 'limit': Limits the number of results produced by an iterator.

Filters are implemented as subclasses of 'AttributeFilter', which define the
specific attributes of interest and the conditions for filtering.
"""

import operator


class UnsupportedCriterionError(NotImplementedError):
    """An error raised when a filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to a reference value. It
    essentially functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Subclasses must override the 'get' method to specify which attribute of a 
    'CloseApproach' is being compared.

    Atributes:
       op (callable): A comparator function, e.g., 'operator.le'.
       value (any): The reference value to compare against.
    """

    def __init__(self, op, value):
        """Create a new 'AttributeFilter'.

        :param op: A binary predicate comparator (e.g., 'operator.le').
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Evaluate the filter on a 'CloseApproach.
        
        This invokes 'self(approach)' and applies the comparator.

        :param approach: A 'CloseApproach' instance to evaluate.
        :return: True if the filter criterion is satisfied, otherwise False.
        """
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a 'CloseApproach'.

        Subclasses must override this method to specify the attribute of
        interest for the filter.

        :param approach: A 'CloseApproach' instance.
        :return: The value of the relevant attribute for comparison.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """Return a string representation of the filter."""
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"


class DateFilter(AttributeFilter):
    """Filter for the exact date of a close approach."""

    @classmethod
    def get(cls, approach):
        """Return the date of the close approach.

        :param approach: A `CloseApproach` instance.
        :return: The `date` of the close approach.      
        """
        return approach.time.date()   

class StartDateFilter(AttributeFilter):
    """Filter for the start date of a close approach."""

    @classmethod
    def get(cls, approach):
        """Return the date of the close approach.

        :param approach: A `CloseApproach` instance.
        :return: The `date` of the close approach.
        """
        return approach.time.date()
    
class EndDateFilter(AttributeFilter):
    """Filter for the end date of a close approach."""

    @classmethod
    def get(cls, approach):
        """Return the date of the close approach.

        :param approach: A `CloseApproach` instance.
        :return: The `date` of the close approach.
        """
        return approach.time.date()


class DistanceFilter(AttributeFilter):
    """Filter for the nominal approach distance."""

    @classmethod
    def get(cls, approach):
        """Return the nominal approach distance.

        :param approach: A `CloseApproach` instance.
        :return: The `distance` of the close approach.
        """
        return approach.distance


class VelocityFilter(AttributeFilter):
    """Filter for the relative velocity of a close approach."""

    @classmethod
    def get(cls, approach):
        """Return the relative velocity of the close approach.

        :param approach: A `CloseApproach` instance.
        :return: The `velocity` of the close approach.
        """
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """Filter for the diameter of the NEO."""

    @classmethod
    def get(cls, approach):
        """Return the diameter of the NEO.

        :param approach: A `CloseApproach` instance.
        :return: The `diameter` of the NEO.
        """
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    """Filter for whether the NEO is hazardous."""
    
    @classmethod
    def get(cls, approach):
        """Return whether the NEO is hazardous.

        :param approach: A `CloseApproach` instance.
        :return: True if the NEO is hazardous, otherwise False.
        """
        return approach.neo.hazardous

def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters from user-specified criteria.

    Each argument corresponds to a different filter criterion. If a value is
    provided, a corresponding 'AttributeFilter' is created.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    filters = []
    # Date Filter
    if date:
        filters.append(DateFilter(operator.eq, date))
    if start_date:
        filters.append(DateFilter(operator.ge, start_date))
    if end_date:
        filters.append(DateFilter(operator.le, end_date))

    # Distance Filter
    if distance_min is not None:
        filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max is not None:
        filters.append(DistanceFilter(operator.le, distance_max))

    # Velocity Filter
    if velocity_min is not None:
        filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max is not None:
        filters.append(VelocityFilter(operator.le, velocity_max))

    # Diameter Filter
    if diameter_min is not None:
        filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max is not None:
        filters.append(DiameterFilter(operator.le, diameter_max))

    # Hazordous Filter
    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, hazardous))

    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n is None or n == 0: # If no limit is specified, yield all values.
        yield from iterator
    else:
        for i, value in enumerate(iterator): # Iterate with a counter.
            if i >= n:
                break
            yield value
 