# Easy-GAN
easy gan library made with keras

# Example
```python
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow.keras as keras
import numpy as np
import matplotlib.pyplot as plt
from easygan import GAN

(x,y),(a,z) = keras.datasets.mnist.load_data()
x = x.reshape(47040000)
x = x.astype(np.float32)
x /= 255
x = x.reshape(3000,20,28,28,1)


gan = GAN(20,28,28,1)
gan.train(2, x,5,4)
```

# Example TipGAN
```python
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow.keras as keras
import numpy as np
import matplotlib.pyplot as plt
from easygan import TipGAN

gan =TipGAN()

print("What do you want to draw?")
draw = str(input())
print("How many epochs do you want?")
epochs = int(input())
print("How many intervals do you want?")
interval = int(input())
gan.draw(draw,epochs=epochs,interval=interval,save=True)
```

# Explanation of Example

You can see we sliced 60000 mnist train datas to 3000x20. 20 is our batch size. Batch size is meaning how many images can use at a train step.
Then GAN start plotting images when training. You will see plotted images look alike data images. Plotted images are predictions of image generator.
I hope you can understand other parts of example.

# Explanation of TipGAN

TipGAN takes data from internet and than try to draw that pictures in size of 50x50 grayscale. This is for now. I am going to make it for rgb images. Just wait.
