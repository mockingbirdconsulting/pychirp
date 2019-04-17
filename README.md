# PyLoRaServer

The LoRaServer.io Python Library

# Example usage

```
from pyloraserver import loraserver, device

# Setup the connection
cx = loraserver.Loraserver(
        loraserver_url="https://my.lora.server",
        loraserver_user="my_api_username",
        loraserver_pass="my_api_password"
        )

# Connect to the device class
d = device.Devices(loraserver_connection=cx)

# Get all the devices
d.list_all(appid=7).content
```
