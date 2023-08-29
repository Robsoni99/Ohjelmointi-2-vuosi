import React, { useState } from 'react';

const StatisticLine = ({ text, value }) => {
  const css = {
    margin: 0,
    padding: 0,
  };

  return <p style={css}>{text}: {value}</p>;
};

const Statistics = ({ good, neutral, bad }) => {
  const total = good + neutral + bad;
  const average = total === 0 ? 0 : (good - bad) / total;
  const positivePercentage = total === 0 ? 0 : (good / total) * 100;

  if (total === 0) {
    return (
      <div id="statistics">
        <h2>Statistics</h2>
        <p>No feedback given yet</p>
      </div>
    );
  }

  return (
    <div id="statistics">
      <h2>Statistics</h2>
      <table>
        <tbody>
          <tr>
            <td>Good:</td>
            <td>{good}</td>
          </tr>
          <tr>
            <td>Neutral:</td>
            <td>{neutral}</td>
          </tr>
          <tr>
            <td>Bad:</td>
            <td>{bad}</td>
          </tr>
          <tr>
            <td>All:</td>
            <td>{total}</td>
          </tr>
          <tr>
            <td>Average:</td>
            <td>{isNaN(average) ? 0 : average}</td>
          </tr>
          <tr>
            <td>Positive:</td>
            <td>{isNaN(positivePercentage) ? 0 : positivePercentage + "%"}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

const Button = ({ text, onClick }) => {
  return <button onClick={onClick}>{text}</button>;
};

const App = () => {
  const [good, setGood] = useState(0);
  const [neutral, setNeutral] = useState(0);
  const [bad, setBad] = useState(0);

  return (
    <div>
      <div>
        <h1>Give Feedback</h1>
        <button onClick={() => setGood(good + 1)}>Good</button>
        <button onClick={() => setNeutral(neutral + 1)}>Neutral</button>
        <button onClick={() => setBad(bad + 1)}>Bad</button>
      </div>

      <Statistics good={good} neutral={neutral} bad={bad} />
    </div>
  );
};

export default App;