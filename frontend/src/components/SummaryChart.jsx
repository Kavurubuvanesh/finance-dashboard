import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const SummaryChart = ({ transactions }) => {
  // 1. Calculate Totals
  const income = transactions
    .filter(t => t.is_income)
    .reduce((acc, t) => acc + t.amount, 0);

  const expense = transactions
    .filter(t => !t.is_income)
    .reduce((acc, t) => acc + t.amount, 0);

  // 2. Define Chart Data
  const data = {
    labels: ['Income', 'Expense'],
    datasets: [
      {
        data: [income, expense],
        backgroundColor: ['#4caf50', '#f44336'], // Green for Money In, Red for Money Out
        hoverBackgroundColor: ['#66bb6a', '#e57373'],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    plugins: {
      legend: { position: 'bottom' },
    },
  };

  return (
    <div className="card mb-4">
        <div className="card-header">Financial Overview</div>
        <div className="card-body" style={{ height: '300px', display: 'flex', justifyContent: 'center' }}>
            {/* Handle case with no data */}
            {income === 0 && expense === 0 ? (
                <p className="text-muted mt-5">No data to display</p>
            ) : (
                <Pie data={data} options={options} />
            )}
        </div>
    </div>
  );
};

export default SummaryChart;