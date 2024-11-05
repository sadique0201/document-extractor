import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error uploading the file', error);
    }
  };

  return (
    <div className="App">
      <h1>Document Data Extractor</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {result && (
        <div>
          <h2>Extracted Information</h2>
          <p><strong>Name:</strong> {result.Name}</p>
          <p><strong>Document Number:</strong> {result['Document Number']}</p>
          <p><strong>Expiration Date:</strong> {result['Expiration Date']}</p>
        </div>
      )}
    </div>
  );
}

export default App;
