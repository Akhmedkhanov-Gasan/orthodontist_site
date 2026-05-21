'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { apiBase, withSlash } from '@/utils/url'

interface AboutPageData {
  id: number
  title: string
  content: string
  image: string | null

  value_1_title: string
  value_1_description: string
  value_2_title: string
  value_2_description: string
  value_3_title: string
  value_3_description: string

  updated_at: string
}

export default function About() {
  const [aboutData, setAboutData] = useState<AboutPageData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${apiBase}/api/about/`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('About page content not found')
        }

        return res.json()
      })
      .then((data) => {
        setAboutData(data)
      })
      .catch((err) => {
        console.error('Error fetching about data:', err)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div className="min-h-screen bg-white" />
  }

  if (!aboutData) {
    return (
      <div className="pt-40 text-center text-gray-600">
        Страница «О нас» не настроена в админке.
      </div>
    )
  }

  const values = [
    {
      title: aboutData.value_1_title,
      description: aboutData.value_1_description,
    },
    {
      title: aboutData.value_2_title,
      description: aboutData.value_2_description,
    },
    {
      title: aboutData.value_3_title,
      description: aboutData.value_3_description,
    },
  ].filter((value) => value.title || value.description)

  return (
    <div className="bg-white pt-28 pb-8">
      <div className="container mx-auto px-4">
        <motion.section
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mx-auto mb-10 max-w-7xl"
        >
          <div
            className={`grid items-center gap-10 rounded-lg bg-gray-50/70 p-8 md:p-10 lg:p-12 ${
              aboutData.image ? 'lg:grid-cols-[1.05fr_0.95fr]' : ''
            }`}
          >
            {aboutData.image && (
              <div className="overflow-hidden rounded-lg bg-white shadow-sm">
                <img
                  src={`${apiBase}${withSlash(aboutData.image)}`}
                  alt=""
                  className="aspect-[4/3] w-full object-cover object-center"
                />
              </div>
            )}

            <div className={aboutData.image ? 'text-left' : 'text-center'}>
              <h1 className="mb-6 text-4xl font-light text-gray-950">
                {aboutData.title}
              </h1>

              {aboutData.content && (
                <p className="max-w-xl break-words text-lg leading-8 text-gray-600 [overflow-wrap:anywhere]">
                  {aboutData.content}
                </p>
              )}
            </div>
          </div>
        </motion.section>

        {values.length > 0 && (
          <section className="pt-40 pb-8 md:pt-48 md:pb-10">
            <div className="grid gap-8 md:grid-cols-3">
              {values.map((value, index) => (
                <motion.div
  key={`${value.title}-${index}`}
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.8, delay: index * 0.2 }}
  className="rounded-lg bg-gray-50 p-8"
>
  {value.title && (
    <h3 className="mb-4 text-xl font-medium">{value.title}</h3>
  )}

  {value.description && (
    <p className="text-gray-600">{value.description}</p>
  )}
</motion.div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  )
}