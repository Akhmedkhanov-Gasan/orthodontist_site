'use client'

import { useEffect, useState } from 'react'

interface LightboxImageProps {
  src: string
  alt: string
  className?: string
  wrapperClassName?: string
}

export default function LightboxImage({
  src,
  alt,
  className = '',
  wrapperClassName = '',
}: LightboxImageProps) {
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    if (!isOpen) {
      return
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsOpen(false)
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [isOpen])

  return (
    <>
      <button
        type="button"
        onClick={() => setIsOpen(true)}
        className={`block cursor-zoom-in overflow-hidden rounded-lg ${wrapperClassName}`}
      >
        <img src={src} alt={alt} className={className} />
      </button>

      {isOpen && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 p-4"
          onClick={() => setIsOpen(false)}
        >
          <button
            type="button"
            className="absolute right-4 top-4 rounded bg-white/90 px-3 py-1 text-2xl leading-none text-gray-900 hover:bg-white"
            onClick={() => setIsOpen(false)}
            aria-label="Close"
          >
            x
          </button>

          <img
            src={src}
            alt={alt}
            className="max-h-[90vh] max-w-[90vw] rounded-lg object-contain"
            onClick={(event) => event.stopPropagation()}
          />
        </div>
      )}
    </>
  )
}
