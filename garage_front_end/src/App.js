import './App.css';
import { Routes, Route } from "react-router-dom"
import Projects from './pages/Projects';
import Pendulum from './pages/Projects/Pendulum';

function App() {
  return (
    <>
    <div className="App">
      <Routes>
        <Route path="/" element={<Projects />} />
        <Route path="/pendulum" element={<Pendulum />} />
      </Routes>
    </div>
    </>
  );
}

export default App;
