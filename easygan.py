import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow.keras as keras
import numpy as np
import matplotlib.pyplot as plt


class GAN():
    def __init__(self, batch_size, image_width, image_height, image_channels):
        self.batch_size = batch_size
        self.width = image_width
        self.height = image_height
        self.channels = image_channels

        self.generator = self.build_generator()
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(optimizer="adam", loss="binary_crossentropy", metrics="accuracy")
        self.discriminator.trainable = False
        combine_in = keras.layers.Input(shape=(20))
        generated = self.generator(combine_in)
        combine_out = self.discriminator(generated)
        self.combined = keras.Model(combine_in, combine_out)
        self.combined.compile(optimizer="adam", loss="binary_crossentropy")

    def build_generator(self):
        generator = keras.models.Sequential([
            keras.layers.Dense(256, input_dim=20),
            keras.layers.LeakyReLU(0.2),
            keras.layers.BatchNormalization(momentum=0.8),
            keras.layers.Dense(512),
            keras.layers.LeakyReLU(0.2),
            keras.layers.BatchNormalization(momentum=0.8),
            keras.layers.Dense(1024),
            keras.layers.LeakyReLU(0.2),
            keras.layers.BatchNormalization(momentum=0.8),
            keras.layers.Dense(np.prod((self.width, self.height, self.channels)), activation="sigmoid"),
            keras.layers.Reshape((self.width, self.height, self.channels))
        ])

        return generator

    def build_discriminator(self):
        discriminator = keras.models.Sequential([
            keras.layers.Flatten(input_shape=(self.width, self.height, self.channels)),
            keras.layers.Dense(512),
            keras.layers.LeakyReLU(0.2),
            keras.layers.Dense(256),
            keras.layers.LeakyReLU(0.2),
            keras.layers.Dense(1, activation="sigmoid")
        ])

        return discriminator

    def train(self, epochs, data):
        epoches = 0
        fig = plt.figure()
        for epoch in range(epochs):

            for images in data:
                seed = np.random.normal(0, 1, (self.batch_size, 20))
                images = images.reshape(self.batch_size, self.width, self.height, self.channels)

                fake_images = self.generator.predict(seed)

                fake_images = fake_images.reshape(self.batch_size, self.width, self.height, self.channels)

                self.discriminator.train_on_batch(fake_images, np.zeros((self.batch_size, 1)))
                self.discriminator.train_on_batch(images, np.ones((self.batch_size, 1)))
                self.combined.train_on_batch(seed, np.ones((self.batch_size, 1)))
                epoches += 1
                print(epoches)
                if epoches % 100 == 0:
                    seed = np.random.normal(0, 1, (5, 20))
                    fake_images = self.generator.predict(seed)
                    fake_images = fake_images.reshape(5, self.width, self.height, self.channels)

                    for n in range(5):
                        img = fake_images[n]
                        img = img.reshape(self.width, self.height, self.channels)
                        plt.subplot(1, 5, n + 1)
                        plt.imshow(img)
                    plt.draw()
                    plt.pause(0.1)
                    fig.clear()

class SuperGAN():
    def __init__(self, batch_size, image_width, image_height, image_channels):
        self.batch_size = batch_size
        self.width = image_width
        self.height = image_height
        self.channels = image_channels

        self.discriminator = self.build_discriminator()
        self.generator = self.build_generator()

        self.discriminator.compile(optimizer="adam", loss="binary_crossentropy", metrics="accuracy")
        self.discriminator.trainable = False
        combine_in = keras.layers.Input(shape=(20))
        generated = self.generator(combine_in)
        combine_out = self.discriminator(generated)
        self.combined = keras.Model(combine_in, combine_out)
        self.combined.compile(optimizer="adam", loss="binary_crossentropy")

    def build_generator(self):
        generator = keras.models.Sequential([
            keras.layers.Dense(8 * 8 * 4),
            keras.layers.Reshape((8, 8, 4)),
            keras.layers.Conv2DTranspose(64, kernel_size=4, strides=2, padding="same"),
            keras.layers.LeakyReLU(alpha=0.2),
            keras.layers.Conv2DTranspose(64, kernel_size=4, strides=2, padding="same"),
            keras.layers.LeakyReLU(alpha=0.2),
            keras.layers.Conv2DTranspose(64, kernel_size=4, strides=2, padding="same"),
            keras.layers.LeakyReLU(alpha=0.2),
            keras.layers.Conv2D(3, kernel_size=4, padding="same"),
            keras.layers.Flatten(),
            keras.layers.LeakyReLU(alpha=0.2),
            keras.layers.Dense(np.prod((self.width, self.height, self.channels)), activation="sigmoid"),
            keras.layers.Reshape((self.width, self.height, self.channels))
        ])
        return generator

    def build_discriminator(self):
        discriminator = keras.models.Sequential([
            keras.Input(shape=(self.width, self.height, self.channels)),
            keras.layers.Flatten(),
            keras.layers.Dense(8*8*8),
            keras.layers.Reshape((8,8,8)),
            keras.layers.LeakyReLU(alpha=0.2),
            keras.layers.Conv2D(64, kernel_size=4, strides=2, padding="same"),
            keras.layers.LeakyReLU(alpha=0.2),
            keras.layers.Conv2D(64, kernel_size=4, strides=2, padding="same"),
            keras.layers.LeakyReLU(alpha=0.2),
            keras.layers.Flatten(),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(1, activation="sigmoid"),
        ])

        return discriminator

    def train(self, epochs, data):
        epoches = 0
        fig = plt.figure()
        for epoch in range(epochs):

            for images in data:
                seed = np.random.normal(0, 1, (self.batch_size, 20))
                images = images.reshape(self.batch_size, self.width, self.height, self.channels)

                fake_images = self.generator.predict(seed)

                fake_images = fake_images.reshape(self.batch_size, self.width, self.height, self.channels)

                self.discriminator.train_on_batch(fake_images, np.zeros((self.batch_size, 1)))
                self.discriminator.train_on_batch(images, np.ones((self.batch_size, 1)))
                self.combined.train_on_batch(seed, np.ones((self.batch_size, 1)))
                epoches += 1
                print(epoches)
                if epoches % 100 == 0:
                    seed = np.random.normal(0, 1, (5, 20))
                    fake_images = self.generator.predict(seed)
                    fake_images = fake_images.reshape(5, self.width, self.height, self.channels)

                    for n in range(25):
                        img = fake_images[n]
                        img = img.reshape(self.width, self.height, self.channels)
                        plt.subplot(5, 5, n + 1)
                        plt.imshow(img)
                    plt.draw()
                    plt.pause(0.1)
                    fig.clear()