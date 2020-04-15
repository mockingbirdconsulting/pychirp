Examples
========

List all Devices
----------------

You can list all devices with the following code::

    from pychirp import chirpstack, device
    
    # Setup the connection
    cx = chirpstack.Chirpstack(
            chirpstack_url="https://my.lora.server",
            chirpstack_user="my_api_username",
            chirpstack_pass="my_api_password"
            )
    
    # Connect to the device class
    d = device.Devices(chirpstack_connection=cx)
    
    # Get all the devices
    devices = d.list_all(appid=7)
    print("We found %s devices" % devices['totalCount'])
    for dev in devices['result']:
        for key, val in dev.items():
            print("%s => %s" % (key, val))
        print("==========")

This will return the following output (the device ID's etc will be different for your server::

    We found 2 devices
    devEUI => bebebebebebebebe
    name => asdf
    applicationID => 7
    description => asdf
    deviceProfileID => 54767cb5-ba1b-494e-beef-8821ddd69bcb
    deviceProfileName => ODN_EU_02
    deviceStatusBattery => 255
    deviceStatusMargin => 256
    deviceStatusExternalPowerSource => False
    deviceStatusBatteryLevelUnavailable => True
    deviceStatusBatteryLevel => 0
    lastSeenAt => 2019-04-17T06:12:31.904650Z
    ==========
    devEUI => deadbeefdeadbeef
    name => pychirp_test
    applicationID => 7
    description => Testing from the new library
    deviceProfileID => 54767cb5-ba1b-494e-beef-8821ddd69bcb
    deviceProfileName => ODN_EU_02
    deviceStatusBattery => 255
    deviceStatusMargin => 256
    deviceStatusExternalPowerSource => False
    deviceStatusBatteryLevelUnavailable => True
    deviceStatusBatteryLevel => 0
    lastSeenAt => None
    ==========


Create a device
---------------

Creating a device is also straight-forward::

    from pychirp import chirpstack, device
    # Setup the connection
    cx = chirpstack.Chirpstack(
            chirpstack_url="https://my.lora.server",
            chirpstack_user="my_api_username",
            chirpstack_pass="my_api_password"
            )
    d = device.Devices(chirpstack_connection=cx)
    d.description = "This is my device"
    d.deveui = "deadbeefdeadbeef"
    d.name = "My-device-name"
    d.profile_id = "dead-beefbeef-dead-dead"
    d.appid = 1
    d.nwkKey = "MyRandomHexStrings"
    res = d.create_and_activate()
    print(res)
