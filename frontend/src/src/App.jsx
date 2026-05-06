import { useState, useEffect } from "react";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";
import DocumentList from "./components/DocumentList";
import AudioPlayer from "./components/AudioPlayer";
import { getDocuments } from "./api/client";

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [timestamp, setTimestamp] = useState(null);
  const [audioFile, setAudioFile] = useState(null);

  const fetchDocuments = async () => {
    try {
      const res = await getDocuments();
      setDocuments(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUploadSuccess = (data) => {
    fetchDocuments();
    setSelectedDoc({ id: data.doc_id, filename: data.filename, summary: data.summary });
  };

  return (
    <div style={{
      minHeight: "100vh", background: "#f8fafc",
      fontFamily: "'Inter', sans-serif"
    }}>
      {/* Header */}
      <div style={{
        background: "#6366f1", color: "#fff",
        padding: "16px 32px", display: "flex",
        alignItems: "center", gap: "12px"
      }}>
        <span style={{ fontSize: "24px" }}>🤖</span>
        <div>
          <h1 style={{ margin: 0, fontSize: "20px", fontWeight: 700 }}>AI Document & Media Q&A</h1>
          <p style={{ margin: 0, fontSize: "13px", opacity: 0.8 }}>
            Upload PDFs, audio, or video — then ask questions
          </p>
        </div>
      </div>

      {/* Main Layout */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "320px 1fr",
        gap: "24px",
        padding: "24px",
        maxWidth: "1200px",
        margin: "0 auto"
      }}>
        {/* Left Panel */}
        <div>
          <div style={{
            background: "#fff", borderRadius: "14px",
            padding: "20px", boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
            marginBottom: "20px"
          }}>
            <h2 style={{ margin: "0 0 16px", fontSize: "16px", color: "#1e293b" }}>
              📤 Upload File
            </h2>
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          </div>

          <div style={{
            background: "#fff", borderRadius: "14px",
            padding: "20px", boxShadow: "0 1px 4px rgba(0,0,0,0.06)"
          }}>
            <h2 style={{ margin: "0 0 16px", fontSize: "16px", color: "#1e293b" }}>
              📁 Your Documents
            </h2>
            <DocumentList
              documents={documents}
              selectedDoc={selectedDoc}
              onSelect={setSelectedDoc}
            />
          </div>
        </div>

        {/* Right Panel */}
        <div style={{
          background: "#fff", borderRadius: "14px",
          boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
          display: "flex", flexDirection: "column",
          height: "calc(100vh - 140px)"
        }}>
          <div style={{ padding: "20px 20px 0" }}>
            <h2 style={{ margin: "0 0 12px", fontSize: "16px", color: "#1e293b" }}>
              💬 Chat with Document
            </h2>
            {selectedDoc?.type === "audio" && audioFile && (
              <AudioPlayer
                file={audioFile}
                timestamp={timestamp}
                segments={selectedDoc.segments}
              />
            )}
          </div>
          <ChatBox
            selectedDoc={selectedDoc}
            onTimestamp={setTimestamp}
          />
        </div>
      </div>
    </div>
  );
}