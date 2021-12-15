import time
import structlog

from prometheus_client import start_http_server, Summary, Gauge
from INA219 import INA219


log = structlog.get_logger()

ina219 = INA219(addr=0x42)
ups_load_voltage = Gauge('ups_load_voltage', 'Bus voltage on the load side')
ups_current = Gauge('ups_current', 'current in mA')
ups_power = Gauge('ups_power', 'draw power in W')
ups_charged = Gauge('ups_charged', 'how much power is stored in the battery')


def update_ups_metrics():
    bus_voltage = ina219.getBusVoltage_V()  # voltage on V- (load side)
    # voltage between V+ and V- across the shunt
    shunt_voltage = ina219.getShuntVoltage_mV() / 1000
    current = ina219.getCurrent_mA()  # current in mA
    power = ina219.getPower_W()  # power in W
    p = (bus_voltage - 6) / 2.4 * 100
    if (p > 100):
        p = 100
    if (p < 0):
        p = 0

    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    # print("PSU Voltage:   {:6.3f} V".format(bus_voltage + shunt_voltage))
    # print("Shunt Voltage: {:9.6f} V".format(shunt_voltage))
    
    log.dbg("",load_voltage="{:.3f}V".format(bus_voltage), current="{:.6f}A".format(
        current / 1000), power="{:.3f}W".format(power), percent="{:.1f}%".format(p))

    ups_load_voltage.set("{:.3f}".format(bus_voltage))
    ups_current.set("{:.6f}".format(current / 1000))
    ups_power.set("{:.3f}".format(power))
    ups_charged.set("{:.1f}".format(p))


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.

    while True:
        update_ups_metrics()
        time.sleep(10)
