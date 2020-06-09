## client
- Runs on RCcar (RaspberryPi). Two applications, `app` and `sender`, they should run together.
- app: Main application for driving the car. Start via `bash run.sh`.
- sender: This is a docker application that sends data to the server. Run it with docker-compose:

```
$ docker-compose build
$ docker-compose up
```

Info: The RPi should have internet connection through WiFi.


## server
Simple http message collector. Gets data from RCcar and stores it in Amazon S3. Run it with docker-compose:

```
$ docker-compose build
$ docker-compose up
```
