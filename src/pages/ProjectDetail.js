import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getProjectById } from "../api/projects.api";

const ProjectDetail = () => {
  const { id } = useParams();
  const [project, setProject] = useState(null);

  useEffect(() => {
    getProjectById(id).then(res => setProject(res.data));
  }, [id]);

  if (!project) return <p>Loading...</p>;

  return (
    <div>
      <h2>{project.name}</h2>
      <p>{project.description}</p>
      <p>Budget: NPR {project.budget}</p>

      <Link to={`/projects/${id}/upload`}>
        Upload Progress
      </Link>
    </div>
  );
};

export default ProjectDetail;
