schema = {
    "doc": "Lap reading.",
    "name": "Lap",
    "namespace": "F12020",
    "type": "record",
    "fields": [
        {"name": "type", "type": "string"},
        {"name": "name", "type": "string"},
        {"name": "sessionTime", "type": "float"},
        {"name": "sessionUID", "type": "double"},
        {"name": "lastLapTime", "type": "float"},
        {"name": "currentLapTime", "type": "float"},
        {"name": "sector1TimeInMS", "type": "int"},
        {"name": "sector2TimeInMS", "type": "int"},
        {"name": "bestLapTime", "type": "float"},
        {"name": "bestLapNum", "type": "int"},
        {"name": "bestLapSector1TimeInMS", "type": "int"},
        {"name": "bestLapSector2TimeInMS", "type": "int"},
        {"name": "bestLapSector3TimeInMS", "type": "int"},
        {"name": "bestOverallSector1TimeInMS", "type": "int"},
        {"name": "bestOverallSector1LapNum", "type": "int"},
        {"name": "bestOverallSector2TimeInMS", "type": "int"},
        {"name": "bestOverallSector2LapNum", "type": "int"},
        {"name": "bestOverallSector3TimeInMS", "type": "int"},
        {"name": "bestOverallSector3LapNum", "type": "int"},
        {"name": "lapDistance", "type": "float"},
        {"name": "totalDistance", "type": "float"},
        {"name": "safetyCarDelta", "type": "float"},
        {"name": "carPosition", "type": "int"},
        {"name": "currentLapNum", "type": "int"},
        {"name": "pitStatus", "type": "int"},
        {"name": "sector", "type": "int"},
        {"name": "currentLapInvalid", "type": "int"},
        {"name": "penalties", "type": "int"},
        {"name": "gridPosition", "type": "int"},
        {"name": "driverStatus", "type": "int"},
        {"name": "resultStatus", "type": "int"},
    ],
}
