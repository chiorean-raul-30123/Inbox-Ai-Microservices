import { useRef, useState } from "react";
import { uploadDocument, uploadScannedDocument } from "../api/documentsApi";


type SubmitMode = "email" | "pdf" | "scan";

const companyEmail = "documents@inbox-ai.local";

export function ClientSubmitPage() {
  const [activeMode, setActiveMode] = useState<SubmitMode>("email");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const cameraInputRef = useRef<HTMLInputElement | null>(null);

  async function handlePdfUpload() {
    if (!selectedFile) {
      setMessage("Please select a PDF document first.");
      return;
    }

    setIsSubmitting(true);
    setMessage(null);

    try {
      const result = await uploadDocument(selectedFile);
      setMessage(`Document submitted successfully. Tracking ID: ${result.documentId ?? result.id}`);
      setSelectedFile(null);
    } catch (error: any) {
      setMessage(
        error.response?.data?.detail ?? "Upload failed. Please try again."
      );
    }finally {
      setIsSubmitting(false);
    }
  }

  async function handleScanUpload() {
  if (!selectedFile) {
    setMessage("Please select or scan an image first.");
    return;
  }

  setIsSubmitting(true);
  setMessage(null);

  try {
    const result = await uploadScannedDocument(selectedFile);
    setMessage(
      `Scanned document submitted successfully. Tracking ID: ${
        result.documentId ?? result.id
      }`
    );
    setSelectedFile(null);
  } catch (error: any) {
    setMessage(
      error.response?.data?.detail ?? "Scan upload failed. Please try again."
    );
  } finally {
    setIsSubmitting(false);
  }
}

  function handleCopyEmail() {
    navigator.clipboard.writeText(companyEmail);
    setMessage("Company email copied to clipboard.");
  }

  function scrollToSubmit() {
    document.getElementById("submit-options")?.scrollIntoView({ behavior: "smooth" });
  }

  function handleScanClick() {
    cameraInputRef.current?.click();
  }

  return (
    <div className="min-h-screen bg-[#f4f1ec] text-slate-900">
      <header className="sticky top-0 z-30 border-b border-white/10 bg-[#101820]/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#ff5640] font-bold text-white">
              IA
            </div>
            <div>
              <div className="font-semibold text-white">Inbox AI</div>
              <div className="text-xs text-slate-300">Document routing portal</div>
            </div>
          </div>

          <button
            onClick={scrollToSubmit}
            className="rounded-full bg-white px-5 py-2 text-sm font-semibold text-[#101820] transition hover:bg-[#ff5640] hover:text-white"
          >
            Submit document
          </button>
        </div>
      </header>

      <section className="relative overflow-hidden bg-[#101820]">
        <div className="absolute inset-0 opacity-30">
          <div className="absolute left-[-10%] top-[-20%] h-96 w-96 rounded-full bg-[#ff5640] blur-3xl" />
          <div className="absolute bottom-[-20%] right-[-10%] h-96 w-96 rounded-full bg-blue-500 blur-3xl" />
        </div>

        <div className="relative mx-auto grid min-h-[680px] max-w-7xl items-center gap-12 px-6 py-20 lg:grid-cols-2">
          <div>
            <p className="mb-5 text-sm font-semibold uppercase tracking-[0.3em] text-[#ffb4a8]">
              Intelligent document intake
            </p>

            <h1 className="max-w-3xl text-5xl font-bold leading-tight text-white md:text-7xl">
              Submit documents. Let AI route them.
            </h1>

            <p className="mt-6 max-w-xl text-lg leading-8 text-slate-300">
              Upload PDFs, send attachments by email, or scan paper documents from your phone.
              Inbox AI classifies and routes every document to the right business team.
            </p>

            <div className="mt-10 flex flex-col gap-4 sm:flex-row">
              <button
                onClick={scrollToSubmit}
                className="rounded-full bg-[#ff5640] px-7 py-4 text-sm font-bold text-white shadow-xl shadow-[#ff5640]/20 transition hover:bg-[#ff735f]"
              >
                Start submission
              </button>

              <a
                href={`mailto:${companyEmail}`}
                className="rounded-full border border-white/20 px-7 py-4 text-center text-sm font-bold text-white transition hover:bg-white hover:text-[#101820]"
              >
                Send by email
              </a>
            </div>
          </div>

          <div className="relative">
            <div className="overflow-hidden rounded-[2rem] border border-white/10 bg-white/10 p-3 shadow-2xl backdrop-blur">
              <img
                src="https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&q=80"
                alt="Business team reviewing documents"
                className="h-[460px] w-full rounded-[1.5rem] object-cover"
              />
            </div>

            
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-20">
        <div className="grid gap-6 md:grid-cols-3">
          {[
            ["1", "Submit", "Send documents by upload, email, or mobile scan."],
            ["2", "Classify", "AI extracts content and predicts HR, Finance, or Legal."],
            ["3", "Route", "The document lands in the correct department inbox."],
          ].map(([step, title, description]) => (
            <div key={step} className="rounded-3xl bg-white p-8 shadow-sm">
              <div className="mb-8 flex h-12 w-12 items-center justify-center rounded-full bg-[#101820] text-lg font-bold text-white">
                {step}
              </div>
              <h3 className="text-2xl font-bold text-[#101820]">{title}</h3>
              <p className="mt-3 leading-7 text-slate-600">{description}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="submit-options" className="mx-auto max-w-7xl px-6 py-20">
        <div className="mb-10 max-w-2xl">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-[#ff5640]">
            Contact us
          </p>
          <h2 className="mt-4 text-4xl font-bold text-[#101820]">
            Choose how you want to submit your document
          </h2>
          <p className="mt-4 text-lg leading-8 text-slate-600">
            Pick the option that fits your workflow. Email and PDF upload are available now;
            mobile scanning is prepared for OCR processing.
          </p>
        </div>

        <div className="grid gap-5 md:grid-cols-3">
          {[
            ["email", "Send by email", "Use the company intake mailbox."],
            ["pdf", "Upload PDF", "Submit an existing PDF file."],
            ["scan", "Scan document", "Use a phone camera or image upload."],
          ].map(([mode, title, description]) => (
            <button
              key={mode}
              onClick={() => {
                setActiveMode(mode as SubmitMode);
                setMessage(null);
              }}
              className={`rounded-3xl border p-6 text-left transition ${
                activeMode === mode
                  ? "border-[#ff5640] bg-[#fff1ee] shadow-lg"
                  : "border-slate-200 bg-white hover:border-[#ff5640]"
              }`}
            >
              <h3 className="text-xl font-bold text-[#101820]">{title}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">{description}</p>
            </button>
          ))}
        </div>

        <div className="mt-8 rounded-[2rem] bg-white p-8 shadow-sm">
          {activeMode === "email" && (
            <div>
              <h3 className="text-2xl font-bold text-[#101820]">Send your documents by email</h3>
              <p className="mt-3 text-slate-600">
                Attach PDF documents and send them to the intake address below.
              </p>

              <div className="mt-6 flex flex-col gap-4 rounded-2xl bg-slate-100 p-5 sm:flex-row sm:items-center sm:justify-between">
                <span className="font-mono text-sm text-slate-800">{companyEmail}</span>
                <button
                  onClick={handleCopyEmail}
                  className="rounded-full bg-[#101820] px-5 py-3 text-sm font-bold text-white hover:bg-[#ff5640]"
                >
                  Copy email
                </button>
              </div>
            </div>
          )}

          {activeMode === "pdf" && (
            <div>
              <h3 className="text-2xl font-bold text-[#101820]">Upload a PDF</h3>
              <p className="mt-3 text-slate-600">
                Your document will be stored securely and queued for classification.
              </p>

              <input
                type="file"
                accept="application/pdf"
                className="mt-6 block w-full rounded-2xl border border-slate-300 bg-white p-4 text-sm"
                onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
              />

              <button
                onClick={handlePdfUpload}
                disabled={isSubmitting}
                className="mt-6 rounded-full bg-[#ff5640] px-7 py-4 text-sm font-bold text-white hover:bg-[#ff735f] disabled:opacity-60"
              >
                {isSubmitting ? "Submitting..." : "Submit document"}
              </button>
            </div>
          )}

          {activeMode === "scan" && (
            <div>
              <h3 className="text-2xl font-bold text-[#101820]">Scan or upload an image</h3>
              <p className="mt-3 text-slate-600">
                On mobile, this opens the camera. OCR processing will be connected in the scan input service.
              </p>

              <input
                ref={cameraInputRef}
                type="file"
                accept="image/*"
                capture="environment"
                className="hidden"
                onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
              />

              <button
                onClick={handleScanClick}
                className="mt-6 rounded-full bg-[#101820] px-7 py-4 text-sm font-bold text-white hover:bg-[#ff5640]"
              >
                Open camera
              </button>

              {selectedFile && (
                <p className="mt-4 text-sm text-slate-600">
                  Selected image: {selectedFile.name}
                </p>
              )}
              <button
                onClick={handleScanUpload}
                disabled={isSubmitting || !selectedFile}
                className="mt-6 rounded-full bg-[#ff5640] px-7 py-4 text-sm font-bold text-white hover:bg-[#ff735f] disabled:opacity-60"
              >
                {isSubmitting ? "Submitting..." : "Submit scanned document"}
              </button>
            </div>
          )}

          {message && (
            <div className="mt-8 rounded-2xl bg-slate-100 p-5 text-sm font-medium text-slate-700">
              {message}
            </div>
          )}
        </div>
      </section>

      <footer className="bg-[#101820] px-6 py-10 text-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="font-bold">Inbox AI</div>
            <div className="mt-1 text-sm text-slate-400">
              Enterprise document classification and routing.
            </div>
          </div>
          <button
            onClick={scrollToSubmit}
            className="rounded-full bg-white px-5 py-3 text-sm font-bold text-[#101820] hover:bg-[#ff5640] hover:text-white"
          >
            Contact us
          </button>
        </div>
      </footer>
    </div>
  );
}