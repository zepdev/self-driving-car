## client
- Runs on RCcar (RaspberryPi).
- The scripts 'main.py' and 'sender.py' should run automatically when RaspberryPi is switched on.
- Use 'config.py' to set the url of the message collector.

## server
Simple http message collector. Gets data from RCcar and stores it in Amazon S3. Run it with docker:

```
$ docker-compose build
$ docker-compose up
```
