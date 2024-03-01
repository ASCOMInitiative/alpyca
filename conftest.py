import pytest
import os
import sys
import json
import platform
import ast
import requests
import xml.etree.ElementTree as ET

@pytest.fixture(scope="module")
def device(request):
    global d
    n = getattr(request.module, "dev_name")
    print(f'Setup: for {n}')
    c = getattr(sys.modules[f"alpaca.{n.lower()}"], n)  # Creates a device class by string name :-)
    d =  c('localhost:32323', 0)                       # Created an instance of the class
#    d = c('[fe80::9927:65fc:e9e8:f33a%eth0]:32323', 0)  # RPi 4 Ethernet to Windows OmniSim IPv6
    d.Connected = True
    print(f"Setup: Connected to OmniSim {n} OK")
    return d
#
# Grabs the settings for the device from the OmniSim settings data *once*.
#
@pytest.fixture(scope="module")
def settings(request):
    n = getattr(request.module, "dev_name").lower()
    resp = requests.get(f'http://localhost:32323/simulator/v1/{n}/0/xmlprofile?ClientID=0&ClientTransactionID=0')
    text = eval(resp.content)["Value"]
    root = ET.ElementTree(ET.fromstring(text)).getroot()
    s = {}
    for i in root.iter("SettingsPair"):
        k = i.find('Key').text
        v = i.find('Value').text
        try:
            s[k] = ast.literal_eval(v)      # Numerics
        except:
            try:
                s[k] = json.loads(v)        # Boolean strings from XML
            except:
                s[k] = v                    # Punt ... string
    print(f"Setup: {n} OminSim Settings retrieved")
    return s

@pytest.fixture(scope="module")
def disconn(request):
    global d
    yield
    d.Connected = False
    n = getattr(request.module, "dev_name")
    print(f"Teardown: {n} Disconnected")

#
# Common function to get settings for @pytest.mark.skipif() decorators
#
def get_settings(device: str):
    resp = requests.get(f'http://localhost:32323/simulator/v1/{device}/0/xmlprofile?ClientID=0&ClientTransactionID=0')
    text = eval(resp.content)["Value"]
    root = ET.ElementTree(ET.fromstring(text)).getroot()
    s = {}
    for i in root.iter("SettingsPair"):
        k = i.find('Key').text
        v = i.find('Value').text
        try:
            s[k] = ast.literal_eval(v)      # Numerics
        except:
            try:
                s[k] = json.loads(v)        # Boolean strings from XML
            except:
                s[k] = v                    # Punt ... string
    return s
