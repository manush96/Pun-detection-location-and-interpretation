from __future__ import print_function

import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import Conv1D, MaxPooling1D, Embedding,LSTM
from keras.models import Model
from keras.utils import plot_model
embeddings_index = {}
import matplotlib.pyplot as plt

MAX_SEQUENCE_LENGTH = 100
MAX_NUM_WORDS = 20000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.2
TEST_SPLIT=0.2


#replace with Glove vectors path
with open("/media/manush96/wayne/glove.6B.100d.txt") as f:
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs

print('Found %s word vectors.' % len(embeddings_index))


file=open("raw_sent1.txt","r")

data=file.read()

docs=data.split("\n")
docs=docs[:2250]
texts = docs  # list of text samples
labels_index = {"0":0,"1":1}  # dictionary mapping label name to numeric id
file1=open("lables.txt","r")
data=file1.read()
labels=eval(data)
tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)


word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

labels = to_categorical(np.asarray(labels))



indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]
num_validation_samples = 450
print(num_validation_samples)
num_test_samples=int(TEST_SPLIT * data.shape[0])
x_train = data[:-900]
y_train = labels[:-900]
x_val = data[-900:-450]
y_val = labels[-900:-450]
x_test=data[-450:]
y_test=labels[-450:]






# prepare embedding matrix
num_words = min(MAX_NUM_WORDS, len(word_index) + 1)
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if i >= MAX_NUM_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector




embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

print('Training model.')

# train a 1D convnet with global maxpooling
sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sequence_input)
x=LSTM(100,return_sequences=True)(embedded_sequences)
x = Conv1D(128, 5, activation = 'relu') (x)
x = Conv1D(128, 5, activation='relu')(x)
x = GlobalMaxPooling1D()(x)

preds = Dense(len(labels_index), activation='softmax')(x)

model = Model(sequence_input, preds)
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['acc'])

history=model.fit(x_train, y_train,
          batch_size=128,
          epochs=40,
          validation_data=(x_val, y_val),verbose=1)
accuracy=model.evaluate(x_test,y_test)
print(accuracy)
plot_model(model,to_file="model.png")
print(history.history.keys())


# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
