import { FileText, Music } from "lucide-react";

export default function DocumentList({ documents, selectedDoc, onSelect }) {
  if (documents.length === 0) {
    return (
      <p style={{ color: "#94a3b8", textAlign: "center", padding: "20px" }}>
        No documents uploaded yet
      </p>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
      {documents.map((doc) => (
        <div
          key={doc.id}
          onClick={() => onSelect(doc)}
          style={{
            padding: "14px",
            borderRadius: "10px",
            border: `2px solid ${selectedDoc?.id === doc.id ? "#6366f1" : "#e2e8f0"}`,
            background: selectedDoc?.id === doc.id ? "#eef2ff" : "#fff",
            cursor: "pointer",
            transition: "all 0.2s"
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            {doc.type === "pdf"
              ? <FileText size={18} color="#6366f1" />
              : <Music size={18} color="#6366f1" />}
            <span style={{ fontWeight: 600, color: "#1e293b" }}>{doc.filename}</span>
            <span style={{
              marginLeft: "auto",
              fontSize: "11px",
              background: doc.type === "pdf" ? "#dbeafe" : "#fce7f3",
              color: doc.type === "pdf" ? "#2563eb" : "#db2777",
              padding: "2px 8px",
              borderRadius: "999px"
            }}>
              {doc.type.toUpperCase()}
            </span>
          </div>

          {doc.summary && (
            <p style={{
              margin: "8px 0 0",
              fontSize: "13px",
              color: "#64748b",
              lineHeight: "1.5",
              whiteSpace: "pre-line"
            }}>
              {doc.summary.slice(0, 200)}...
            </p>
          )}
        </div>
      ))}
    </div>
  );
}