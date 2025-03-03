/** @jsxImportSource https://esm.sh/react@18.2.0 */
import React, { useState, useRef } from "https://esm.sh/react@18.2.0";
import { createRoot } from "https://esm.sh/react-dom@18.2.0/client";
import QRCode from "https://esm.sh/qrcode";

function QRCodeGenerator() {
  const [url, setUrl] = useState('');
  const [qrCodeData, setQRCodeData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [qrStyle, setQRStyle] = useState('square');
  const canvasRef = useRef(null);

  const validateUrl = (inputUrl) => {
    try {
      new URL(inputUrl);
      return true;
    } catch {
      return false;
    }
  };

  const generateQRCode = async () => {
    setLoading(true);
    setError(null);

    if (!validateUrl(url)) {
      setError('Invalid URL. Please enter a valid URL.');
      setLoading(false);
      return;
    }

    try {
      const canvas = canvasRef.current;
      
      await QRCode.toCanvas(canvas, url, {
        width: 300,
        margin: 2,
        color: {
          dark: "#000000",
          light: "#ffffff"
        },
        type: qrStyle === 'rounded' ? 'svg' : 'png'
      });

      setQRCodeData(canvas.toDataURL());
    } catch (err) {
      setError('Failed to generate QR Code');
    } finally {
      setLoading(false);
    }
  };

  const downloadQRCode = () => {
    if (!qrCodeData) return;

    const link = document.createElement('a');
    link.download = `qr_code_${new Date().toISOString().replace(/[:.]/g, '-')}.png`;
    link.href = qrCodeData;
    link.click();
  };

  return (
    <div style={{
      fontFamily: 'Arial, sans-serif',
      maxWidth: '500px',
      margin: 'auto',
      padding: '20px',
      textAlign: 'center',
      background: 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)',
      borderRadius: '15px',
      boxShadow: '0 10px 25px rgba(0,0,0,0.1)'
    }}>
      <h1 style={{ 
        color: '#333', 
        marginBottom: '20px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        🔳 QR Code Generator
      </h1>

      <div style={{ 
        background: 'white', 
        padding: '20px', 
        borderRadius: '10px',
        boxShadow: '0 5px 15px rgba(0,0,0,0.1)'
      }}>
        <input 
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL (https://example.com)"
          style={{
            width: '100%',
            padding: '10px',
            marginBottom: '15px',
            border: '1px solid #ddd',
            borderRadius: '5px'
          }}
        />

        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          marginBottom: '15px' 
        }}>
          <label style={{ marginRight: '10px' }}>
            <input 
              type="radio" 
              value="square"
              checked={qrStyle === 'square'}
              onChange={() => setQRStyle('square')}
            />
            Square
          </label>
          <label>
            <input 
              type="radio" 
              value="rounded"
              checked={qrStyle === 'rounded'}
              onChange={() => setQRStyle('rounded')}
            />
            Rounded
          </label>
        </div>

        <button 
          onClick={generateQRCode}
          disabled={loading}
          style={{
            backgroundColor: loading ? '#ccc' : '#4CAF50',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '5px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Generating...' : 'Generate QR Code'}
        </button>

        {error && (
          <div style={{ 
            color: 'red', 
            marginTop: '15px',
            padding: '10px',
            backgroundColor: '#ffeeee',
            borderRadius: '5px'
          }}>
            {error}
          </div>
        )}

        {qrCodeData && (
          <div style={{ 
            marginTop: '20px', 
            display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'center' 
          }}>
            <canvas 
              ref={canvasRef} 
              style={{ 
                display: 'none' 
              }}
            />
            <img 
              src={qrCodeData} 
              alt="Generated QR Code" 
              style={{ 
                maxWidth: '250px', 
                boxShadow: '0 5px 15px rgba(0,0,0,0.2)',
                borderRadius: '10px'
              }}
            />
            <button 
              onClick={downloadQRCode}
              style={{
                marginTop: '15px',
                backgroundColor: '#2196F3',
                color: 'white',
                border: 'none',
                padding: '10px 20px',
                borderRadius: '5px'
              }}
            >
              Download QR Code
            </button>
          </div>
        )}
      </div>

      <a 
        href={import.meta.url.replace("esm.town", "val.town")} 
        target="_top" 
        style={{ 
          display: 'block', 
          marginTop: '20px', 
          color: '#333', 
          textDecoration: 'none',
          fontSize: '0.8em'
        }}
      >
        View QR Code Generator Source
      </a>
    </div>
  );
}

function App() {
  return <QRCodeGenerator />;
}

function client() {
  createRoot(document.getElementById("root")).render(<App />);
}
if (typeof document !== "undefined") { client(); }

export default async function server(request: Request): Promise<Response> {
  return new Response(`
    <html>
      <head>
        <title>QR Code Generator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
      </head>
      <body>
        <div id="root"></div>
        <script src="https://esm.town/v/std/catch"></script>
        <script type="module" src="${import.meta.url}"></script>
      </body>
    </html>
  `, {
    headers: { "content-type": "text/html" }
  });
}
