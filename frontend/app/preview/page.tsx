"use client"

import React, { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"

export default function PreviewPage() {
  const [dataUrl, setDataUrl] = useState<string | null>(null)
  const [fileName, setFileName] = useState<string>("translated_document.pdf")
  const router = useRouter()

  useEffect(() => {
    const data = sessionStorage.getItem("translated_pdf_data")
    const name = sessionStorage.getItem("translated_pdf_name")
    if (!data) {
      // No preview available — go back
      router.replace("/")
      return
    }
    setDataUrl(data)
    if (name) setFileName(name)
  }, [router])

  const handleDownload = () => {
    if (!dataUrl) return
    const a = document.createElement("a")
    a.href = dataUrl
    a.download = fileName
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  return (
    <div className="min-h-screen bg-white p-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Preview — {fileName}</h2>
          <div className="flex gap-2">
            <Button onClick={() => router.push("/") } variant="ghost">Back</Button>
            <Button onClick={handleDownload}>Download</Button>
          </div>
        </div>

        {dataUrl ? (
          <iframe
            title="PDF Preview"
            src={dataUrl}
            className="w-full h-[80vh] border"
          />
        ) : (
          <div className="p-8 text-center text-gray-500">Preparing preview...</div>
        )}
      </div>
    </div>
  )
}
