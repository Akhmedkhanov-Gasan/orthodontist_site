'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Menu, X } from 'lucide-react'
import { usePathname } from 'next/navigation'

export default function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const [isScrolled, setIsScrolled] = useState(false)
  const pathname = usePathname()

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

const isActive = (href: string) => pathname === href

const navLinkClass = (href: string) =>
  `rounded border px-4 py-2 transition-colors ${
    isActive(href)
      ? 'border-gray-900 bg-gray-900 text-white'
      : 'border-transparent text-gray-900 hover:border-gray-300 hover:text-gray-600'
  }`

const appointmentClass = navLinkClass('/appointment')

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
            <div className="flex flex-col items-center gap-1 text-sm md:flex-row md:gap-1">
              <Link
                href="/"
                className={navLinkClass('/')}
                onClick={() => setIsOpen(false)}
              >
                Главная
              </Link>

              <Link
                href="/about"
                className={navLinkClass('/about')}
                onClick={() => setIsOpen(false)}
              >
                О нас
              </Link>

              <Link
                href="/about/team"
                className={navLinkClass('/about/team')}
                onClick={() => setIsOpen(false)}
              >
                Команда
              </Link>

              <Link
                href="/portfolio"
                className={navLinkClass('/portfolio')}
                onClick={() => setIsOpen(false)}
              >
                Наши работы
              </Link>

              <Link
                href="/appointment"
                className={appointmentClass}
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