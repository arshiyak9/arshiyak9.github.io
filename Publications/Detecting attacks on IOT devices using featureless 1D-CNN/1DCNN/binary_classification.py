from __future__ import print_function
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import coremltools
from scipy import stats
import os
from IPython.display import display, HTML
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn import preprocessing

import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Reshape
from keras.layers import Conv1D, MaxPooling1D, GlobalAveragePooling1D
from keras.utils import np_utils
pd.options.display.float_format = '{:.1f}'.format
sns.set() # Default seaborn look and feel
plt.style.use('ggplot')
print('keras version ', keras.__version__)

#Call the dataset into a dataframe df.
df=pd.read_csv("packet_training.csv")
#df=pd.read_csv("flow_training.csv")
#df=pd.read_csv("session_training.csv")
#df=df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])

X=df
#Fill missing values with 0
X=X.fillna(0)
print(X['Label'].value_counts())
LABELS=list(X['Label'].unique())
#LABELS=['Malicious', 'Benign']
X=X.drop(columns=['Label', 'Type'])

#Column names
training_cols=X.columns
pd.options.mode.chained_assignment = None
for each in training_cols:
    print(each)
    X[each]=X[each]/X[each].max()

# Define column name of the label vector
LABEL = 'PacketEncoded'
# Transform the labels from String to Integer via LabelEncoder
le = preprocessing.LabelEncoder()
# Add a new column to the existing DataFrame with the encoded values
df[LABEL] = le.fit_transform(df['Label'].values.ravel())
Y=df[LABEL]

#Split the dataset into training and test sets
X_train, X_test, Y_train, Y_test= train_test_split(X, Y, test_size=0.2, random_state=41)

#create segments
def create_segments_and_labels(x_data, time_steps, step, y_data):
    N_FEATURES=120
    segments = []
    labels=[]
    for i in range(0,len(x_data)-time_steps, step):
        vs=x_data.values[i:i+time_steps]
        label=stats.mode(y_data[i:i+time_steps])[0][0]
        segments.append([vs])
        labels.append(label)
    reshaped_segments = np.asarray(segments, dtype= np.int64).reshape(-1, time_steps, N_FEATURES)
    labels = np.asarray(labels)
    return reshaped_segments, labels

TIME_PERIODS=20
STEP_DISTANCE=10
new_X_train,new_Y_train=create_segments_and_labels(X_train,TIME_PERIODS,STEP_DISTANCE,Y_train)
#new_X_train,new_Y_train=create_segments_and_labels(X,TIME_PERIODS,STEP_DISTANCE,Y)
print('new_X_train shape:', new_X_train.shape)
print('new_Y_train shape: ', new_Y_train.shape)
num_values, num_sensors = new_X_train.shape[1], new_X_train.shape[2]
num_classes=len(LABELS)

input_shape = (num_values*num_sensors)
y_train_hot = np_utils.to_categorical(new_Y_train, num_classes)
newest_X_train = new_X_train.reshape(new_X_train.shape[0], input_shape)

new_X_test,new_Y_test=create_segments_and_labels(X_test,TIME_PERIODS,STEP_DISTANCE,Y_test)
print('new_X_test shape:', new_X_test.shape)
print('input_shape:', input_shape)
print('new_Y_test shape: ', new_Y_test.shape)

y_test_hot = np_utils.to_categorical(new_Y_test, num_classes)
newest_X_test = new_X_test.reshape(new_X_test.shape[0], input_shape)

callbacks_list = [
    keras.callbacks.ModelCheckpoint(
        filepath='showAll_best_model.{epoch:02d}-{val_loss:.2f}.h5',
        monitor='val_loss', save_best_only=True),
    keras.callbacks.EarlyStopping(monitor='acc', patience=2)]

#Create layers
model_m = Sequential()
model_m.add(Reshape((TIME_PERIODS, num_sensors), input_shape=(input_shape,)))
model_m.add(Conv1D(64, 3, activation='relu', input_shape=(TIME_PERIODS, num_sensors)))
model_m.add(MaxPooling1D(5))
model_m.add(Conv1D(64, 3, activation='relu'))
model_m.add(GlobalAveragePooling1D())
model_m.add(Dense(num_classes, activation='sigmoid'))
print(model_m.summary())

model_m.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
BATCH_SIZE = 20
EPOCHS = 50
history = model_m.fit(newest_X_train,
                      y_train_hot,
                      batch_size=BATCH_SIZE,
                      epochs=EPOCHS,
                      callbacks=callbacks_list,
                      validation_split=0.2,
                      verbose=1)

###save the model
#model_m.save('session_label_classification_1dcnn_model.h5')
#from keras.models import load_model
#model = load_model('masked_malware_label_classification_1dcnn_model.h5')
score = model_m.evaluate(newest_X_test, y_test_hot, verbose=1)
print(score)
y_pred_train = model_m.predict(newest_X_train)
max_y_pred_train = np.argmax(y_pred_train, axis=1)
print(classification_report(new_Y_train, max_y_pred_train))

######Acccuracy graph ############
plt.figure(figsize=(6, 4))
plt.plot(history.history['acc'], color='#D95319', label='Accuracy of training data')
plt.plot(history.history['val_acc'], color='#0072BD', label='Accuracy of validation data')
plt.plot(history.history['loss'], color='#D95319', linestyle='--', label='Loss of training data')
plt.plot(history.history['val_loss'],color='#0072BD', linestyle='--', label='Loss of validation data')
#plt.title('All Headers for Malware Type')
#plt.ylabel('Accuracy and Loss')
#h7plt.xlabel('Training Epoch')
plt.ylim(0)
#plt.legend()
plt.savefig("binary_showAll_pcap.png")

y_pred_test = model_m.predict(newest_X_test)
max_y_pred_test = np.argmax(y_pred_test, axis=1)
max_y_test=np.argmax(y_test_hot, axis=1)

################ Confusion Matrix ################
matrix = metrics.confusion_matrix(max_y_test, max_y_pred_test)
cmn = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]
plt.figure(figsize=(6, 4))
sns.heatmap(matrix,cmap='coolwarm',linecolor='white',linewidths=1,xticklabels=LABELS, yticklabels=LABELS,
annot=True, fmt='d')
plt.title('Confusion Matrix of Packet Label')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.savefig("binary_showAll_Packet_confusion.png")
