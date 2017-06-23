Based on the [Brody Lab protocol](Brody lab protocol.pdf) we do the following:
- Use a [stripping tool](http://www.fiberinstrumentsales.com/fis-lynx-precision-cleaver-with-fiber-basket.html) to strip a [200 micron Newport fiber](https://www.newport.com/p/F-MBB) to remove outer jacket
- Use a [cleaver](http://www.fiberinstrumentsales.com/fis-lynx-precision-cleaver-with-fiber-basket.html) to cut fiber down to ~ 15mm
- Use a butane torch/lighter to burn away ~3mm of thin plastic coating to expose the tip for etching
- Fill a small container with 48% HF, and top with a layer of mineral oil
- Submerge the tip ~2mm past the mineral oil/HF interface.
- Retract the fiber at ~1.5mm/hr. We use Zaber's [T-LHM050A](http://www.zaber.com/products/product_detail.php?detail=T-LHM050A) motor. To control the motor use a [Zaber Device Python Library](https://github.com/janelia-pypi/zaber_device_python). Can be controlled using the [zaber_controller.ipynb](zaber_controller.ipynb) with a Python 2.7 kernel.
