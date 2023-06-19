# 4x4_Gewinnt

## Demo

change IP-Adress in

Server: 
```
py_server/ConnectFour.py --> line 78 in def create_coap_server
```
Client: 
```
cpp_client/CoAPSender.cpp --> line 16 in Constructor
```

## SSH to Pi
```
ssh pi@<ipAdress>
```
pw: 
```
raspberry
```
```
cd 4x4_gewinnt/cpp_client/
```
## bluetooth
```
bluetoothctl
scan on
trust E8:47:3A:01:EE:E3
pair E8:47:3A:01:EE:E3
connect E8:47:3A:01:EE:E3
```