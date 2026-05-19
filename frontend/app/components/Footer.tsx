'use client'

import { useEffect, useState } from 'react'
import { apiBase } from '@/utils/url'

interface FooterData {
  footer_title: string
  footer_description: string
  footer_copyright: string
  footer_contacts: string
  telegram_url: string
  instagram_url: string
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
  const telegramUrl = footerData?.telegram_url || ''
  const instagramUrl = footerData?.instagram_url || ''

  return (
    <footer className="bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-wrap justify-between items-center">
          <div className="w-full md:w-auto text-center md:text-left mb-4 md:mb-0">
            <h3 className="text-lg font-medium mb-2">{footerTitle}</h3>
            <p className="text-sm text-gray-600">{footerDescription}</p>
          </div>

    <div className="w-full md:w-auto text-center md:text-right">
  <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-2 md:justify-end">
    <p className="text-sm text-gray-600">{footerCopyright}</p>

    {(telegramUrl || instagramUrl) && (
      <div className="flex items-center gap-3">
        {telegramUrl && (
          <a
            href={telegramUrl}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Telegram"
            className="inline-flex h-10 w-10 items-center justify-center rounded-full transition-opacity hover:opacity-70"
          >
            <img
              src="/icons/telegram.svg"
              alt=""
              className="h-9 w-9 object-contain"
            />
          </a>
        )}

        {instagramUrl && (
          <a
            href={instagramUrl}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Instagram"
            className="inline-flex h-10 w-10 items-center justify-center rounded-full transition-opacity hover:opacity-70"
          >
            <img
              src="/icons/instagram.svg"
              alt=""
              className="h-9 w-9 object-contain"
            />
          </a>
        )}
      </div>
    )}
  </div>

  <p className="text-sm text-gray-600 mt-2">{footerContacts}</p>
</div>
        </div>
      </div>
    </footer>
  )
}
