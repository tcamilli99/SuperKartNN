
# Import necessary libraries
import joblib  # For loading the serialized preprocessor
import pandas as pd  # For data manipulation
import tensorflow as tf  # For loading the trained neural network
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize Flask app with a name
superkart_api = Flask("SuperKart")

# Load the fitted preprocessor and the trained neural network
preprocessor = joblib.load("superkart_preprocessor.joblib")
model = tf.keras.models.load_model("superkart_nn_model.keras")

# Columns the model expects, in the schema produced by model.py
FEATURE_COLUMNS = [
    'Product_Weight',
    'Product_Sugar_Content',
    'Product_Allocated_Area',
    'Product_MRP',
    'Store_Size',
    'Store_Location_City_Type',
    'Store_Type',
    'Product_Id_char',
    'Store_Age_Years',
    'Product_Type_Category',
]

# Define a route for the home page
@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart System"

# Define an endpoint to predict sales for a single product
@superkart_api.post('/v1/predict')
def predict_sales():
    # Get JSON data from the request
    data = request.get_json()

    # Extract relevant features from the input data
    sample = {col: data[col] for col in FEATURE_COLUMNS}

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Preprocess and predict using the trained neural network
    processed = preprocessor.transform(input_data)
    prediction = float(model.predict(processed).flatten()[0])

    # Return the prediction as a JSON response
    return jsonify({'Sales': prediction})

# Define an endpoint to predict sales for a batch of products
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Preprocess and predict for the batch data
    processed = preprocessor.transform(input_data[FEATURE_COLUMNS])
    predictions = model.predict(processed).flatten().tolist()

    # Create an output dictionary mapping row index to predicted sales
    output_dict = {str(i): round(pred, 2) for i, pred in enumerate(predictions)}

    return output_dict


# Run the Flask app in debug mode
if __name__ == '__main__':
    superkart_api.run(debug=True)
