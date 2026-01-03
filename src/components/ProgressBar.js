import React from 'react';

function ProgressBar({ percentage, height = '20px', color = '#3b82f6' }) {
  return (
    <div className="progress-bar-container" style={{ height }}>
      <div 
        className="progress-bar-fill" 
        style={{ 
          width: `${percentage}%`,
          backgroundColor: color
        }}
      >
        <span className="progress-text">{percentage}%</span>
      </div>
    </div>
  );
}

export default ProgressBar;
