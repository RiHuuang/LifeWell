# import tensorflow as tf
# import pandas as pd
# import numpy as np
# import os
# from collections import Counter

# # Define your folder and filenames
# folder = r"C:\Users\richa\OneDrive\Documents\Kuliah\Coding Kuliah\Lifewell\LifeWell_Beneran\dataset"
# # Add more filenames as needed
# filenames = ['dish2.csv', 'dish3.csv', 'dish4.csv']

# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# # Initialize the tokenizer
# tokenizer = tf.keras.preprocessing.text.Tokenizer()

# # Create a list to store sequences from all files
# all_sequences = []

# # Process each file separately and collect sequences
# for filename in filenames:
#     file_path = os.path.join(folder, filename)
#     df = pd.read_csv(file_path, sep=',')
#     df['name'].fillna('UNKNOWN', inplace=True)
#     df = df['name']

#     food_name = df.to_list()

#     # Update tokenizer with the data from each file
#     tokenizer.fit_on_texts(food_name)

#     # Prepare the sequences
#     seq = tokenizer.texts_to_sequences(food_name)
#     all_sequences.extend(seq)

# # Prepare x and y from all sequences
# x = []
# y = []

# total_words_dropped = 0

# for i in all_sequences:
#     if len(i) > 1:
#         for index in range(1, len(i)):
#             x.append(i[:index])
#             y.append(i[index])
#     else:
#         total_words_dropped += 1

# # Reduce vocabulary size
# word_counts = Counter(y)
# threshold = 25  # Adjust as needed
# filtered_words = [word for word, count in word_counts.items()
#                   if count >= threshold]
# word_to_index = {word: index for index, word in enumerate(filtered_words)}
# index_to_word = {index: word for word, index in word_to_index.items()}

# # Initialize an OOV token index
# oov_token_index = len(filtered_words)  # Assign a unique index for OOV words

# # Create a function to map words to indices or the OOV token


# def word_to_index_with_oov(word):
#     return word_to_index.get(word, oov_token_index)


# # Replace y with the reduced vocabulary or OOV token index
# y = [word_to_index_with_oov(word) for word in y]

# # Ensure that OOV token index is included in the vocabulary size
# vocab_size = len(filtered_words) + 1  # +1 for the OOV token

# x = tf.keras.preprocessing.sequence.pad_sequences(x)
# y = tf.keras.utils.to_categorical(y, num_classes=vocab_size)

# x = x.reshape(-1, x.shape[1], 1)

# # Create a TensorFlow Dataset for batch processing
# batch_size = 32
# dataset = tf.data.Dataset.from_tensor_slices((x, y)).batch(batch_size)

# model = tf.keras.Sequential([
#     tf.keras.layers.Embedding(vocab_size, 14),
#     tf.keras.layers.LSTM(100, return_sequences=True),
#     tf.keras.layers.LSTM(100),
#     tf.keras.layers.Dense(100, activation='relu'),
#     tf.keras.layers.Dense(vocab_size, activation='softmax')
# ])

# model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.004),
#               loss='categorical_crossentropy', metrics=['accuracy'])
# model.fit(dataset, epochs=150)

# model.save('my_model.keras')
# vocab_array = np.array(list(filtered_words))


# def make_prediction(text, n_words):
#     for i in range(n_words):
#         text_tokenize = tokenizer.texts_to_sequences([text])
#         text_padded = tf.keras.preprocessing.sequence.pad_sequences(
#             text_tokenize, maxlen=14)
#         prediction = np.squeeze(np.argmax(model.predict(text_padded), axis=-1))

#         # Handle OOV token index
#         if prediction == oov_token_index:
#             prediction_word = "OOV_WORD"  # Replace with an appropriate OOV token or handling
#         else:
#             prediction_word = vocab_array[prediction - 1]

#         text += " " + prediction_word
#     return text


# # Example prediction
# print(make_prediction("mushroom", 1))

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
model.fit(dataset, epochs=10)

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
print(make_prediction("mushroom", 1))
