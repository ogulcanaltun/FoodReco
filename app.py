import gradio as gr
import pandas as pd
import tensorflow as tf
import torch
from recoalgorithms import bmh_hesapla, tdee_hesapla, makro_ihtiyac_hesapla, yemek_tuketimi_sorgula, kalan_ihtiyac_hesapla, filtreleme_ve_oneri

# Load models
keras_model = tf.keras.models.load_model("101_food_class_10_percent_saved_model.keras")
pytorch_model = torch.load("best.pt")
pytorch_model.eval()

# Load dataset
dataset = pd.read_csv("categorized_recipes.csv")

def predict_food(image):
    # Preprocess image for keras model
    keras_image = tf.image.resize(image, (224, 224)) / 255.0
    keras_prediction = keras_model.predict(keras_image[None, ...])[0]

    # Preprocess image for PyTorch model
    pytorch_image = torch.tensor(image).permute(2, 0, 1).unsqueeze(0).float() / 255.0
    pytorch_image = torch.nn.functional.interpolate(pytorch_image, size=(224, 224))
    pytorch_prediction = torch.softmax(pytorch_model(pytorch_image), dim=1).detach().numpy()[0]

    # Get top predictions
    keras_top = keras_prediction.argmax()
    pytorch_top = pytorch_prediction.argmax()
    keras_prob = keras_prediction[keras_top]
    pytorch_prob = pytorch_prediction[pytorch_top]

    return keras_top, keras_prob, pytorch_top, pytorch_prob

def calculate_remaining_needs(age, gender, weight, height, activity, image, category):
    # Calculate user's needs
    user_info = {"yas": age, "cinsiyet": gender, "kilo": weight, "boy": height, "aktivite_durumu": activity}
    bmh = bmh_hesapla(user_info)
    tdee = tdee_hesapla(bmh, user_info["aktivite_durumu"])
    needs = makro_ihtiyac_hesapla(tdee, gender, weight, age)

    # Predict food
    keras_top, keras_prob, pytorch_top, pytorch_prob = predict_food(image, category)
    selected_prediction = keras_top if keras_prob > pytorch_prob else pytorch_top

    # Get food nutrition values
    food_name = dataset.iloc[selected_prediction]['title']
    portion = 1  # Default portion value
    food_values = yemek_tuketimi_sorgula(dataset, food_name.lower(), portion)

    if food_values:
        remaining_needs = kalan_ihtiyac_hesapla(needs, food_values)
        recommendations = filtreleme_ve_oneri(dataset, category, remaining_needs)
        return remaining_needs, recommendations, keras_top, keras_prob, pytorch_top, pytorch_prob
    else:
        return "Food not found in dataset. Please check the input image.", None, None, None, None, None

# Gradio interface
def gradio_interface(age, gender, weight, height, activity, image, category):
    remaining_needs, recommendations, keras_top, keras_prob, pytorch_top, pytorch_prob = calculate_remaining_needs(
        age, gender, weight, height, activity, image, category
    )
    return {
        "Remaining Needs": remaining_needs,
        "Recommendations": recommendations.to_dict() if recommendations is not None else {},
        "Keras Prediction": f"Class {keras_top} with Probability {keras_prob:.2f}",
        "PyTorch Prediction": f"Class {pytorch_top} with Probability {pytorch_prob:.2f}",
    }

interface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Number(label="Age"),
        gr.Radio(["Male", "Female"], label="Gender"),
        gr.Number(label="Weight (kg)"),
        gr.Number(label="Height (cm)"),
        gr.Radio(["sedentary", "light", "moderate", "very", "extra"], label="Activity Level"),
        gr.Image(label="Food Image"),
        gr.Radio(["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"], label="Category"),
    ],
    outputs=[
        gr.JSON(label="Results")
    ],
)

interface.launch()
