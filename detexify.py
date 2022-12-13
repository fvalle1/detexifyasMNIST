# %%
import psycopg
import os

# %%
dbfile = "detexify.sql"

# %%
import json
import plotly.express as px
import plotly.graph_objects as go
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

# %%
with open("symbols.json", "r") as f:
    symbols = json.load(f)

# %%
symbols[1]

# %%
io = open("detexify.sql", "r")
for i in range(77): #skip unuseful lines
    io.readline()

# %%
def parse_stroke(strokes):
    return [[(x[0],x[1]) for x in stroke] for stroke in json.loads(strokes)]

def parse_image(strokes, nbins=25, pad=50):
    data = np.concatenate(strokes)
    bins_x = np.linspace(data[:,0].min()-pad, data[:,0].max()+pad, nbins+1)
    bins_y = np.linspace(data[:,1].min()-pad, data[:,1].max()+pad, nbins+1)
    image = np.histogram2d([x for x,y in data], 
                            [y for x,y in data],
                            bins=[bins_x,bins_y])[0].T
    image = tf.reshape(image, (nbins,nbins,1))
    image = tf.keras.preprocessing.image.smart_resize(image, (28,28))
    return image

def parse_line(line):
    line = line.split("\t")
    strokes = parse_stroke(line[2])
    image = parse_image(strokes)
    return line[1], strokes, image

# %%
parsed = parse_line(io.readline())
fig = go.Figure()
fig.add_traces([
                go.Scatter(x = [x for x,y in stroke], y = [500-y for x,y in stroke], mode="lines")
                for stroke in parsed[1]
                ])
fig.update_layout({"title":parsed[0]})

# %%
image = parsed[2]
plt.imshow(image[:,:,0],
           cmap="Greys")

# %%
X = []
y = []
for i in range(50000):
    if (i%100==0):
        print(i)
    label, _, image = parse_line(io.readline())
    X.append(image)
    y.append(label)

# %%
np.savetxt("X_detexify.txt", tf.reshape(X, (-1,28*28)))
labels, y = np.unique(y, return_inverse=True)
np.savetxt("y_detexify.txt", y, fmt="%d")
np.savetxt("labels_detexify.txt", labels, fmt="%s")

# %%
fig, axs = plt.subplots(2,5, figsize=(18,8))
for ax in axs.ravel():
    i = np.random.randint(0,np.shape(X)[0])
    ax.imshow(X[i][:,:,0], cmap="gray")
    ax.set_title(labels[y[i]])
plt.show()

# %%
plt.hist(np.unique(y, return_counts=True)[1], bins=np.linspace(0,100,50))

plt.show()

# %%



