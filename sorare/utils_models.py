import os
import pickle

# Define the model categories and types (based on your file naming pattern)
positions = ['goalkeepers', 'defenders', 'midfielders', 'forwards']
model_types = ['xgb_model', 'lgbm_model', 'elastic_model']

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

models = {}
# Loop through positions and model types to load all models
def load_models():
    for position in positions:
        for model_type in model_types:
            # Construct the relative file path dynamically
            model_filename = f'{position}_{model_type}.pkl'
            model_path = os.path.join(script_dir, 'sorare_models', model_filename)
            
            # Load the model and store it in the dictionary
            with open(model_path, 'rb') as file:
                models[f'{position}_{model_type}'] = pickle.load(file)
                print(f"{position.capitalize()} {model_type.split('_')[0].upper()} Model loaded successfully!")
    return models