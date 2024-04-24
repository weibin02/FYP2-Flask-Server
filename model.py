import pandas as pd
import numpy as np

from category_encoders import OrdinalEncoder, OneHotEncoder

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Conv1D, AveragePooling1D, Dense

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

import seaborn as sns
import matplotlib.pyplot as plt

import pickle

# Get the data
data = pd.read_excel('2022 data raw.xlsx', header=0)

# Drop unnecessary columns
data.drop(["DATE", "TIME", "COILNO", "APNNO", "ISEVERHOLD",
           "onhold", "CUSTNO", "INSPECTIONCODE",
           "DEF_A", "DEF_B", "DEF_C", "DEF_D", "DEF_E",
           "DEF_F", "LOC_F", "RATE_F", "AREA_F",
          "DEF_G", "LOC_G", "RATE_G", "AREA_G",
          "DEF_H", "LOC_H", "RATE_H", "AREA_H",
          "DEF_I", "LOC_I", "RATE_I", "AREA_I",
          "DEF_J", "LOC_J", "RATE_J", "AREA_J",], axis=1, inplace=True)

# Split LOCATION into LENGTH, WIDTH, and HEIGHT
data[['LOC_A_LENGTH', 'LOC_A_WIDTH', 'LOC_A_HEIGHT']] = data['LOC_A'].str.split("", expand=True).drop([0,4], axis=1)
data.drop("LOC_A", axis=1, inplace=True)
data[['LOC_B_LENGTH', 'LOC_B_WIDTH', 'LOC_B_HEIGHT']] = data['LOC_B'].str.split("", expand=True).drop([0,4], axis=1)
data.drop("LOC_B", axis=1, inplace=True)
data[['LOC_C_LENGTH', 'LOC_C_WIDTH', 'LOC_C_HEIGHT']] = data['LOC_C'].str.split("", expand=True).drop([0,4], axis=1)
data.drop("LOC_C", axis=1, inplace=True)
data[['LOC_D_LENGTH', 'LOC_D_WIDTH', 'LOC_D_HEIGHT']] = data['LOC_D'].str.split("", expand=True).drop([0,4], axis=1)
data.drop("LOC_D", axis=1, inplace=True)
data[['LOC_E_LENGTH', 'LOC_E_WIDTH', 'LOC_E_HEIGHT']] = data['LOC_E'].str.split("", expand=True).drop([0,4], axis=1)
data.drop("LOC_E", axis=1, inplace=True)

# Remove rows with unexpected value
data.drop(data[
    (data['LOC_A_LENGTH'] != "H") &
    (data['LOC_A_LENGTH'] != "U") &
    (data['LOC_A_LENGTH'] != "M") &
    (data['LOC_A_LENGTH'] != "V") &
    (data['LOC_A_LENGTH'] != "T") &
    (data['LOC_A_WIDTH'] != "W") &
    (data['LOC_A_WIDTH'] != "X") &
    (data['LOC_A_WIDTH'] != "C") &
    (data['LOC_A_WIDTH'] != "Y") &
    (data['LOC_A_WIDTH'] != "D") &
    (data['LOC_A_WIDTH'] != "A") &
    (data['LOC_A_WIDTH'] != "F") &
    (data['LOC_A_HEIGHT'] != "T") &
    (data['LOC_A_HEIGHT'] != "B") &
    (data['LOC_A_HEIGHT'] != "D") &
    (data['LOC_B_LENGTH'] != "H") &
    (data['LOC_B_LENGTH'] != "U") &
    (data['LOC_B_LENGTH'] != "M") &
    (data['LOC_B_LENGTH'] != "V") &
    (data['LOC_B_LENGTH'] != "T") &
    (data['LOC_B_WIDTH'] != "W") &
    (data['LOC_B_WIDTH'] != "X") &
    (data['LOC_B_WIDTH'] != "C") &
    (data['LOC_B_WIDTH'] != "Y") &
    (data['LOC_B_WIDTH'] != "D") &
    (data['LOC_B_WIDTH'] != "A") &
    (data['LOC_B_WIDTH'] != "F") &
    (data['LOC_B_HEIGHT'] != "T") &
    (data['LOC_B_HEIGHT'] != "B") &
    (data['LOC_B_HEIGHT'] != "D") &
    (data['LOC_C_LENGTH'] != "H") &
    (data['LOC_C_LENGTH'] != "U") &
    (data['LOC_C_LENGTH'] != "M") &
    (data['LOC_C_LENGTH'] != "V") &
    (data['LOC_C_LENGTH'] != "T") &
    (data['LOC_C_WIDTH'] != "W") &
    (data['LOC_C_WIDTH'] != "X") &
    (data['LOC_C_WIDTH'] != "C") &
    (data['LOC_C_WIDTH'] != "Y") &
    (data['LOC_C_WIDTH'] != "D") &
    (data['LOC_C_WIDTH'] != "A") &
    (data['LOC_C_WIDTH'] != "F") &
    (data['LOC_C_HEIGHT'] != "T") &
    (data['LOC_C_HEIGHT'] != "B") &
    (data['LOC_C_HEIGHT'] != "D") &
    (data['LOC_D_LENGTH'] != "H") &
    (data['LOC_D_LENGTH'] != "U") &
    (data['LOC_D_LENGTH'] != "M") &
    (data['LOC_D_LENGTH'] != "V") &
    (data['LOC_D_LENGTH'] != "T") &
    (data['LOC_D_WIDTH'] != "W") &
    (data['LOC_D_WIDTH'] != "X") &
    (data['LOC_D_WIDTH'] != "C") &
    (data['LOC_D_WIDTH'] != "Y") &
    (data['LOC_D_WIDTH'] != "D") &
    (data['LOC_D_WIDTH'] != "A") &
    (data['LOC_D_WIDTH'] != "F") &
    (data['LOC_D_HEIGHT'] != "T") &
    (data['LOC_D_HEIGHT'] != "B") &
    (data['LOC_D_HEIGHT'] != "D") &
    (data['LOC_E_LENGTH'] != "H") &
    (data['LOC_E_LENGTH'] != "U") &
    (data['LOC_E_LENGTH'] != "M") &
    (data['LOC_E_LENGTH'] != "V") &
    (data['LOC_E_LENGTH'] != "T") &
    (data['LOC_E_WIDTH'] != "W") &
    (data['LOC_E_WIDTH'] != "X") &
    (data['LOC_E_WIDTH'] != "C") &
    (data['LOC_E_WIDTH'] != "Y") &
    (data['LOC_E_WIDTH'] != "D") &
    (data['LOC_E_WIDTH'] != "A") &
    (data['LOC_E_WIDTH'] != "F") &
    (data['LOC_E_HEIGHT'] != "T") &
    (data['LOC_E_HEIGHT'] != "B") &
    (data['LOC_E_HEIGHT'] != "D")
].index, inplace = True)

# Convert all letters to uppercase
data['LOC_A_LENGTH'] = data['LOC_A_LENGTH'].str.upper()

# drop row that contains null value
data = data.dropna(axis=0)

# drop rows that contain target value 5
data.drop(data[data['INSPDISP'] == 5].index, inplace = True)

# Preprocess label column (R --> 4)
data.loc[data['INSPDISP'] == 'R', 'INSPDISP'] = 4

# Make label start from index 0 for cross entropy to work
data['INSPDISP'] = data['INSPDISP'] - 1

# Preprocess RATE Column L, M, H --> 0, 1, 2
data = OrdinalEncoder(cols=['RATE_A','RATE_B','RATE_C','RATE_D','RATE_E']).fit(data).transform(data)

# Split into input and target
X = data.drop("INSPDISP", axis="columns")
y = pd.DataFrame(data.INSPDISP)

# Feature Scaling (MinMaxScaler)
cols = ['RATE_A', 'AREA_A','RATE_B', 'AREA_B','RATE_C', 'AREA_C','RATE_D', 'AREA_D','RATE_E', 'AREA_E']
mmSc = MinMaxScaler()
X[cols] = mmSc.fit_transform(X[cols])
X_scaled = X

# Preprocess LOC columns (One-Hot Encoder)
onehot_X = OneHotEncoder(
    cols=['LOC_A_LENGTH', 'LOC_B_LENGTH', 'LOC_C_LENGTH', 'LOC_D_LENGTH', 'LOC_E_LENGTH',
         'LOC_A_WIDTH', 'LOC_B_WIDTH', 'LOC_C_WIDTH', 'LOC_D_WIDTH', 'LOC_E_WIDTH',
         'LOC_A_HEIGHT', 'LOC_B_HEIGHT', 'LOC_C_HEIGHT', 'LOC_D_HEIGHT', 'LOC_E_HEIGHT'],
    use_cat_names=True).fit(X_scaled).transform(X_scaled)

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(onehot_X, y, test_size=0.33, random_state=1)

# Instantiate the model
model = Sequential()
model.add(Conv1D(filters=6, kernel_size=5, activation='tanh', input_shape=(85,1)))
model.add(AveragePooling1D(pool_size=2, strides=2))

model.add(Conv1D(filters=16, kernel_size=5, activation='tanh'))
model.add(AveragePooling1D(pool_size=2, strides=2))

model.add(Conv1D(filters=120, kernel_size=5, activation='tanh'))

model.add(Flatten())

model.add(Dense(units=84, activation='tanh'))
model.add(Dense(units=4, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

X_train = np.asarray(X_train).astype(np.float32)
y_train = np.asarray(y_train).astype(np.float32)
X_test = np.asarray(X_test).astype(np.float32)
y_test = np.asarray(y_test).astype(np.float32)

# Fit the model
model.fit(X_train, y_train, batch_size=16,epochs=20, verbose=1)

# Make pickle file of our model
# pickle.dump(model, open("model.pkl", "wb"))

# model evaluation
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
print(f"Test Accuracy: {test_accuracy*100:.2f}%")

# Predict the test set labels
y_pred = np.argmax(model.predict(X_test), axis=-1)

# Generate classification report
class_names = ['Class 1', 'Class 2', 'Class 3', 'Class 4']
print(classification_report(y_test, y_pred, target_names=class_names))

# Compute confusion matrix
conf_mat = confusion_matrix(y_test, y_pred)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()
