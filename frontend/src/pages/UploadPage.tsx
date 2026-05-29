import { useState } from "react";
import { FileText, Mail, ScanLine, Send } from "lucide-react";

import {
  simulateIncomingEmail,
  uploadDocument,
  uploadScannedDocument,
} from "../api/documentsApi";
import { Layout } from "../components/Layout";

type UploadMode = "pdf" | "email" | "scan";

export function UploadPage() {
  const [activeMode, setActiveMode] = useState<UploadMode>("pdf");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState("");

  const [pdfFile, setPdfFile] = useState<File | null>(null);

  const [senderEmail, setSenderEmail] = useState("client.company@example.com");
  const [senderName, setSenderName] = useState("Client Company");
  const [emailSubject, setEmailSubject] = useState("Finance documents");
  const [emailBody, setEmailBody] = useState(
    "Hello, please process the attached documents."
  );
  const [emailAttachments, setEmailAttachments] = useState<File[]>([]);

  const [scanFile, setScanFile] = useState<File | null>(null);
  const [uploadSenderEmail, setUploadSenderEmail] = useState("client.company@example.com");
  const [uploadSenderName, setUploadSenderName] = useState("Client Company");
  const [uploadSubject, setUploadSubject] = useState("Uploaded business document");
  const [uploadBody, setUploadBody] = useState(
    "Hello, please process the attached document."
  );
  const [scanSenderEmail, setScanSenderEmail] = useState("client.company@example.com");

  const [scanSenderName, setScanSenderName] = useState("Client Company");

  const [scanSubject, setScanSubject] = useState("Scanned business document");

  const [scanBody, setScanBody] = useState("Hello, please process the attached scanned document.");

  function getErrorMessage(error: any, fallback: string) {
    return error.response?.data?.detail ?? fallback;
  }

  async function handlePdfUpload() {
    if (!pdfFile) {
      setMessage("Please select a PDF file first.");
      return;
    }

    setIsSubmitting(true);
    setMessage("");

    try {
      const result = await uploadDocument(pdfFile, {
        senderEmail: uploadSenderEmail,
        senderName: uploadSenderName,
        subject: uploadSubject,
        body: uploadBody,
        });
      setMessage(
        `PDF uploaded successfully. Document ID: ${result.documentId ?? result.id}`
      );
      setPdfFile(null);
    } catch (error: any) {
      setMessage(getErrorMessage(error, "PDF upload failed."));
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleEmailSimulation() {
    if (emailAttachments.length === 0) {
      setMessage("Please select at least one PDF attachment.");
      return;
    }

    setIsSubmitting(true);
    setMessage("");

    try {
      const result = await simulateIncomingEmail({
        senderEmail,
        senderName,
        subject: emailSubject,
        body: emailBody,
        attachments: emailAttachments,
      });

      setMessage(
        `Email simulated successfully. Processed attachments: ${result.uploadedDocuments?.length ?? 0}`
      );
      setEmailAttachments([]);
    } catch (error: any) {
      setMessage(getErrorMessage(error, "Email simulation failed."));
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleScanUpload() {
    if (!scanFile) {
        setMessage("Please select a scanned image first.");
        return;
    }

    setIsSubmitting(true);
    setMessage("");

    try {
        const result = await uploadScannedDocument(scanFile, {
        senderEmail: scanSenderEmail,
        senderName: scanSenderName,
        subject: scanSubject,
        body: scanBody,
        });

        setMessage(
        `Scan uploaded successfully. Document ID: ${result.documentId ?? result.id}`
        );

        setScanFile(null);
    } catch (error: any) {
        setMessage(getErrorMessage(error, "Scan upload failed."));
    } finally {
        setIsSubmitting(false);
    }
}

  return (
    <Layout>
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-3xl bg-[#101820] p-8 text-white shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#ffb4a8]">
            Admin Input Control
          </p>
          <h1 className="mt-3 text-3xl font-bold">Upload Center</h1>
          <p className="mt-3 max-w-2xl text-slate-300">
            Test and validate all document input channels: direct PDF upload,
            simulated incoming email, and scanned document OCR flow.
          </p>
        </div>

        <div className="mb-6 grid gap-4 md:grid-cols-3">
          <button
            onClick={() => {
              setActiveMode("pdf");
              setMessage("");
            }}
            className={`rounded-3xl border p-5 text-left transition hover:-translate-y-0.5 hover:shadow-md ${
              activeMode === "pdf"
                ? "border-blue-200 bg-blue-50"
                : "border-slate-200 bg-white"
            }`}
          >
            <FileText className="text-blue-600" size={26} />
            <h2 className="mt-4 text-lg font-bold text-slate-950">
              Direct PDF Upload
            </h2>
            <p className="mt-2 text-sm leading-6 text-slate-500">
              Sends a PDF through the upload input service.
            </p>
          </button>

          <button
            onClick={() => {
              setActiveMode("email");
              setMessage("");
            }}
            className={`rounded-3xl border p-5 text-left transition hover:-translate-y-0.5 hover:shadow-md ${
              activeMode === "email"
                ? "border-blue-200 bg-blue-50"
                : "border-slate-200 bg-white"
            }`}
          >
            <Mail className="text-blue-600" size={26} />
            <h2 className="mt-4 text-lg font-bold text-slate-950">
              Email Simulation
            </h2>
            <p className="mt-2 text-sm leading-6 text-slate-500">
              Simulates a real incoming email with PDF attachments.
            </p>
          </button>

          <button
            onClick={() => {
              setActiveMode("scan");
              setMessage("");
            }}
            className={`rounded-3xl border p-5 text-left transition hover:-translate-y-0.5 hover:shadow-md ${
              activeMode === "scan"
                ? "border-blue-200 bg-blue-50"
                : "border-slate-200 bg-white"
            }`}
          >
            <ScanLine className="text-blue-600" size={26} />
            <h2 className="mt-4 text-lg font-bold text-slate-950">
              Scan / OCR Upload
            </h2>
            <p className="mt-2 text-sm leading-6 text-slate-500">
              Sends an image through the OCR processing flow.
            </p>
          </button>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          {activeMode === "pdf" && (
            <div>
                <h2 className="text-2xl font-bold text-slate-950">
                Direct PDF Upload
                </h2>
                <p className="mt-2 text-sm text-slate-500">
                Upload a PDF and attach sender details so it appears in the inbox like a normal email.
                </p>

                <div className="mt-6 grid gap-4 md:grid-cols-2">
                <input
                    value={uploadSenderEmail}
                    onChange={(event) => setUploadSenderEmail(event.target.value)}
                    placeholder="Sender email"
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500"
                />

                <input
                    value={uploadSenderName}
                    onChange={(event) => setUploadSenderName(event.target.value)}
                    placeholder="Sender name / company"
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500"
                />

                <input
                    value={uploadSubject}
                    onChange={(event) => setUploadSubject(event.target.value)}
                    placeholder="Subject"
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500 md:col-span-2"
                />

                <textarea
                    value={uploadBody}
                    onChange={(event) => setUploadBody(event.target.value)}
                    placeholder="Message body"
                    rows={5}
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500 md:col-span-2"
                />

                <input
                    type="file"
                    accept="application/pdf"
                    className="block w-full rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm md:col-span-2"
                    onChange={(event) => setPdfFile(event.target.files?.[0] ?? null)}
                />
                </div>

                <button
                onClick={handlePdfUpload}
                disabled={isSubmitting}
                className="mt-6 flex items-center gap-2 rounded-2xl bg-[#101820] px-6 py-3 text-sm font-bold text-white transition hover:bg-[#ff5640] disabled:opacity-60"
                >
                <Send size={17} />
                {isSubmitting ? "Submitting..." : "Submit PDF"}
                </button>
            </div>
            )}

          {activeMode === "email" && (
            <div>
              <h2 className="text-2xl font-bold text-slate-950">
                Email Simulation
              </h2>
              <p className="mt-2 text-sm text-slate-500">
                Simulate an incoming company email with one or more PDF attachments.
              </p>

              <div className="mt-6 grid gap-4 md:grid-cols-2">
                <input
                  value={senderEmail}
                  onChange={(event) => setSenderEmail(event.target.value)}
                  placeholder="Sender email"
                  className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500"
                />

                <input
                  value={senderName}
                  onChange={(event) => setSenderName(event.target.value)}
                  placeholder="Sender name"
                  className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500"
                />

                <input
                  value={emailSubject}
                  onChange={(event) => setEmailSubject(event.target.value)}
                  placeholder="Subject"
                  className="md:col-span-2 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500"
                />

                <textarea
                  value={emailBody}
                  onChange={(event) => setEmailBody(event.target.value)}
                  placeholder="Email body"
                  rows={5}
                  className="md:col-span-2 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500"
                />

                <input
                  type="file"
                  accept="application/pdf"
                  multiple
                  className="md:col-span-2 block w-full rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm"
                  onChange={(event) =>
                    setEmailAttachments(Array.from(event.target.files ?? []))
                  }
                />
              </div>

              <button
                onClick={handleEmailSimulation}
                disabled={isSubmitting}
                className="mt-6 flex items-center gap-2 rounded-2xl bg-[#101820] px-6 py-3 text-sm font-bold text-white transition hover:bg-[#ff5640] disabled:opacity-60"
              >
                <Send size={17} />
                {isSubmitting ? "Submitting..." : "Simulate Email"}
              </button>
            </div>
          )}

          {activeMode === "scan" && (
            <div>
                <h2 className="text-2xl font-bold text-slate-950">
                Scan / OCR Upload
                </h2>

                <p className="mt-2 text-sm text-slate-500">
                Upload a scanned image and verify OCR + AI classification.
                </p>

                <div className="mt-6 grid gap-4 md:grid-cols-2">
                <input
                    value={scanSenderEmail}
                    onChange={(event) => setScanSenderEmail(event.target.value)}
                    placeholder="Sender email"
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500"
                />

                <input
                    value={scanSenderName}
                    onChange={(event) => setScanSenderName(event.target.value)}
                    placeholder="Sender name / company"
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500"
                />

                <input
                    value={scanSubject}
                    onChange={(event) => setScanSubject(event.target.value)}
                    placeholder="Subject"
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500 md:col-span-2"
                />

                <textarea
                    value={scanBody}
                    onChange={(event) => setScanBody(event.target.value)}
                    placeholder="Message body"
                    rows={5}
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none focus:border-blue-500 md:col-span-2"
                />

                <input
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    className="block w-full rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm md:col-span-2"
                    onChange={(event) =>
                    setScanFile(event.target.files?.[0] ?? null)
                    }
                />
                </div>

                <button
                onClick={handleScanUpload}
                disabled={isSubmitting}
                className="mt-6 flex items-center gap-2 rounded-2xl bg-[#101820] px-6 py-3 text-sm font-bold text-white transition hover:bg-[#ff5640] disabled:opacity-60"
                >
                <Send size={17} />
                {isSubmitting ? "Submitting..." : "Submit Scan"}
                </button>
            </div>
            )}

          {message && (
            <div className="mt-8 rounded-2xl bg-slate-100 p-4 text-sm font-medium text-slate-700">
              {message}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}