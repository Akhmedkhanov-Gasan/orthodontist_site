'use client'

import { useEffect, useState } from 'react'
import { apiBase } from '@/utils/url'

interface FooterData {
  footer_title: string
  footer_description: string
  footer_copyright: string
  footer_contacts: string
}

export default function Footer() {
  const [footerData, setFooterData] = useState<FooterData | null>(null)

  useEffect(() => {
    fetch(`${apiBase}/api/home/`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Footer content not found')
        }

        return res.json()
      })
      .then((data) => {
        setFooterData(data)
      })
      .catch((err) => {
        console.error('Error fetching footer data:', err)
      })
  }, [])

  const footerTitle = footerData?.footer_title || 'JML ORTHO'
  const footerDescription =
    footerData?.footer_description || 'Профессиональная ортодонтическая клиника'
  const footerCopyright =
    footerData?.footer_copyright || '© 2025 JML ORTHO. Все права защищены.'
  const footerContacts =
    footerData?.footer_contacts ||
    'г. Москва, ул. Примерная, д. 1 | Тел: +7 (495) 123-45-67'

  return (
    <footer className="bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-wrap justify-between items-center">
          <div className="w-full md:w-auto text-center md:text-left mb-4 md:mb-0">
            <h3 className="text-lg font-medium mb-2">{footerTitle}</h3>
            <p className="text-sm text-gray-600">{footerDescription}</p>
          </div>

          <div className="w-full md:w-auto text-center md:text-right">
            <p className="text-sm text-gray-600">{footerCopyright}</p>
            <p className="text-sm text-gray-600 mt-2">{footerContacts}</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
