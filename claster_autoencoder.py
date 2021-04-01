import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
import json
import utils as TG
import time
from keras.layers import Input, Dense, Reshape, Flatten, Dropout, multiply, GaussianNoise
from keras.layers import BatchNormalization, Activation, Embedding, ZeroPadding2D
from keras.layers import MaxPooling2D, merge
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras import losses
from keras.utils import to_categorical
import keras.backend as K



def similarity(vector1, vector2):
    return np.dot(vector1, vector2.T) / np.dot(np.linalg.norm(vector1, axis=0, keepdims=True), np.linalg.norm(vector2.T, axis=0, keepdims=True))

#def func_sort(ID):
#    if len(max_list) != 0:
#        for i in range(len(max_list)):
#            if ID not in G.keys():
#                    preds0 = max_list[i][1][0]
#                    #print (preds0, len(preds0))
#                    G[ID] = [max_list[i][0]]
#                    del max_list[i]
#            else:
#                try:
#                    preds1 = max_list[i][1][0]
#                    KEF = similarity(preds0, preds1)
#                    if KEF>tresh:
#                         G[ID].append(max_list[i][0])
#                         del max_list[i]
#                except IndexError: 
#                    if len(max_list) == 0:
#                         break
#                    ID += 1
#                    func_sort(ID)

#def func_rec(ID):
#    print (len(arr_list), len(arr.file), len(G.keys()))
#    for ix, i in enumerate(arr_list):
#        G[ID] = [arr.file[ix]]
#        del arr.file[ix]
#        del arr_list[ix]
#        for iix, ii in enumerate(arr_list):
#                KEF = similarity(i, ii)  
#                if KEF[0]>tresh:
#                   G[ID].append(arr.file[iix])
#                   del arr.file[iix]
#                   del arr_list[iix] 
#        ID += 1

file_arr_temp = open("out/file_arr_temp_v2.txt", "r")  
def get_batch():
    L = []
    for i in file_arr_temp:
            res = json.loads(i.split("\n")[0].split(";")[1])
            A = np.array(res)
            L.append(A)
            if len(L) == 32:
                yield np.array(L)
                L = []       

 

class AdversarialAutoencoder():
    def __init__(self):
        self.img_rows = 12
        self.img_cols = 48603
        #self.channels = 1
        self.img_shape = (self.img_rows, self.img_cols)
        self.latent_dim = 10

        optimizer = Adam(0.0002, 0.5)

        # Build and compile the discriminator
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='binary_crossentropy',
            optimizer=optimizer,
            metrics=['accuracy'])

        # Build the encoder / decoder
        self.encoder = self.build_encoder()
        self.decoder = self.build_decoder()

        img = Input(shape=self.img_shape)
        # The generator takes the image, encodes it and reconstructs it
        # from the encoding
        encoded_repr = self.encoder(img)
        reconstructed_img = self.decoder(encoded_repr)

        # For the adversarial_autoencoder model we will only train the generator
        self.discriminator.trainable = False

        # The discriminator determines validity of the encoding
        validity = self.discriminator(encoded_repr)

        # The adversarial_autoencoder model  (stacked generator and discriminator)
        self.adversarial_autoencoder = Model(img, [reconstructed_img, validity])
        self.adversarial_autoencoder.compile(loss=['mse', 'binary_crossentropy'],
            loss_weights=[0.999, 0.001],
            optimizer=optimizer)


    def build_encoder(self):
        # Encoder

        img = Input(shape=self.img_shape)

        h = Flatten()(img)
        h = Dense(128)(h)
        h = LeakyReLU(alpha=0.2)(h)
        h = Dense(128)(h)
        h = LeakyReLU(alpha=0.2)(h)
        mu = Dense(self.latent_dim)(h)
        log_var = Dense(self.latent_dim)(h)
        latent_repr = merge([mu, log_var],
                mode=lambda p: p[0] + K.random_normal(K.shape(p[0])) * K.exp(p[1] / 2),
                output_shape=lambda p: p[0])

        return Model(img, latent_repr)

    def build_decoder(self):

        model = Sequential()

        model.add(Dense(128, input_dim=self.latent_dim))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(128))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(np.prod(self.img_shape), activation='tanh'))
        model.add(Reshape(self.img_shape))

        model.summary()

        z = Input(shape=(self.latent_dim,))
        img = model(z)

        return Model(z, img)

    def build_discriminator(self):

        model = Sequential()

        model.add(Dense(128, input_dim=self.latent_dim))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(64))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(1, activation="sigmoid"))
        model.summary()

        encoded_repr = Input(shape=(self.latent_dim, ))
        validity = model(encoded_repr)

        return Model(encoded_repr, validity)

    def train(self, epochs, batch_size=128, sample_interval=50):

        # Load the dataset
        
        # Rescale -1 to 1
#        X_train = (X_train.astype(np.float32) - 127.5) / 127.5
#        X_train = np.expand_dims(X_train, axis=2)

        # Adversarial ground truths
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))

        for epoch in range(epochs):
            for i in get_batch():
                #print (i.shape) 
                # ---------------------
                #  Train Discriminator
                # ---------------------

                # Select a random batch of images
                #idx = np.random.randint(0, X_train.shape[0], batch_size)
                imgs = i#X_train[idx]

                latent_fake = self.encoder.predict(imgs)
                latent_real = np.random.normal(size=(batch_size, self.latent_dim))

                # Train the discriminator
                d_loss_real = self.discriminator.train_on_batch(latent_real, valid)
                d_loss_fake = self.discriminator.train_on_batch(latent_fake, fake)
                d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

                # ---------------------
                #  Train Generator
                # ---------------------

                # Train the generator
                g_loss = self.adversarial_autoencoder.train_on_batch(imgs, [imgs, valid])

                # Plot the progress
                print ("%d [D loss: %f, acc: %.2f%%] [G loss: %f, mse: %f]" % (epoch, d_loss[0], 100*d_loss[1], g_loss[0], g_loss[1]))

            # If at save interval => save generated image samples
            if epoch % sample_interval == 0:
                self.save_model()

#    def sample_images(self, epoch):
#        r, c = 5, 5

#        z = np.random.normal(size=(r*c, self.latent_dim))
#        gen_imgs = self.decoder.predict(z)

#        gen_imgs = 0.5 * gen_imgs + 0.5

#        fig, axs = plt.subplots(r, c)
#        cnt = 0
#        for i in range(r):
#            for j in range(c):
#                axs[i,j].imshow(gen_imgs[cnt, :,:,0], cmap='gray')
#                axs[i,j].axis('off')
#                cnt += 1
#        fig.savefig("images/mnist_%d.png" % epoch)
#        plt.close()

    def save_model(self):

        def save(model, model_name):
            model_path = "saved_model/%s.json" % model_name
            weights_path = "saved_model/%s_weights.hdf5" % model_name
            options = {"file_arch": model_path,
                        "file_weight": weights_path}
            json_string = model.to_json()
            open(options['file_arch'], 'w').write(json_string)
            model.save_weights(options['file_weight'])

        save(self.generator, "aae_generator")
        save(self.discriminator, "aae_discriminator")



if __name__ == "__main__":
#    p_open = TG.PRODUCT() #['Order_ID', 'Product_ID', 'Items_Count', 'Total_Amount', 'TotalDiscount']
#    product_arr = p_open.to_numpy()

##---------------------------------------------->
#    # Создаю словарь ID продуктов
#    ids_product = {}
#    vals_prod = np.unique(product_arr[:,1])
#    for ix, i in enumerate(vals_prod):
#        ids_product[i] = ix
#    num_ids = len(ids_product)
#    ids_product_order = TG.func_return(product_arr, 0)

###---------------------------------------------->    

#    o_open = TG.ORDER() #['Order_Id', 'Customer_Id', 'Items_Count', 'price_before_discount', 'Amount_Charged']  
#    order_arr = o_open.to_numpy()
#    ids_order = TG.func_return(order_arr, 1)

#    c_open = TG.CUSTOMER() #['Customer_Id', 'consent', 'join_club_success', 'Could_send_sms', 'Could_send_email']
#    customer_arr = c_open.to_numpy()
#    ids_customer = TG.func_return(customer_arr, 0)
#    print (num_ids, len(ids_customer))

##---------------------------------------------->
#    """
#    У меня есть вектор (48603, 1) в него ложу среднее кол во продуктов исходя из покупок
#    Нужно получить кол покупок для каждого пользователя
#    """
#    MZ = {'01':0, '02':1, '03':2, '04':3, '05':4, '06':5, '07':6, '08':7, '09':8, '10':9, '11':10, '12':11} 
#    ERROR = 0
#    user_data = {}
#    file_arr_temp = open("out/file_arr_temp_v2.txt", "w")
#    for i in ids_customer:
#        try:
#            Z = np.zeros((12, num_ids))
#            #print (Z.shape)
#            for p in ids_order[int(i)]:
#                o_id = order_arr[p][0]
#                order_date = order_arr[p][-1]
#                M = order_date.split(" ")[0].split("-")[1]
#                #print (i, order_arr[p], len(ids_product_order[o_id]), len(ids_order[int(i)]), order_date, M, Z[MZ[M],:].shape)
#                for g in ids_product_order[o_id]:
#                    Z[MZ[M], ids_product[product_arr[g][1]]] += 1
##                    print (product_arr[g].tolist())
##                print (product_arr[ids_product_order[o_id]].tolist())
##                print(order_arr[p].tolist())
##                print (sum(Z))
##                print ("..................................")
#            if sum(customer_arr[ids_customer[i], 1:-1][0]) == 3.0:
#                #print (customer_arr[ids_customer[i], 1:-1])
#                #user_data[i] = Z
#                
#                file_arr_temp.write(f"{i};{Z.tolist()}\n")
#        except KeyError:
#            ERROR += 1
#            pass
#    print (ERROR)
#    print (len(user_data))
#    file_arr_temp.close()

#    def read_file(block_size=1024): 
#        with open("out/file_arr_temp_v2.txt", 'rb') as f: 
#            while True: 
#                piece = f.read()
#                if piece: 
#                    yield piece 
#                else: 
#                    return

#    for piece in read_file():
#        print (piece)
        

                
    aae = AdversarialAutoencoder()
    aae.train(epochs=20000, batch_size=32, sample_interval=500)    
    

