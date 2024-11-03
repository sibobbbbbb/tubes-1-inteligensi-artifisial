export default function ImageModal({ src, alt, onClose }) {
    return (
      <div 
        className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
        onClick={onClose} // Menutup modal ketika latar belakang diklik
      >
        <div className="relative" onClick={(e) => e.stopPropagation()}>
          <button onClick={onClose} className="absolute top-2 right-2 text-black text-2xl">&times;</button>
          <img src={src} alt={alt} className="max-w-full max-h-full" />
        </div>
      </div>
    );
  }
  