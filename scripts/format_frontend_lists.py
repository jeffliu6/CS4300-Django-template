import json

medical_effects = ["Cramps", "Depression", "Eye Pressure", "Fatigue", "Headaches",
    "Inflammation", "Insomnia", "Lack of Appetite", "Muscle Spasms", "Nausea",
    "Pain", "Seizures", "Spasticity", "Stress"]
    
desired_effects = ["Aroused", "Creative", "Energetic", "Euphoric", "Focused", 
    "Giggly", "Happy", "Hungry", "Relaxed", "Sleepy", "Talkative", "Tingly", "Uplifted"]

undesired_effects = ["Anxious", "Dizzy", "Dry Eyes", "Dry Mouth", "Headache", "Paranoid"]

flavors = ["Apple", "Berry", "Blueberry", "Bubble Gum", "Buttery", "Candy", "Caramel",
    "Cheesy", "Chemical", "Cherry", "Chocolate", "Citrus", "Coffee", "Creamy",
    "Dank", "Diesel", "Flowery", "Fruity", "Grape", "Grapefruit", "Hash",
    "Herbal", "Honey", "Lavender", "Lemon", "Lime", "Mango", "Menthol", "Mint",
    "Nutty", "Orange", "Peppery", "Pine", "Pineapple", "Sage", "Skunky", "Sour",
    "Spicy", "Strawberry", "Sugary", "Sweet", "Tangy", "Tea", "Tobacco",
    "Tropical", "Vanilla", "Woody"]

aromas = ["Apple", "Banana", "Berry", "Blueberry", "Bubble Gum", "Candy", "Caramel",
    "Cheese", "Chemical", "Cherry", "Chocolate", "Citrus", "Coffee", "Creamy",
    "Dank", "Diesel", "Earthy", "Floral", "Flowery", "Fragrant", "Fruity", "Fuel",
    "Grape", "Grapefruit", "Grassy", "Harsh", "Hash", "Herbal", "Kush",
    "Lavender", "Lemon", "Lime", "Mango", "Mellow", "Mint", "Musky", "Nutty",
    "Orange", "Pepper", "Pine", "Pineapple", "Pungent", "Sage", "Skunky", "Sour",
    "Spicy", "Strawberry", "Sweet", "Tropical", "Vanilla", "Woody"]
   
def low(word):
    return word.lower()

data = {}
data["medical_effects"] = list(map(low, medical_effects))
data["desired_effects"] = list(map(low, desired_effects))
data["undesired_effects"] = list(map(low, undesired_effects))
data["flavors"] = list(map(low, flavors))
data["aromas"] = list(map(low, aromas))

def get_medical(word):
    return {
        "id": data["medical_effects"].index(word.lower()),
        "text": word
    }

def get_desired(word):
    return {
        "id": data["desired_effects"].index(word.lower()),
        "text": word
    }

def get_undesired(word):
    return {
        "id": data["undesired_effects"].index(word.lower()),
        "text": word
    }

def get_flavor(word):
    return {
        "id": data["flavors"].index(word.lower()),
        "text": word
    }

def get_aroma(word):
    return {
        "id": data["aromas"].index(word.lower()),
        "text": word
    }
data["select"] = {}
data["select"]["medical_effects"] = list(map(get_medical, medical_effects))
data["select"]["desired_effects"] = list(map(get_desired, desired_effects))
data["select"]["undesired_effects"] = list(map(get_undesired, undesired_effects))
data["select"]["flavors"] = list(map(get_flavor, flavors))
data["select"]["aromas"] = list(map(get_aroma, aromas))

with open('../Mariwanna/static/data/select-options.json', 'w') as outfile:
    json.dump(data, outfile)
