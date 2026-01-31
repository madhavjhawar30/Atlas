/**
 * Upload Panel Component
 * Upload functionality disabled - view-only mode
 */
export default function UploadPanel() {
  return (
    <div className="bg-neural-card rounded-lg p-4 shadow-xl border border-gray-700">
      <h3 className="text-lg font-semibold mb-3 text-white flex items-center">
        <span className="mr-2">📤</span>
        Upload Images
      </h3>
      
      <div className="border-2 border-dashed rounded-lg p-6 text-center border-gray-600 bg-gray-800/30 opacity-60">
        <div className="text-4xl mb-2">🚫</div>
        <p className="text-sm text-gray-400 mb-1">
          Upload disabled
        </p>
        <p className="text-xs text-gray-500">
          View-only mode - explore existing images
        </p>
      </div>
      
      <div className="mt-3 text-xs text-gray-500">
        <p>• Upload functionality not available</p>
        <p>• View and explore existing images only</p>
      </div>
    </div>
  )
}

