/**
 * Node Detail Panel Component
 * Shows details about selected node and its neighbors
 */
import { useStore } from '../store'

export default function NodeDetailPanel() {
  const { selectedNode, getImageById, getNeighbors, setSelectedNode } = useStore()
  
  if (!selectedNode) return null
  
  const image = getImageById(selectedNode)
  const neighbors = getNeighbors(selectedNode)
  
  if (!image) return null
  
  return (
    <div className="absolute top-24 right-6 z-10 w-80 max-h-[calc(100vh-8rem)] overflow-y-auto">
      <div className="bg-neural-card rounded-lg shadow-xl border border-gray-700 animate-fade-in">
        {/* Header */}
        <div className="p-4 border-b border-gray-700 flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">Image Details</h3>
          <button
            onClick={() => setSelectedNode(null)}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>
        
        {/* Image Info */}
        <div className="p-4 space-y-3">
          {/* Actual Image */}
          <div className="bg-neural-bg rounded-lg overflow-hidden">
            <img 
              src={`http://localhost:8000/images/${selectedNode}`}
              alt={image.filename}
              className="w-full h-auto object-contain max-h-64"
              onError={(e) => {
                e.target.onerror = null;
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'flex';
              }}
            />
            <div className="hidden flex-col items-center justify-center p-8">
              <div className="text-5xl mb-2">🖼️</div>
              <p className="text-sm text-gray-400">Image not available</p>
            </div>
            <p className="text-sm text-gray-400 text-center py-2 border-t border-gray-700">{image.filename}</p>
          </div>
          
          {/* Metadata */}
          <div className="space-y-2">
            <div className="text-xs">
              <span className="text-gray-400">ID:</span>
              <span className="text-gray-300 ml-2 font-mono text-xs">
                {selectedNode.slice(0, 8)}...
              </span>
            </div>
            
            <div className="text-xs">
              <span className="text-gray-400">Position:</span>
              <span className="text-gray-300 ml-2 font-mono text-xs">
                ({image.coords[0].toFixed(2)}, {image.coords[1].toFixed(2)}, {image.coords[2].toFixed(2)})
              </span>
            </div>
            
            {image.labels && image.labels.length > 0 && (
              <div>
                <span className="text-gray-400 text-xs">Labels:</span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {image.labels.map((label, i) => (
                    <span
                      key={i}
                      className="px-2 py-1 bg-neural-accent/20 text-neural-glow text-xs rounded"
                    >
                      {label.name}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
        
        {/* Neighbors */}
        {neighbors.length > 0 && (
          <>
            <div className="px-4 py-2 border-t border-gray-700">
              <h4 className="text-sm font-semibold text-white">
                Similar Images ({neighbors.length})
              </h4>
            </div>
            
            <div className="p-4 space-y-2 max-h-64 overflow-y-auto">
              {neighbors.slice(0, 8).map((neighbor) => (
                <div
                  key={neighbor.id}
                  onClick={() => setSelectedNode(neighbor.id)}
                  className="
                    flex items-center justify-between p-2 
                    bg-neural-bg hover:bg-gray-700 rounded-lg 
                    cursor-pointer transition-colors
                  "
                >
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-neural-accent/20 rounded overflow-hidden flex-shrink-0">
                      <img 
                        src={`http://localhost:8000/images/${neighbor.id}`}
                        alt={neighbor.image.filename}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.style.display = 'none';
                          const fallback = document.createElement('div');
                          fallback.className = 'w-8 h-8 flex items-center justify-center text-lg';
                          fallback.textContent = '🖼️';
                          e.target.parentNode.appendChild(fallback);
                        }}
                      />
                    </div>
                    <div>
                      <p className="text-sm text-gray-300 truncate max-w-[150px]">
                        {neighbor.image.filename}
                      </p>
                      <p className="text-xs text-gray-500">
                        {(neighbor.weight * 100).toFixed(0)}% similar
                      </p>
                    </div>
                  </div>
                  <div className="text-gray-400">→</div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}

