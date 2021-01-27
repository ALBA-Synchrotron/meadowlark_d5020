import tango
import os

os.environ["TANGO_HOST"] = "localhost:10000"

d5020 = tango.DeviceProxy("lab_test/d5020/1")

property_names = [
    "url",
]

device_properties = d5020.get_property(property_names)
for prop in device_properties.keys():
    print("%s: %s" % (prop, device_properties[prop]))

# Changing Properties
# device_properties["serialline"] = ["RFC2217://dbl16ctmoxa01:4001"]
device_properties["url"] = ["/tmp/meadowlark_d5020"]

d5020.put_property(device_properties)

d5020.Init()