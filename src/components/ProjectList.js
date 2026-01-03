import React, { useEffect, useState } from "react";
import { fetchProjects } from "../api/projects.api";
import ProjectCard from "./ProjectCard";

function ProjectList() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetchProjects()
      .then(setProjects)
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      {projects.length === 0 && <p>No projects found.</p>}
      {projects.map((project) => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  );
}

export default ProjectList;
