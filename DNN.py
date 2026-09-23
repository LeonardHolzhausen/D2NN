import numpy as np
from tensorflow import keras
from keras import Model
from keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split

import dataset

# --- Data ---
d = dataset.Dataset(4000, image_size=16, seed=42)
X = np.array([s["image"] for s in d.dataset], dtype="float32")
X = X.reshape(-1, 16, 16, 1)                     # add the channel dimension Conv2D expects
y = np.array([s["label"] for s in d.dataset])    # integer labels 0-3

# Remove duplicates BEFORE splitting
_, unique_idx = np.unique(X.reshape(len(X), -1), axis=0, return_index=True)
X, y = X[unique_idx], y[unique_idx]
 
# Balance the classes
counts = np.bincount(y)
k = counts.min()
rng = np.random.default_rng(0)
keep = np.concatenate([rng.choice(np.where(y == c)[0], k, replace=False)
                       for c in range(4)])
X, y = X[keep], y[keep]
print(f"{len(X)} images after dedup + balancing ({k} per class)")
 
X = X.reshape(-1, 16, 16, 1)                     # add the channel dimension Conv2D expects

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Model ---
inputs = Input(shape=(16, 16, 1))

x = Conv2D(16, 3, activation="relu", padding="same")(inputs)
x = Conv2D(16, 3, activation="relu", padding="same")(x)
x = Conv2D(16, 3, activation="relu", padding="same")(x)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Conv2D(32, 3, activation="relu", padding="same")(x)
x = Conv2D(32, 3, activation="relu", padding="same")(x)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Conv2D(64, 3, activation="relu", padding="same")(x)
x = MaxPooling2D(pool_size=(2, 2))(x)

x = Flatten()(x)
x = Dense(64, activation="relu")(x)
predictions = Dense(4, activation="softmax")(x)

model = Model(inputs=inputs, outputs=predictions)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

early_stop = keras.callbacks.EarlyStopping(patience=8, restore_best_weights=True)

history = model.fit(
    X_train, y_train,
    epochs=500,
    validation_split=0.2,
    callbacks=[early_stop],
    verbose=1
)

test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Held-out test accuracy: {test_acc:.4f}")