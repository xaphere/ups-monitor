# ups-monitor

Prometheus metics for [Waveshare UPS HAT](https://www.waveshare.com/wiki/UPS_HAT)

This repo contains extended version of the [python code](https://www.waveshare.com/w/upload/d/d9/UPS_HAT.7z) provided by Waveshare.

It starts a http server that serves prometheus metrics on port 8000.

In additon to the default python metrics it exposes

```
ups_load_voltage = Gauge('ups_load_voltage', 'Bus voltage on the load side')
ups_current = Gauge('ups_current', 'current in mA')
ups_power = Gauge('ups_power', 'draw power in W')
ups_charged = Gauge('ups_charged', 'how much power is stored in the battery')
```

## Build & Run

### Local

```sh
pip3 install -r requirements.txt
```

```sh
python3 src/main.py
```

### Docker

```sh
docker build -t ups-monitor .
```

Because the script need to read from I2C interface we need to attach it as a device Or run the container in `privileged` mode.

```sh
docker run --device /dev/i2c-1 -p 8000:8000 ups-monitor
```

When running the script checks every 10 seconds the UPS state and updates the metrics.
It also produses structured log that contains the same information. 