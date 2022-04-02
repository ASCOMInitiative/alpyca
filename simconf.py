import os
import xml.etree.ElementTree as ET
#
# Access by device name to Omni Simulator Settings as needed for tests
#
import ast

def settings(devname):
    data_file = f"{os.getenv('USERPROFILE')}/.ASCOM/Alpaca/ASCOM-Alpaca-Simulator/{devname}/v1/Instance-0.xml"
    tree = ET.parse(data_file)
    root = tree.getroot()
    s = {}
    for i in root.iter("SettingsPair"):
        k = i.find('Key').text
        v = i.find('Value').text
        try:
            s[k] = ast.literal_eval(v)
        except:
            s[k] = v
    return(s)    


def addr():
    return 'localhost:32323'        # All tests need this to talk to the Omni Simulator

if __name__ == "__main__":
    s = settings("Telescope")       # See the Instance-0.xml for the device or "server"
    for k, v in s.items():
        print(f"{k} {v}")