import React, { useState } from 'react';
import api from '../api';

const UploadForm = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            await api.post('/transactions/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            alert('Upload Successful!');
            onUploadSuccess(); // Refresh the list
        } catch (error) {
            console.error('Upload failed:', error);
            alert('Upload failed');
        }
    };

    return (
        <div className="card mb-4">
            <div className="card-header">Import Transactions (CSV)</div>
            <div className="card-body">
                <form onSubmit={handleUpload} className="d-flex gap-2">
                    <input
                        type="file"
                        accept=".csv"
                        className="form-control"
                        onChange={handleFileChange}
                    />
                    <button type="submit" className="btn btn-success">
                        Upload
                    </button>
                </form>
                <small className="text-muted">
                    Format: date, amount, category, description, is_income
                </small>
            </div>
        </div>
    );
};

export default UploadForm;