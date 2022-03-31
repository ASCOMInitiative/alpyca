# This is shamefully devoid of my usual comments and module headers
# mostly because it's hack code for JIT learning. 

from alpaca import discovery, management
from alpaca.filterwheel import FilterWheel
from alpaca.telescope import Telescope
from alpaca.telescope import AlignmentModes
from alpaca.telescope import DriveRates
from alpaca.telescope import EquatorialCoordinateType
from alpaca.telescope import PierSide
from alpaca.telescope import TelescopeAxes
from alpaca.switch import Switch
from alpaca.camera import Camera
from alpaca.camera import SensorTypes
from alpaca.safetymonitor import SafetyMonitor

svrs = discovery.search_ipv4(2)
for svr in svrs:
    print(f"At {svr}")
    print (f"  V{management.apiversions(svr)} server")
    print (f"  {management.description(svr)['ServerName']}")
    devs = management.configureddevices(svr)
    for dev in devs:
        print(f"    {dev['DeviceType']}[{dev['DeviceNumber']}]: {dev['DeviceName']}")

f = FilterWheel('localhost:32323', 0)
f.Connected = True
print(f.Description)
print(f.Names)
print(f.FocusOffsets)
f.Connected = False

t = Telescope('localhost:32323', 0)
t.Connected = True
print(t.Name)
print(t.Description)
print(repr(AlignmentModes(t.AlignmentMode)))
print(repr(EquatorialCoordinateType(t.EquatorialSystem)))
print(repr(PierSide(t.SideOfPier)))
for r in t.TrackingRates :
    print(repr(DriveRates(r)))
print(t.UTCDate)
for a in t.AxisRates(TelescopeAxes.axisPrimary):
    print(str(a.Maximum) + " " + str(a.Minimum))
t.Connected = False

s = Switch('localhost:32323', 0)
s.Connected = True
print(s.GetSwitch(1))
print(s.MaxSwitch)
print(s.GetSwitchDescription(1))
print(s.GetSwitchName(1))
s.Connected = False

c = Camera('localhost:32323', 0)
c.Connected = True
print(repr(SensorTypes(c.SensorType)))
print(c.SetCCDTemperature)
c.Connected = False

m = SafetyMonitor('localhost:32323', 0)
m.Connected = True
print(m.IsSafe)
m.Connected = False

print("done") 
