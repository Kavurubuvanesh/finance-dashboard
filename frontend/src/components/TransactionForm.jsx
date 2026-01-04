import React, { useState } from 'react';
import api from '../api';

const TransactionForm = ({ onTransactionAdded }) => {
  const [formData, setFormData] = useState({
    amount: '',
    category: '',
    description: '',
    is_income: false,
    date: new Date().toISOString().split('T')[0]
  });

  const handleInputChange = (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      await api.post('/transactions/', formData);
      // Notify parent component that data changed
      onTransactionAdded();
      // Reset form
      setFormData({
        amount: '',
        category: '',
        description: '',
        is_income: false,
        date: new Date().toISOString().split('T')[0]
      });
    } catch (error) {
      console.error("Error creating transaction:", error);
    }
  };

  return (
    <div className='card mb-4'>
      <div className='card-header'>Add New Transaction</div>
      <div className='card-body'>
        <form onSubmit={handleFormSubmit}>
          <div className='mb-3'>
            <label className='form-label'>Amount</label>
            <input type='number' name='amount' className='form-control' onChange={handleInputChange} value={formData.amount} required />
          </div>
          <div className='mb-3'>
            <label className='form-label'>Category</label>
            <input type='text' name='category' className='form-control' onChange={handleInputChange} value={formData.category} required />
          </div>
          <div className='mb-3'>
            <label className='form-label'>Description</label>
            <input type='text' name='description' className='form-control' onChange={handleInputChange} value={formData.description} />
          </div>
          <div className='mb-3 form-check'>
            <input type='checkbox' name='is_income' className='form-check-input' onChange={handleInputChange} checked={formData.is_income} id="incomeCheck"/>
            <label className='form-check-label' htmlFor="incomeCheck">Is this Income?</label>
          </div>
          <div className='mb-3'>
            <label className='form-label'>Date</label>
            <input type='date' name='date' className='form-control' onChange={handleInputChange} value={formData.date} />
          </div>
          <button type='submit' className='btn btn-primary w-100'>Add Transaction</button>
        </form>
      </div>
    </div>
  );
};

export default TransactionForm;