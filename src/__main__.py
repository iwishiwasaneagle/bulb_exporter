from typing import List
import prometheus_client
import time
import sys
import pysmartthings
import aiohttp
import asyncio
from loguru import logger
import os

def setup():
    # Setup logger
    valid_log_levels = ['DEBUG','INFO','WARNING','ERROR']
    log_level = os.environ.get('LOG_LEVEL','INFO')
    if log_level not in valid_log_levels:
        logger.error(f"LOG_LEVEL={log_level} is not a valid input ({valid_log_levels})")
        sys.exit(1)
    logger.remove()
    logger.add(sys.stdout, level=log_level)

    # Setup prometheus_client
    gas = prometheus_client.Gauge('bulb_gas_used_units','Gas meter readings')
    electricity = prometheus_client.Gauge('bulb_electricity_used_kwh','Electricity meter readings')
    refresh_timer = prometheus_client.Summary("smartthings_refresh_time_seconds", "Time taken to fetch data from SmartThings")
    info = prometheus_client.Info('bulb_build_info','bulb_exporter build information')

    return gas, electricity, refresh_timer, info

async def getBulbMeter(api: pysmartthings.SmartThings) -> pysmartthings.Device:
    try:
        devices: List[pysmartthings.Device]  = await api.devices()
    except aiohttp.client_exceptions.ClientResponseError as e:
        if e.status == 403:
            logger.error(f"Access denied error ({e.status}) while fetching devices. This is most likely due to incorrect permissions being granted to the API token.")
        else:
            logger.error(f"Error while accessing the device list: {e}")
        sys.exit(1)
    
    bulb: pysmartthings.Device = None
    for device in devices:
        if device.name == "smartthings-energy-control-bulb":
            bulb = device
            break

    if bulb is None:
        logger.error("No bulb energy meter found!")
        sys.exit(1)
    else:
        logger.info(f"Bulb energy meter found with id=\"{bulb.device_id}\" and label=\"{bulb.label}\"")

    return bulb

async def scrape(token: str) -> None:
    gas_gauge, electricity_gauge, refresh_timer, info = setup()

    info.info({'version':'0.0.1', 'log_level':os.environ.get('LOG_LEVEL','INFO')})
    
    async with aiohttp.ClientSession() as session:
        api: pysmartthings.SmartThings = pysmartthings.SmartThings(session, token)
        bulb = await getBulbMeter(api)

        while True:
            t_start: float = time.time()

            with refresh_timer.time():
                await bulb.status.refresh()

            electricity_reading: float = bulb.status.values.get('energy')
            if electricity_reading <= 0 or electricity_reading is None:
                logger.error(f"Invalid value {electricity_reading=}")
                sys.exit(1)
            electricity_gauge.set(electricity_reading)

            gas_reading: float = bulb.status.values.get('gasMeter')
            if gas_reading <= 0 or gas_reading is None:
                logger.error(f"Invalid value {gas_reading=}")
                exit(1)
            gas_gauge.set(gas_reading)

            if os.environ.get("ONCE", "FALSE") == "TRUE":
                logger.debug(f"Exiting after running once: {os.environ['ONCE']=}")
                break
            await asyncio.sleep(os.environ.get('INTERVAL',20)-(time.time()-t_start))

def main():
    prometheus_client.start_http_server(os.environ.get('PORT',8023))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    token = os.environ.get('SMARTTHINGS_TOKEN',None)
    if not token:
        logger.error(f"No value for environmental variable 'SMARTTHINGS_TOKEN'")
        sys.exit(1)

    loop.run_until_complete(scrape(token))

if __name__ == "__main__":
    main()