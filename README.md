# 4x4_Gewinnt
This is a project for Project system development: Internet of Things course, which allows you to play 4x4-gewinnt games on your computer remotely through raspberry pi and ps4 controllers.
Server and Clients use Contraint objects application protocol (CoAp) to interact with each others

## How to set up

## SSH to Pi
```
ssh pi@<ipAdress>
```
pw: 
```
raspberry
```
## Setup Client
```
cd 4x4_gewinnt
```
### edit configurations in [config.txt](config.txt)
```
- set right Server-IP
- set right Controller-MAC
```
## Run Client
```
cd cpp_client

bash run.sh
```
Make sure to put your controller in pairing-mode by pressing the __PS-Button and Share-Button__ at the same time for a few Seconds.

Success if you see in terminal: "HealthCheck: Controller is connected"