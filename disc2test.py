from alpaca import discovery2, management

svrs = discovery2.search_ipv6(1,1)
print(svrs)
for svr in svrs:
   print(f"At {svr}")
   print (f"  V{management.apiversions(svr)} server")
   print (f"  {management.description(svr)['ServerName']}")
   devs = management.configureddevices(svr)
   for dev in devs:
       print(f"    {dev['DeviceType']}[{dev['DeviceNumber']}]: {dev['DeviceName']}")
