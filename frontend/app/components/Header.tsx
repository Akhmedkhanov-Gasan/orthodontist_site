'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Menu, X } from 'lucide-react'

export default function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <header className={`fixed w-full top-0 z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white shadow-md py-2' : 'bg-white/95 py-4'
    }`}>
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center">
          {/* Logo */}
          <Link href="/" className="text-2xl font-light tracking-wider mb-4">
            JML ORTHO
          </Link>

          {/* Mobile menu button */}
          <button 
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden absolute right-4 top-4"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>

          {/* Navigation */}
          <nav className={`${
            isOpen ? 'flex' : 'hidden'
          } md:flex flex-col md:flex-row items-center w-full md:w-auto`}>
            <div className="flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-8 text-sm">
              <Link 
                href="/" 
                className="hover:text-gray-600 transition-colors"
                onClick={() => setIsOpen(false)}
              >
                Главная
              </Link>
              <Link 
                href="/services" 
                className="hover:text-gray-600 transition-colors"
                onClick={() => setIsOpen(false)}
              >
                Услуги
              </Link>
              <Link 
                href="/about" 
                className="hover:text-gray-600 transition-colors"
                onClick={() => setIsOpen(false)}
              >
                О нас
              </Link>
              <Link 
                href="/portfolio" 
                className="hover:text-gray-600 transition-colors"
                onClick={() => setIsOpen(false)}
              >
                Наши работы
              </Link>
              <Link 
                href="/appointment" 
                className="px-6 py-2 bg-gray-900 text-white rounded hover:bg-gray-800 transition-colors"
                onClick={() => setIsOpen(false)}
              >
                Запись на прием
              </Link>
            </div>
          </nav>
        </div>
      </div>
    </header>
  )
}

