import tensorflow as tf

MODEL_PATH = "agro_adviser_model/agro_advise_v2_final.keras"

print("Loading ML model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully")