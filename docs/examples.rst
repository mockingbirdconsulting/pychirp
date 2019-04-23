Examples
========

List all Devices
----------------

You can list all devices with the following code::

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

Create a device
---------------

Creating a device is also straight-forward::

    from pyloraserver import loraserver, device
    # Setup the connection
    cx = loraserver.Loraserver(
            loraserver_url="https://my.lora.server",
            loraserver_user="my_api_username",
            loraserver_pass="my_api_password"
            )
    d = device.Devices(loraserver_connection=cx)
    d.description = "This is my device"
    d.deveui = "deadbeefdeadbeef"
    d.name = "My-device-name"
    d.profile_id = "dead-beefbeef-dead-dead"
    d.appid = 1
    d.nwkKey = "MyRandomHexStrings"
    res = d.create_and_activate()
    print(res)
