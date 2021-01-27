import tango
import os

os.environ["TANGO_HOST"] = "localhost:10000"

dev_info = tango.DbDevInfo()
dev_info.server = "Meadowlark_d5020/test"
dev_info._class = "Meadowlark_d5020"
dev_info.name = "lab_test/d5020/1"

db = tango.Database()
db.add_device(dev_info)