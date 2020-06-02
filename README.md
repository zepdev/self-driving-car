## client
- Runs on RCcar (RaspberryPi). Two applications, `app` and `sender`, they should run together.
- app: Main application for driving the car. Run the script `run.sh`.
- sender: This is a docker application that send data to the server. Run it with docker-compose:

```
$ docker-compose build
$ docker-compose up
```

The RPi should have internet connection


## server
Simple http message collector. Gets data from RCcar and stores it in Amazon S3. Run it with docker-compose:

```
$ docker-compose build
$ docker-compose up
```
