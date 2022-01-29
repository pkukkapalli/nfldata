import { BrowserRouter as Router, Routes, Link, Route } from "react-router-dom";
import CoachingTree from "./CoachingTree";

function App() {
  return (
    <Router>
      <div className="App">
        <strong>Analyses</strong>
        <ul>
          <li>
            <Link to="/coaching-tree">Coaching Tree</Link>
          </li>
        </ul>
      </div>

      <Routes>
        <Route path="/coaching-tree" element={<CoachingTree />} />
      </Routes>
    </Router>
  );
}

export default App;
