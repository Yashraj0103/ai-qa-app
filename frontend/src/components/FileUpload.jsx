import { useState } from "react";
import { uploadPDF, uploadAudio } from "../api/client";
import { FileText, Music, Loader } from "lucide-react";

export default function FileUpload({ onUploadSuccess }) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [dragOver, setDragOver] = useState(false);

  const handleFile = async (file) => {
    if (!file) return;

    const isPDF = file.name.endsWith(".pdf");
    const isAudio = [".mp3", ".mp4", ".wav", ".m4a", ".webm"].some(ext =>
      file.name.endsWith(ext)
    );

    if (!isPDF && !isAudio) {
      setMessage("❌ Only PDF, MP3, MP4, WAV, M4A files are supported");
      return;
    }

    setLoading(true);
    setMessage("⏳ Uploading and processing...");

    try {
      const res = isPDF
        ? await uploadPDF(file)
        : await uploadAudio(file);

      setMessage("✅ Upload successful!");
      onUploadSuccess(res.data);
    } catch (err) {
      setMessage("❌ Upload failed. Check your API key and try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const handleInput = (e) => {
    handleFile(e.target.files[0]);
  };

  return (
    <div style={{ marginBottom: "24px" }}>
      <div
        onDrop={handleDrop}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        style={{
          border: `2px dashed ${dragOver ? "#6366f1" : "#cbd5e1"}`,
          borderRadius: "12px",
          padding: "40px",
          textAlign: "center",
          background: dragOver ? "#eef2ff" : "#f8fafc",
          cursor: "pointer",
          transition: "all 0.2s"
        }}
        onClick={() => document.getElementById("fileInput").click()}
      >
        <div style={{ display: "flex", justifyContent: "center", gap: "16px", marginBottom: "12px" }}>
          <FileText size={32} color="#6366f1" />
          <Music size={32} color="#6366f1" />
        </div>
        <p style={{ fontSize: "16px", color: "#475569", margin: 0 }}>
          {loading ? "Processing..." : "Drag & drop or click to upload"}
        </p>
        <p style={{ fontSize: "13px", color: "#94a3b8", margin: "6px 0 0" }}>
          Supports PDF, MP3, MP4, WAV, M4A
        </p>
        <input
          id="fileInput"
          type="file"
          accept=".pdf,.mp3,.mp4,.wav,.m4a,.webm"
          style={{ display: "none" }}
          onChange={handleInput}
        />
      </div>

      {loading && (
        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginTop: "12px", color: "#6366f1" }}>
          <Loader size={16} className="spin" />
          <span>This may take a moment for large files...</span>
        </div>
      )}

      {message && (
        <p style={{ marginTop: "10px", color: message.includes("❌") ? "#ef4444" : "#22c55e" }}>
          {message}
        </p>
      )}
    </div>
  );
}