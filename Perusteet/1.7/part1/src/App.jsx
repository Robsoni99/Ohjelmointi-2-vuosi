import { useState } from 'react'

const App = () => {
  const [good, setGood] = useState(0)
  const [neutral, setNeutral] = useState(0)
  const [bad, setBad] = useState(0)

  const total = good + neutral + bad
  const average = (good - bad) / total
  const positivePercentage = (good / total) * 100

  const css = {
    margin: 0,
    padding: 0
  };

  return (
    <div>
      <div>
        <h1>Give Feedback</h1>
        <button onClick={() => setGood(good + 1)}>Hyvä</button>
        <button onClick={() => setNeutral(neutral + 1)}>Neutraali</button>
        <button onClick={() => setBad(bad + 1)}>Huono</button>
      </div>
  
      <div id="statistics">
        <h2>Statistics</h2>
        <p style={css}>Good: {good}</p>
        <p style={css}>Neutral: {neutral}</p>
        <p style={css}>Bad: {bad}</p>
        <p style={css}>All: {total}</p>
        <p style={css}>Average: {isNaN(average) ? 0 : average}</p>
        <p style={css}>Positive: {isNaN(positivePercentage) ? 0 : positivePercentage}%</p>
      </div>
    </div>
  )
}

export default App