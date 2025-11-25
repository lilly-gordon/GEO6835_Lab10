import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import leafmap.foliumap as leafmap

st.title("CRC NAIP 2011 NDVI Viewer (Leafmap Version)")

# ---------------------------------------------------
# 1) Load NDVI TIFF (relative path is cloud safe)
# ---------------------------------------------------
tif_path = "data/CRC_NAIP_2011_NDVI.tif"

img = Image.open(tif_path)
ndvi = np.array(img)

# ---------------------------------------------------
# 2) Geospatial Bounds
# ---------------------------------------------------
left  = -109.639353
right = -109.628493
bottom = 38.262410
top    = 38.268114

bounds = [[bottom, left], [top, right]]

# ---------------------------------------------------
# 3) NDVI Breaks + Colors
# ---------------------------------------------------
ndvi_breaks = [-1.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]

ndvi_colors = [
    '#FFFFFF',
    '#CE7E45',
    '#FCD163',
    '#99B718',
    '#66A000',
    '#207401',
    '#056201',
    '#004C00',
    '#023B01',
    '#012E01'
]

# ---------------------------------------------------
# 4) Build Leafmap map
# ---------------------------------------------------
m = leafmap.Map(center=((top+bottom)/2, (left+right)/2), zoom=15)

# Add NDVI using the built-in leafmap.add_raster()
m.add_raster(
    tif_path,
    colormap=ndvi_colors,
    vmin=-1,
    vmax=1,
    layer_name="NDVI"
)

# ---------------------------------------------------
# 5) Add Legend
# ---------------------------------------------------
legend_dict = {
    "No vegetation (≤ 0.0)": "#FFFFFF",
    "0.0 – 0.1": "#CE7E45",
    "0.1 – 0.2": "#FCD163",
    "0.2 – 0.3": "#99B718",
    "0.3 – 0.4": "#66A000",
    "0.4 – 0.5": "#207401",
    "0.5 – 0.6": "#056201",
    "0.6 – 0.7": "#004C00",
    "0.7 – 0.8": "#023B01",
    "0.8 – 1.0": "#012E01",
}

m.add_legend(title="NDVI", legend_dict=legend_dict)

# ---------------------------------------------------
# 6) Display in Streamlit
# ---------------------------------------------------
m.to_streamlit(height=500)

# ---------------------------------------------------
# 7) NDVI Histogram
# ---------------------------------------------------
st.subheader("NDVI Histogram")
fig, ax = plt.subplots()
ax.hist(ndvi[np.isfinite(ndvi)], bins=50)
ax.set_xlabel("NDVI")
ax.set_ylabel("Pixel Count")
st.pyplot(fig)
