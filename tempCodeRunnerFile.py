
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(food_name)
seq = tokenizer.texts_to_sequences(food_name)