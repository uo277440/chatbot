import React, { useState, useContext } from 'react';
import axios from 'axios';
import AuthContext from './AuthContext';


function AdminView() {
  const [file, setFile] = useState(null);
  const { currentUser, setCurrentUser } = useContext(AuthContext)
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };
  const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true
});
  const handleUpload = () => {
    const formData = new FormData();
    formData.append('json_file', file);

    axiosInstance.post('/api/upload_json', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
        alert('El JSON se ha subido correctamente');
    })
    .catch(error => {
        alert('Ha habido un error durante la subida del archivo');
    });
  };

  return (
    <div>
      <h2>Admin View</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

export default AdminView;
