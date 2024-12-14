import pandas as pd

# Load the original database from CSV file
data = pd.read_csv('recipes_with_images.csv')


def categorize_meals(title):
    title_lower = title.lower()

    if any(keyword in title_lower for keyword in ['egg', 'breakfast', 'toast', 'pancake', 'waffle', 'smoothie', 'cereal']):
        return 'Breakfast'
    elif any(keyword in title_lower for keyword in ['salad', 'sandwich', 'bowl', 'wrap', 'burger', 'quiche']):
        return 'Lunch'
    elif any(keyword in title_lower for keyword in ['roast', 'pasta', 'steak', 'curry', 'dinner', 'bake', 'lasagna']):
        return 'Dinner'
    elif any(keyword in title_lower for keyword in ['snack', 'cookie', 'brownie', 'muffin', 'chips', 'popcorn', 'bar']):
        return 'Snack'
    elif any(keyword in title_lower for keyword in ['cake', 'pie', 'ice cream', 'pudding', 'tart', 'dessert', 'chocolate']):
        return 'Dessert'
    else:
        # Default to closest category based on general associations
        # Order of preference: Kahvaltı > Tatlı > Atıştırmalık > Öğle Yemeği > Akşam Yemeği
        if 'cheese' in title_lower or 'eggplant' in title_lower:
            return 'Breakfast'
        elif 'sugar' in title_lower or 'sweet' in title_lower:
            return 'Dessert'
        elif 'blondie' in title_lower or 'chips' in title_lower:
            return 'Snack'
        elif 'soup' in title_lower or 'roll' in title_lower:
            return 'Lunch'
        else:
            return 'Dinner'

# Apply the new categorization to all titles
data['category'] = data['title'].apply(categorize_meals)

# Save the updated DataFrame to a new CSV file
output_path = 'categorized_recipes.csv'
data.to_csv(output_path, index=False)

