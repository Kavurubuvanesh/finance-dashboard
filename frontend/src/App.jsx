import React, { useState, useEffect } from 'react';
import api from './api';
import TransactionList from './components/TransactionList';
import TransactionForm from './components/TransactionForm';
import UploadForm from './components/UploadForm'; // <--- IMPORT THIS

function App() {
  const [transactions, setTransactions] = useState([]);

  const fetchTransactions = async () => {
    try {
      const response = await api.get('/transactions/');
      setTransactions(response.data);
    } catch (error) {
      console.error("Error fetching transactions:", error);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  return (
    <div>
      <nav className='navbar navbar-dark bg-primary mb-4'>
        <div className='container-fluid'>
          <a className='navbar-brand' href='#'>Finance Dashboard</a>
        </div>
      </nav>

      <div className='container'>
        <div className="row">
            {/* Left Column: Manual Form */}
            <div className="col-md-6">
                <TransactionForm onTransactionAdded={fetchTransactions} />
            </div>

            {/* Right Column: Upload Form (NEW) */}
            <div className="col-md-6">
                <UploadForm onUploadSuccess={fetchTransactions} />
            </div>
        </div>

        <TransactionList transactions={transactions} />
      </div>
    </div>
  );
}

export default App;