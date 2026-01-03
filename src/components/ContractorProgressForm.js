import { useState } from "react";
import { submitProgress } from "../api/progress.api";

function ContractorProgressForm({ projectId }) {
  const [physical, setPhysical] = useState("");
  const [financial, setFinancial] = useState("");
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await submitProgress(projectId, {
        physical_progress: physical,
        financial_progress: financial,
        images: images,
      });

      alert("Progress submitted successfully");

      setPhysical("");
      setFinancial("");
      setImages([]);
    } catch (err) {
      console.error(err);
      alert("Failed to submit progress");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="progress-form">
      <h3>Submit Progress</h3>

      <input
        type="number"
        placeholder="Physical Progress (%)"
        value={physical}
        onChange={(e) => setPhysical(e.target.value)}
        required
      />

      <input
        type="number"
        placeholder="Financial Progress (%)"
        value={financial}
        onChange={(e) => setFinancial(e.target.value)}
        required
      />

      <input
        type="file"
        multiple
        accept="image/*"
        onChange={(e) => setImages(e.target.files)}
      />

      <button type="submit" disabled={loading}>
        {loading ? "Submitting..." : "Submit"}
      </button>
    </form>
  );
}

export default ContractorProgressForm;
