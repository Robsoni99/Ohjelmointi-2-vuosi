import { useState } from 'react'

const App = () => {
  const [good, setGood] = useState(0)
  const [neutral, setNeutral] = useState(0)
  const [bad, setBad] = useState(0)

  return (
    <div>
      <h1>Palautteet</h1>
      <button onClick={() => setGood(good + 1)}>Hyvä</button>
      <button onClick={() => setNeutral(neutral + 1)}>Neutraali</button>
      <button onClick={() => setBad(bad + 1)}>Huono</button>

      <h2>Tilanne:</h2>
      <p>Hyvä: {good}</p>
      <p>Neutraali: {neutral}</p>
      <p>Huono: {bad}</p>
    </div>
  )
}

export default App