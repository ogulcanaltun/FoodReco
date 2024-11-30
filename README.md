# 🍽️ FoodReco: Personalized Food Recommendation System  
**Recognizing food and making smart, personalized meal recommendations based on your nutritional needs!**

---

## 🌟 **Overview**
FoodReco is a web application designed to bring together cutting-edge AI and nutritional science. With the ability to recognize food from images, FoodReco tracks your nutritional intake and provides tailored meal recommendations based on your remaining dietary needs. Say goodbye to manual food tracking and hello to smarter, healthier choices!

---

## 🚀 **Features**
- **Food Recognition**: Identify food items in images using advanced deep learning models like ResNet, VGG16, or Inceptionv3.
- **Personalized Recommendations**: Suggest meals that align with your daily nutritional goals after accounting for food you've already consumed.
- **Seamless User Experience**: Built with Gradio for an intuitive and visually appealing interface.
- **Nutritional Accuracy**: Data sourced from trusted databases like USDA and Food101 for precise tracking.

---

## 🛠️ **How It Works**
1. **Upload a Food Image**: Simply upload a picture of your meal.  
2. **AI-Powered Recognition**: The system identifies the food using fine-tuned models trained on the enhanced Epicurious dataset.  
3. **Track Nutrition**: Automatically calculates your nutritional intake and remaining daily needs.  
4. **Meal Suggestions**: Recommends meals to meet your dietary requirements.  

---

## 🏗️ **Technical Architecture**
FoodReco's core design includes:
- **Frontend & Backend**: Gradio handles user interactions and processing seamlessly.  
- **Image Recognition**: Powered by TensorFlow or PyTorch, fine-tuned on curated datasets like Epicurious and Food101.  
- **Nutritional Database**: Incorporates reliable nutritional data from sources like USDA.  

![System Architecture](https://via.placeholder.com/800x400?text=System+Architecture+Diagram)

---

## 🗂️ **Dataset**
We use the [Epicurious dataset](https://www.kaggle.com/datasets/hugodarwood/epirecipes) enhanced with food images manually curated and supplemented with datasets like Food101.  

---

## 📈 **Challenges We Solved**
1. **Data Preparation**: Enhanced the Epicurious dataset with diverse food images to improve model accuracy.  
2. **Model Accuracy**: Leveraged transfer learning and added custom layers for improved recognition of mixed or unclear food images.  

---

## 📅 **Development Timeline**
| Week | Task                          | Description                          |
|------|-------------------------------|--------------------------------------|
| 1    | Data Collection               | Gathered datasets and resources.    |
| 2    | Data Preparation              | Curated and enhanced Epicurious.    |
| 3    | Model Training                | Fine-tuned pre-trained models.      |
| 4    | Backend Development           | Developed backend logic using Gradio.|
| 5    | Frontend Development          | Designed UI for image upload and recommendations. |
| 6    | Integration                   | Integrated frontend and backend.    |
| 7    | Testing                       | Conducted functional testing.       |
| 8    | Beta Testing                  | Collected user feedback for refinement. |

---

## 🔗 **Links**
- **GitHub Repository**: [FoodReco](https://github.com/ogulcanaltun/FoodReco)  
- **Epicurious Dataset**: [Download Here](https://www.kaggle.com/datasets/hugodarwood/epirecipes)  

---

## 💻 **Contributors**
- **Oğulcan Altun** | [GitHub](https://github.com/ogulcanaltun) | Gazi University  
- **Eda Dilek** | [GitHub](https://github.com/edadilek) | Gazi University  
- **Ahmet Karakuş** | [GitHub](https://github.com/casanovathoper) | Gazi University  

---

## 🏆 **Acknowledgments**
We extend our gratitude to the creators of Epicurious, USDA Food Composition Databases, and the Food101 dataset, as well as the developers of pre-trained models that power FoodReco.

---

## 📜 **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
