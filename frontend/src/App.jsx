import React, { useState, useEffect } from 'react';
import api from './api';
import TransactionList from './components/TransactionList';
import TransactionForm from './components/TransactionForm';
import UploadForm from './components/UploadForm';
import SummaryChart from './components/SummaryChart'; // <--- NEW IMPORT

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

        {/* TOP ROW: Forms and Chart */}
        <div className="row mb-4">
            {/* Left Column: Forms */}
            <div className="col-md-6">
                <TransactionForm onTransactionAdded={fetchTransactions} />
                <UploadForm onUploadSuccess={fetchTransactions} />
            </div>

            {/* Right Column: Chart (NEW) */}
            <div className="col-md-6">
                <SummaryChart transactions={transactions} />
            </div>
        </div>

        {/* BOTTOM ROW: Table */}
        <TransactionList transactions={transactions} />
      </div>
    </div>
  );
}

export default App;