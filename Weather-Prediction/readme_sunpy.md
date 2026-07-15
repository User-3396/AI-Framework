```python
import sunpy.map
import sunpy.data.sample
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import SkyCoord
```
```python
aia_map =sunpy.map.Map(sunpy.data.sample.AIA_171_IMAGE)
```

```python
plt.figure(figsize =(8,8))
aia_map.plot()
plt.colorbar()
plt.title("Sample Solar Image")
plt.show()
```

```python
bottom_left =SkyCoord(0*u.arcsec, -500*u.arcsec, frame=aia_map.coordinate_frame)
top_right =SkyCoord(500*u.arcsec, 0*u.arcsec, frame =aia_map.coordinate_frame)

submap =aia_map.submap(bottom_left, top_right =top_right)
```

```python
plt.figure(figsize =(6,6))
# aia_map.plot()
submap.plot()
plt.title("Subplot Solar Image")
plt.show()
```
