import React from 'react';

// We accept 'transactions' as a prop from the parent
const TransactionList = ({ transactions }) => {
  return (
    <div>
      <h2>Latest Transactions</h2>
      <table className='table table-striped table-bordered table-hover'>
        <thead className='table-dark'>
          <tr>
            <th>Amount</th>
            <th>Category</th>
            <th>Description</th>
            <th>Income?</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              {/* Conditional styling for income vs expense */}
              <td className={transaction.is_income ? 'text-success fw-bold' : 'text-danger fw-bold'}>
                {transaction.is_income ? '+' : '-'}${transaction.amount}
              </td>
              <td>{transaction.category}</td>
              <td>{transaction.description}</td>
              <td>{transaction.is_income ? 'Yes' : 'No'}</td>
              <td>{transaction.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TransactionList;