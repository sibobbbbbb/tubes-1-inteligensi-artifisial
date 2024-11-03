// pages/api/initial-state.js
export default function handler(req, res) {
  if (req.method === 'GET') {
    const initialState = Array.from({ length: 125 }, (_, i) => i + 1);
    shuffleArray(initialState); // Shuffle to simulate random initial state
    res.status(200).json(initialState);
  } else {
    res.status(405).end(); // Method Not Allowed
  }
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}
