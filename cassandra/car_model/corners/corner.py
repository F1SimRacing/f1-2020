from dataclasses import dataclass
from typing import Union

from cassandra.car_model.car_locations import Location
from cassandra.car_model.corners.wheels.tyres.tyre import Tyre
from cassandra.car_model.corners.wheels.wheel import Wheel


@dataclass
class Corner:
    _wheel: Union[Wheel, None]

    def __init__(self, location: Location):
        self.location: Location = location

    @property
    def wheel(self):
        if not self._wheel:
            self._wheel = Wheel(
                speed=0.0,
                slip=0.0,
                tyre=Tyre(
                    pressure=0.0,
                    surface_temperature=0.0,
                    inner_temperature=0.0,
                    wear=0.0,
                    compound='',
                    visual_compound='',
                    age_laps=0,
                    damage=0.0,
                ),
                location=self.location,
            )
