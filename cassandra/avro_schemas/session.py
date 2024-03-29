schema = {
    "doc": "Session reading.",
    "name": "Session",
    "namespace": "F12020",
    "type": "record",
    "fields": [
        {"name": "type", "type": "string"},
        {"name": "name", "type": "string"},
        {"name": "sessionTime", "type": "float"},
        {"name": "sessionUID", "type": "double"},
        {"name": "weather", "type": "int"},
        {"name": "trackTemperature", "type": "int"},
        {"name": "airTemperature", "type": "int"},
        {"name": "totalLaps", "type": "int"},
        {"name": "trackLength", "type": "int"},
        {"name": "sessionType", "type": "int"},
        {"name": "trackId", "type": "int"},
        {"name": "formula", "type": "int"},
        {"name": "sessionTimeLeft", "type": "int"},
        {"name": "sessionDuration", "type": "int"},
        {"name": "pitSpeedLimit", "type": "int"},
        {"name": "gamePaused", "type": "int"},
        {"name": "isSpectating", "type": "int"},
        {"name": "spectatorCarIndex", "type": "int"},
        {"name": "sliProNativeSupport", "type": "int"},
        {"name": "numMarshalZones", "type": "int"},
        {"name": "safetyCarStatus", "type": "int"},
        {"name": "networkGame", "type": "int"},
        {"name": "numWeatherForecastSamples", "type": "int"},
    ],
}
