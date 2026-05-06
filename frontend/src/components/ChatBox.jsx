import { useState } from "react";
import { askQuestion } from "../api/client";
import { Send, Loader } from "lucide-react";

export default function ChatBox({ selectedDoc, onTimestamp }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || !selectedDoc) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await askQuestion(selectedDoc.id, input);
      const botMsg = {
        role: "bot",
        text: res.data.answer,
        timestamp: res.data.timestamp,
        sources: res.data.sources
      };
      setMessages((prev) => [...prev, botMsg]);

      if (res.data.timestamp !== null && res.data.timestamp !== undefined) {
        onTimestamp(res.data.timestamp);
      }
    } catch (err) {
      setMessages((prev) => [...prev, {
        role: "bot",
        text: "❌ Error getting answer. Please try again."
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      {!selectedDoc && (
        <div style={{
          flex: 1, display: "flex", alignItems: "center",
          justifyContent: "center", color: "#94a3b8"
        }}>
          ← Select a document to start chatting
        </div>
      )}

      {selectedDoc && (
        <>
          <div style={{
            flex: 1, overflowY: "auto", padding: "16px",
            display: "flex", flexDirection: "column", gap: "12px"
          }}>
            {messages.length === 0 && (
              <p style={{ color: "#94a3b8", textAlign: "center" }}>
                Ask anything about <strong>{selectedDoc.filename}</strong>
              </p>
            )}

            {messages.map((msg, i) => (
              <div key={i} style={{
                display: "flex",
                justifyContent: msg.role === "user" ? "flex-end" : "flex-start"
              }}>
                <div style={{
                  maxWidth: "75%",
                  padding: "12px 16px",
                  borderRadius: msg.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                  background: msg.role === "user" ? "#6366f1" : "#f1f5f9",
                  color: msg.role === "user" ? "#fff" : "#1e293b",
                  fontSize: "14px",
                  lineHeight: "1.6",
                  whiteSpace: "pre-wrap"
                }}>
                  {msg.text}

                  {msg.timestamp !== null && msg.timestamp !== undefined && (
                    <div style={{
                      marginTop: "8px", fontSize: "12px",
                      color: "#6366f1", background: "#eef2ff",
                      padding: "4px 8px", borderRadius: "6px",
                      display: "inline-block"
                    }}>
                      ▶ Jump to {msg.timestamp.toFixed(1)}s
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "#94a3b8" }}>
                <Loader size={14} />
                <span>Thinking...</span>
              </div>
            )}
          </div>

          <div style={{
            padding: "16px",
            borderTop: "1px solid #e2e8f0",
            display: "flex", gap: "10px"
          }}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Ask a question about the document..."
              style={{
                flex: 1, padding: "12px 16px",
                borderRadius: "10px", border: "1px solid #e2e8f0",
                fontSize: "14px", outline: "none"
              }}
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              style={{
                padding: "12px 18px", borderRadius: "10px",
                background: "#6366f1", color: "#fff",
                border: "none", cursor: "pointer",
                opacity: loading || !input.trim() ? 0.5 : 1
              }}
            >
              <Send size={18} />
            </button>
          </div>
        </>
      )}
    </div>
  );
}