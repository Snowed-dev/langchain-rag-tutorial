from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from query_data import querydata  # Ensure this is the correct path to your querydata function

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/query', methods=['GET'])
def get_query():
    # Get the query text from the query parameters
    text = request.args.get('query', default='What?', type=str)

    # Call your querydata function with the passed text
    response = querydata(text)  # Now this should return the response content as a string

    # Return the response content
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for easier debugging
