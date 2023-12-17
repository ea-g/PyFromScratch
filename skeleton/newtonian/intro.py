import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# setup a time scale for ~3 seconds (90 frames)
t = np.linspace(0, 3, 90)

# Create other parameters to define motion
# fill here!

# create a plot for our object
fig, ax = plt.subplots()

# plot the initial position (use,)

def update(frame):
    # for each frame, update the data stored on each artist. (use .set_data())
    # return with ,
    pass 

ani = animation.FuncAnimation(fig=fig, func=update, frames=90, interval=33)
plt.show()
