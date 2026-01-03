import React from "react";
import ContractorProgressForm from "./ContractorProgressForm";

function ProjectCard({ project }) {
  return (
    <div
      style={{
        border: "1px solid #ccc",
        padding: "15px",
        marginBottom: "15px",
        borderRadius: "8px",
      }}
    >
      <h3>{project.name}</h3>
      <p><strong>Location:</strong> {project.location}</p>
      <p><strong>Ministry:</strong> {project.ministry}</p>
      <p><strong>Budget:</strong> NPR {project.total_budget}</p>

      <ContractorProgressForm projectId={project.id} />
    </div>
  );
}

export default ProjectCard;
