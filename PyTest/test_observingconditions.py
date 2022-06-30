# PyTest Unit tests for IObservingConditions
import conftest

from alpaca.observingconditions import ObservingConditions
dev_name = "ObservingConditions"

#
# Grab the camera settings for the pytest.mark.skipif() decisions 
#
c_sets = conftest.get_settings('ObservingConditions')

def test_observingconditions(device, settings, disconn):
    d = device
    s = settings
    print("Test ObservingConditions interface. OmniSim must be set to override")
    print("all settings with any non-zero values. ")
    assert d.AveragePeriod <= s['Average Period']       # Default after reset
    assert s['CloudCoverOverride'] == True, "CloudCover value must be overridden"
    assert d.CloudCover == s['CloudCoverOverride Value'], 'CloudCover value mismatch'
#   No settings for DewPoint
#    assert s['DewPointOverride'] == True, "DewPoint value must be overridden"
#    assert d.DewPoint == s['DewPointOverride Value'], 'DewPoint value mismatch'
    assert s['HumidityOverride'] == True, "Humidity value must be overridden"
    assert d.Humidity == s['HumidityOverride Value'], 'Humidity value mismatch'
    assert s['PressureOverride'] == True, "Pressure value must be overridden"
    assert d.Pressure == s['PressureOverride Value'], 'Pressure value mismatch'
    assert s['RainRateOverride'] == True, "RainRate value must be overridden"
    assert d.RainRate == s['RainRateOverride Value'], 'RainRate value mismatch'
    assert s['SkyBrightnessOverride'] == True, "SkyBrightness value must be overridden"
    assert d.SkyBrightness == s['SkyBrightnessOverride Value'], 'SkyBrightness value mismatch'
    assert s['SkyQualityOverride'] == True, "SkyQuality value must be overridden"
    assert d.SkyQuality == s['SkyQualityOverride Value'], 'SkyQuality value mismatch'
    assert s['SkyTemperatureOverride'] == True, "SkyTemperature value must be overridden"
    assert d.SkyTemperature == s['SkyTemperatureOverride Value'], 'SkyTemperature value mismatch'
    assert s['StarFWHMOverride'] == True, "StarFWHM value must be overridden"
    assert d.StarFWHM == s['StarFWHMOverride Value'], 'StarFWHM value mismatch'
    assert s['TemperatureOverride'] == True, "Temperature value must be overridden"
    assert d.Temperature == s['TemperatureOverride Value'], 'Temperature value mismatch'
    assert s['WindDirectionOverride'] == True, "WindDirection value must be overridden"
    assert d.WindDirection == s['WindDirectionOverride Value'], 'WindDirection value mismatch'
    assert s['WindGustOverride'] == True, "WindGust value must be overridden"
    assert d.WindGust == s['WindGustOverride Value'], 'WindGust value mismatch'
    assert s['WindSpeedOverride'] == True, "WindSpeed value must be overridden"
    assert d.WindSpeed == s['WindSpeedOverride Value'], 'WindSpeed value mismatch'
    assert d.TimeSinceLastUpdate('CloudCover') <= s['Sensor Read Period'], 'Update time mismatch'
    assert d.SensorDescription('WindSpeed') == 'ObservingConditions Simulated WindSpeed sensor' # Hard wired in OmniSim
    