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
    <header
      className={`fixed top-0 z-50 w-full transition-all duration-300 ${
        isScrolled ? 'bg-white py-2 shadow-md' : 'bg-white/95 py-4'
      }`}
    >
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center">
          <Link href="/" className="mb-4 text-2xl font-light tracking-wider">
            JML ORTHO
          </Link>

          <button
            type="button"
            onClick={() => setIsOpen(!isOpen)}
            className="absolute right-4 top-4 md:hidden"
            aria-label="Открыть меню"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>

          <nav
            className={`${
              isOpen ? 'flex' : 'hidden'
            } w-full flex-col items-center md:flex md:w-auto md:flex-row`}
          >
            <div className="flex flex-col items-center space-y-4 text-sm md:flex-row md:space-x-8 md:space-y-0">
              <Link
                href="/"
                className="transition-colors hover:text-gray-600"
                onClick={() => setIsOpen(false)}
              >
                Главная
              </Link>

              <Link
                href="/about"
                className="transition-colors hover:text-gray-600"
                onClick={() => setIsOpen(false)}
              >
                О нас
              </Link>

              <Link
                href="/about/team"
                className="transition-colors hover:text-gray-600"
                onClick={() => setIsOpen(false)}
              >
                Команда
              </Link>

              <Link
                href="/portfolio"
                className="transition-colors hover:text-gray-600"
                onClick={() => setIsOpen(false)}
              >
                Наши работы
              </Link>

              <Link
                href="/appointment"
                className="rounded bg-gray-900 px-6 py-2 text-white transition-colors hover:bg-gray-800"
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