import React from "react";
import { useParams } from "react-router-dom";
import ContractorProgressForm from "../components/ContractorProgressForm";

function UploadProgress() {
  const { id } = useParams();

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto" }}>
      <h2>Upload Progress Report</h2>
      <ContractorProgressForm projectId={id} />
    </div>
  );
}

export default UploadProgress;