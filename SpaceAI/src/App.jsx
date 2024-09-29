import { useState } from 'react';
import './App.css';
import $ from 'jquery'; // Import jQuery

function App() {
  const [query, setQuery] = useState(''); // To store the input query
  const [data, setData] = useState(null); // To store the response data
  const [error, setError] = useState(null); // To store any errors

  // Function to handle API call using jQuery
  const handleQuery = () => {
    // Clear previous data and error
    setData(null);
    setError(null);

    // Send the query to the Python API
    $.ajax({
      url: 'http://127.0.0.1:5000/query',
      method: 'GET',
      data: { query }, // Send the query as data
      success: function(response) {
        console.log(response);
        setData(response.response); // Access the 'response' property
      },
      error: function(xhr, status, error) {
        console.error(status, error);
        setError('An error occurred while fetching data.'); // Set error state
      }
    });
  };

  return (
    <>
      <div className="input-container">
        <label htmlFor="QueryInput">Query</label>
        <input
          id="QueryInput"
          type="text"
          value={query} // Bind input to the query state
          onChange={(e) => setQuery(e.target.value)} // Update state on input change
        />
        <button onClick={handleQuery}>Submit Query</button>
      </div>

      <div className="response-container">
        {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error message */}
        {data && (
          <div id="ResponseDiv">
            <h3>Response:</h3>
            <p id="Response">{data}</p> {/* Display the response */}
          </div>
        )}
      </div>
    </>
  );
}

export default App;
