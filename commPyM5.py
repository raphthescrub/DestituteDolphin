import dolphinStout
import cv2Viewer

import numpy as np
from bleak import BleakClient
from bleak import BleakScanner
import asyncio
import struct 


status = False
class commPyM5:
    def connectionToM5():
        def notification_callback(sender, payload):
            global status
            status = (struct.unpack("<?", payload))
            
        async def run():
            async with BleakClient("E8:9F:6D:09:35:DA") as client:
                await client.start_notify('15b1f42d-535c-489d-9467-7aa79e662e0f', notification_callback)
                while True:
                    await asyncio.sleep(1)
        asyncio.run(run())