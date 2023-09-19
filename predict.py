import tensorflow as tf
import pandas as pd
import numpy as np
import os

# Set the batch size and sequence length
batch_size = 32
sequence_length = 20  # Adjust as needed

folder = r"C:\Users\richa\OneDrive\Documents\Kuliah\Coding Kuliah\Lifewell\LifeWell_Beneran\dataset"

filename = 'dish.csv'
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
file_path = os.path.join(folder, filename)
df = pd.read_csv(file_path, sep=',')
df['name'].fillna('UNKNOWN', inplace=True)
df = df['name']

food_name = df.to_list()
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(food_name)
seq = tokenizer.texts_to_sequences(food_name)

x = []
y = []

total_words_dropped = 0

for i in seq:
    if len(i) > 1:
        for index in range(1, len(i)):
            x.append(i[:index])
            y.append(i[index])
    else:
        total_words_dropped += 1

x = tf.keras.preprocessing.sequence.pad_sequences(x, maxlen=sequence_length)

vocab_size = len(tokenizer.word_index) + 1

# Create a TensorFlow Dataset for batch processing for x and y
dataset = tf.data.Dataset.from_tensor_slices((x, y)).batch(batch_size)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 14),
    tf.keras.layers.LSTM(100, return_sequences=True),
    tf.keras.layers.LSTM(100),
    tf.keras.layers.Dense(100, activation='relu'),
    tf.keras.layers.Dense(vocab_size, activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.004),
              loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model using the dataset
# model.fit(dataset, epochs=15)

model.save('my_model.keras')
vocab_array = np.array(list(tokenizer.word_index.keys()))


def make_prediction(text, n_words):
    for i in range(n_words):
        text_tokenize = tokenizer.texts_to_sequences([text])
        text_padded = tf.keras.preprocessing.sequence.pad_sequences(
            text_tokenize, maxlen=sequence_length)
        prediction = np.squeeze(np.argmax(model.predict(text_padded), axis=-1))
        prediction = vocab_array[prediction - 1]
        text += " " + prediction
    return text


# Example prediction
print(make_prediction("chicken", 3))
