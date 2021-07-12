from typing import List, NamedTuple


class Location(NamedTuple):
    name: str


def get_all_locations() -> List[Location]:
    """
    Return a list of all the locations
    """

    return [
        Location(name="Rear Left"),
        Location(name="Rear Right"),
        Location(name="Front Left"),
        Location(name="Front Right"),
    ]
