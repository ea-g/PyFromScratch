"""Sepia filter demo"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# convert to float
a = np.array(Image.open("./images/ein.jpg")).astype(float) / 255.0

# reweight and add up
b = np.dstack(
    (
        0.393 * a[:, :, 0] + 0.769 * a[:, :, 1] + 0.189 * a[:, :, 2],
        0.349 * a[:, :, 0] + 0.686 * a[:, :, 1] + 0.168 * a[:, :, 2],
        0.272 * a[:, :, 0] + 0.534 * a[:, :, 1] + 0.131 * a[:, :, 2],
    )
).clip(0, 1) # clip intensity, convert back to uint8
b = (b*255).astype(np.uint8)
plt.imshow(b)
plt.show()
