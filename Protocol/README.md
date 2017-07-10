## Protocol
Based on the [Brody Lab protocol](http://brodywiki.princeton.edu/wiki/index.php/Etching_Fiber_Optics) we do the following:
- Use a [stripping tool](http://www.fiberinstrumentsales.com/fis-lynx-precision-cleaver-with-fiber-basket.html) to strip a [200 micron Newport fiber](https://www.newport.com/p/F-MBB) to remove outer jacket
- Use a [cleaver](http://www.fiberinstrumentsales.com/fis-lynx-precision-cleaver-with-fiber-basket.html) to cut fiber down to ~ 15mm
- Use a butane torch/lighter to burn away ~3mm of thin plastic coating to expose the tip for etching
- Fill a small container with 48% HF, and top with a layer of mineral oil
- Submerge the tip ~2mm past the mineral oil/HF interface.
- Retract the fiber at ~0.75mm/hr. We use Zaber's [T-LHM050A](http://www.zaber.com/products/product_detail.php?detail=T-LHM050A) motor. The motor can be be controlled using  [zaber_controller.ipynb](zaber_controller.ipynb) (requires [zaber_device](https://github.com/janelia-pypi/zaber_device_python), [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/user_install.html) and Python 2.7).


## Setup for using jupyter notebook as motor controller
#### 1. Download [Anaconda](https://www.continuum.io/downloads)
#### 2. Create Python 2.7 Environment called motorController
`conda create motorController python=2.7`
#### 3. Switch to new environment
`source activate motorController`

**or**

`activate motorController`
#### 4. Install ipywidgets
`conda install -c conda-forge ipywidgets`
#### 5. Install zaber_device
` pip install zaber_device`

#### 6. Navigate to this directory and launch zaber_controller notebook
` jupyter notebook zaber_controller.ipynb`
