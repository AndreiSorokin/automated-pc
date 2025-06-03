'use client'

import React, { useEffect, useState } from 'react'


const Landing = () => {
  const [originalImage, setOriginalImage] = useState<string | null>(null)
  const [processedImage, setProcessedImage] = useState<string | null>(null)

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onloadend = () => {
      setOriginalImage(reader.result as string)
      // Here call the background-removal API
      // then setProcessedImage(URL.createObjectURL(new Blob([response.data])));
    }
    reader.readAsDataURL(file)
  }

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-3xl font-bold mb-6">Image Background Remover</h1>

        {/* Upload Button */}
        <label className="inline-block cursor-pointer px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition">
          Upload Image
          <input
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="hidden"
          />
        </label>

        {/* Image Preview */}
        {originalImage && (
          <div className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h2 className="text-lg font-semibold mb-2">Original</h2>
              <img
                src={originalImage}
                alt="Original"
                className="rounded-xl shadow-md max-h-[400px] mx-auto"
              />
            </div>

            <div>
              <h2 className="text-lg font-semibold mb-2">Result</h2>
              {processedImage ? (
                <img
                  src={processedImage}
                  alt="Processed"
                  className="rounded-xl shadow-md max-h-[400px] mx-auto"
                />
              ) : (
                <div className="h-[400px] border-dashed border-2 border-gray-300 rounded-xl flex items-center justify-center text-gray-400">
                  Waiting for processing...
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  )
}

export default Landing
