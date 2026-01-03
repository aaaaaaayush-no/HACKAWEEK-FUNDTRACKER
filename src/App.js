import React from "react";
import Navbar from "./components/Navbar";
import ProjectList from "./components/ProjectList";
import Footer from "./components/Footer";
import "./App.css";

function App() {
  return (
    <div>
      <Navbar />
      <main style={{ padding: "20px" }}>
        <h2>Contractor Dashboard</h2>
        <ProjectList />
      </main>
      <Footer />
    </div>
  );
}

export default App;
