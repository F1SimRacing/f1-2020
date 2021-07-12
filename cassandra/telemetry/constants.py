"""
More info is available here:
https://forums.codemasters.com/topic/54423-f1%C2%AE-2020-udp-specification/
"""

PACKET_MAPPER = {
    'PacketCarTelemetryData_V1': 'telemetry',
    'PacketLapData_V1': 'lap',
    'PacketMotionData_V1': 'motion',
    'PacketSessionData_V1': 'session',
    'PacketCarStatusData_V1': 'status',
    'PacketCarSetupData_V1': 'setup',
    'PacketParticipantsData_V1': 'participants',
}

TYRE_COMPOUND = {
    16: 'C5',  # super soft
    17: 'C4',
    18: 'C3',
    19: 'C2',
    20: 'C1',  # hard
    7: 'intermediates',
    8: 'wet',
    # F1 Classic
    9: 'dry',
    10: 'wet',
    # F2
    11: 'super soft',
    12: 'soft',
    13: 'medium',
    14: 'hard',
    15: 'wet',
}

WEATHER = {
    0: 'clear',
    1: 'light_cloud',
    2: 'overcast',
    3: 'light_rain',
    4: 'heavy_rain',
    5: 'storm',
}

DRIVER_STATUS = {
    0: 'in_garage',
    1: 'flying_lap',
    2: 'in_lap',
    3: 'out_lap',
    4: 'on_track',
}

SESSION_TYPE = {
    0: 'unknown',
    1: 'practice_1',
    2: 'practice_2',
    3: 'practice_3',
    4: 'short_practice',
    5: 'qualifying_1',
    6: 'qualifying_2',
    7: 'qualifying_3',
    8: 'short_qualifying',
    9: 'osq',
    10: 'race',
    11: 'race_2',
    12: 'time_trial',
}
