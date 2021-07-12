# Telemetry
[UDP packet explanation](https://forums.codemasters.com/topic/54423-f1%C2%AE-2020-udp-specification/) covers
the data sent from the F1 2020 game in great detail. Below is an overview gathered from that
page.

|  **Packet** | **Frequency**  | **Notes**  |
|:--- | :---: | ---: |
|Motion|User Defined|-|
|Session|2 Per Second|-|
|Lap|User Defined|-|
|Event|When Triggered|-|
|Participants| 1 Per 5 Seconds|-|
|Car Setup| 2 Per Second|-|
|Car Telemetry|User Defined|-|
|Car Status|User Defined|-|
|Final Classification| 1|Only at the end of the race|


## Events

|Event|Code|Description|
|:--- | :---: | ---: |
|Session Started|**SSTA**|Sent when the session starts|
|Session Ended|**SEND**|Sent when the session ends|
|Fastest Lap|**FTLP**|When a driver achieves the fastest lap
|Retirement|**RTMT**|When a driver retires|
|DRS enabled|**DRSE**|Race control have enabled DRS|
|DRS disabled|**DRSD**|Race control have disabled DRS|
|Team mate in pits|**TMPT**|Your team mate has entered the pits|
|Chequered flag|**CHQF**|The chequered flag has been waved|
|Race Winner|**RCWN**|The race winner is announced|
|Penalty Issued|**PENA**| A penalty has been issued – details in event|
|Speed Trap Triggered|**SPTP**|Speed trap has been triggered by fastest speed|
