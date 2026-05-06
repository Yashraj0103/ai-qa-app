import { useRef, useEffect } from "react";
import { Play, Clock } from "lucide-react";

export default function AudioPlayer({ file, timestamp, segments }) {
  const audioRef = useRef(null);

  useEffect(() => {
    if (timestamp !== null && timestamp !== undefined && audioRef.current) {
      audioRef.current.currentTime = timestamp;
      audioRef.current.play();
    }
  }, [timestamp]);

  if (!file) return null;

  const fileURL = URL.createObjectURL(file);

  return (
    <div style={{
      background: "#f1f5f9",
      borderRadius: "12px",
      padding: "16px",
      marginBottom: "16px"
    }}>
      <p style={{ fontWeight: 600, marginBottom: "10px", color: "#1e293b" }}>
        🎵 {file.name}
      </p>
      <audio ref={audioRef} controls src={fileURL} style={{ width: "100%" }} />

      {segments && segments.length > 0 && (
        <div style={{ marginTop: "14px" }}>
          <p style={{ fontWeight: 600, fontSize: "13px", color: "#475569", marginBottom: "8px" }}>
            <Clock size={14} style={{ marginRight: "4px" }} />
            Timestamps:
          </p>
          <div style={{ maxHeight: "150px", overflowY: "auto", display: "flex", flexDirection: "column", gap: "6px" }}>
            {segments.map((seg, i) => (
              <div
                key={i}
                onClick={() => {
                  if (audioRef.current) {
                    audioRef.current.currentTime = seg.start;
                    audioRef.current.play();
                  }
                }}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "6px 10px",
                  background: "#fff",
                  borderRadius: "8px",
                  cursor: "pointer",
                  fontSize: "13px",
                  color: "#334155"
                }}
              >
                <Play size={12} color="#6366f1" />
                <span style={{ color: "#6366f1", fontWeight: 600, minWidth: "50px" }}>
                  {seg.start.toFixed(1)}s
                </span>
                <span>{seg.text}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}