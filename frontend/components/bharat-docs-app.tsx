"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Upload, Download, FileText, CheckCircle, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

type Status = "idle" | "uploading" | "processing" | "complete"

export default function BharatDocsApp() {
  const [status, setStatus] = useState<Status>("idle")
  const [fileName, setFileName] = useState<string>("")
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [translatedBlob, setTranslatedBlob] = useState<Blob | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && file.type === "application/pdf") {
      setFileName(file.name)
      setUploadedFile(file)
      simulateUpload(file)
    }
  }

  const simulateUpload = async (file: File) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"

    try {
      setStatus("uploading")

      const form = new FormData()
      form.append("file", file)

      const uploadRes = await fetch(`${apiBase}/upload`, {
        method: "POST",
        body: form,
      })

      if (!uploadRes.ok) throw new Error("Upload failed")

      setStatus("processing")

      // Request server to translate/process the uploaded PDF and return the result
      const translateRes = await fetch(`${apiBase}/translate-pdf`, {
        method: "POST",
      })

      if (!translateRes.ok) throw new Error("Processing failed")

      const blob = await translateRes.blob()

      // Keep the translated blob in state so the Download button can use it
      setTranslatedBlob(blob)

      // Trigger download of the processed file (immediate) — also keep blob for later downloads
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `translated_${fileName || "document"}.pdf`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)

      setStatus("complete")
    } catch (err) {
      console.error(err)
      setStatus("idle")
      // Optionally show user-facing error here
    }
  }

  const handleDownload = () => {
    const fileOrBlob = translatedBlob ?? uploadedFile
    if (fileOrBlob) {
      const url = URL.createObjectURL(fileOrBlob)
      const a = document.createElement("a")
      a.href = url
      // Prefer translated filename when available
      a.download = translatedBlob ? `translated_${fileName || "document"}.pdf` : `processed_${fileName}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    }
  }

  const handleReset = () => {
    setStatus("idle")
    setFileName("")
    setUploadedFile(null)
    setTranslatedBlob(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  return (
    <div className="h-screen w-screen bg-white flex flex-col items-center justify-center overflow-hidden p-4">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-32 h-32 bg-orange-100 rounded-full animate-pulse opacity-50" />
        <div
          className="absolute bottom-20 right-20 w-40 h-40 bg-green-100 rounded-full animate-bounce opacity-40"
          style={{ animationDuration: "3s" }}
        />
        <div
          className="absolute top-1/3 right-1/4 w-24 h-24 bg-blue-100 rounded-full animate-ping opacity-30"
          style={{ animationDuration: "2s" }}
        />
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center gap-6 max-w-md w-full">
        {/* Logo & Title */}
        <div className="text-center animate-fade-in">
          <div className="flex items-center justify-center gap-3 mb-2">
            <FileText className="w-10 h-10 text-orange-500" style={{ animationDuration: "2s" }} />
            <h1 className="text-4xl font-bold text-gray-900 tracking-tight">
              NDA <span className="text-orange-500">Docs</span>
            </h1>
          </div>
          <p className="text-gray-500 text-sm animate-fade-in" style={{ animationDelay: "0.2s" }}>
            Upload • Process • Download
          </p>
        </div>

        {/* Upload Card */}
        <Card className="w-full p-6 bg-white border-2 border-dashed border-gray-200 hover:border-orange-300 transition-all duration-300 animate-scale-in shadow-lg">
          {status === "idle" && (
            <label className="flex flex-col items-center justify-center gap-4 cursor-pointer py-8 group">
              <div className="p-4 bg-orange-50 rounded-full group-hover:bg-orange-100 transition-colors duration-300 group-hover:scale-110 transform">
                <Upload className="w-8 h-8 text-orange-500" />
              </div>
              <div className="text-center">
                <p className="text-gray-700 font-medium">Click to upload PDF</p>
                <p className="text-gray-400 text-sm mt-1">or drag and drop</p>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
                className="hidden"
              />
            </label>
          )}

          {status === "uploading" && (
            <div className="flex flex-col items-center justify-center gap-4 py-8 animate-fade-in">
              <Loader2 className="w-12 h-12 text-orange-500 animate-spin" />
              <div className="text-center">
                <p className="text-gray-700 font-medium">Uploading...</p>
                <p className="text-gray-400 text-sm mt-1">{fileName}</p>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                <div className="bg-orange-500 h-2 rounded-full animate-progress" />
              </div>
            </div>
          )}

          {status === "processing" && (
            <div className="flex flex-col items-center justify-center gap-4 py-8 animate-fade-in">
              <div className="relative">
                <FileText className="w-12 h-12 text-green-500" />
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-orange-500 rounded-full animate-ping" />
              </div>
              <div className="text-center">
                <p className="text-gray-700 font-medium">Processing document...</p>
                <p className="text-gray-400 text-sm mt-1">Please wait</p>
              </div>
            </div>
          )}

          {status === "complete" && (
            <div className="flex flex-col items-center justify-center gap-4 py-8 animate-fade-in">
              <div
                className="p-4 bg-green-50 rounded-full animate-bounce"
                style={{ animationDuration: "1s", animationIterationCount: "2" }}
              >
                <CheckCircle className="w-10 h-10 text-green-500" />
              </div>
              <div className="text-center">
                <p className="text-gray-700 font-medium">Ready for download!</p>
                <p className="text-gray-400 text-sm mt-1">{fileName}</p>
              </div>
              <div className="flex gap-3 mt-2">
                <Button
                  onClick={handleDownload}
                  className="bg-orange-500 hover:bg-orange-600 text-white flex items-center gap-2 transition-all duration-300 hover:scale-105"
                >
                  <Download className="w-4 h-4" />
                  Download PDF
                </Button>
                <Button
                  onClick={handleReset}
                  variant="outline"
                  className="border-gray-300 text-gray-600 hover:bg-gray-50 transition-all duration-300 bg-transparent"
                >
                  Upload Another
                </Button>
              </div>
            </div>
          )}
        </Card>

        {/* Footer */}
        <footer className="w-full mt-6 animate-fade-in text-center text-sm text-gray-500" style={{ animationDelay: "0.4s" }}>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-2">
            <p>
              Built by <a className="font-medium text-gray-700 hover:underline" href="https://mitul-khemani-portfolio.vercel.app/">Mitul Khemani</a>
            </p>
            <span className="hidden sm:inline text-gray-300">•</span>
            <p>
              for <span className="font-medium text-orange-500">New Durga Agencies</span>, Ujjain
            </p>
          </div>

          <p className="mt-2 text-xs text-gray-400">© {new Date().getFullYear()} All rights reserved.</p>
        </footer>
      </div>

      {/* Fixed Terms box (bottom-left) — positioned out of document flow so layout/background remain unchanged */}
      <div className="fixed left-4 bottom-4 z-50 bg-white bg-opacity-95 border border-gray-100 rounded-md shadow-md p-3 max-w-xs text-xs text-gray-700">
        <h3 className="text-sm font-semibold mb-1">Terms and Condition</h3>
        <p className="leading-tight">1. This tool is provided to help with document processing. It may produce errors so, please verify all results before relying on them.</p>
        <p className="mt-1 leading-tight">2. Any Error caused will be completely fault of the user. Mitul Khemani will not be responsible for any errors.</p>
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(-10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes scale-in {
          from { opacity: 0; transform: scale(0.95); }
          to { opacity: 1; transform: scale(1); }
        }
        @keyframes progress {
          from { width: 0%; }
          to { width: 100%; }
        }
        .animate-fade-in {
          animation: fade-in 0.5s ease-out forwards;
        }
        .animate-scale-in {
          animation: scale-in 0.4s ease-out forwards;
        }
        .animate-progress {
          animation: progress 1.5s ease-in-out forwards;
        }
      `}</style>
    </div>
  )
}
