import React, { useEffect, useState } from "react";
import ProjectList from "../components/ProjectList";
import { getProjects } from "../api/projects.api";

const ContractorDashboard = () => {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    getProjects().then(res => setProjects(res.data));
  }, []);

  return (
    <div>
      <h2>My Assigned Projects</h2>
      <ProjectList projects={projects} />
    </div>
  );
};

export default ContractorDashboard;
