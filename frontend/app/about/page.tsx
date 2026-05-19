'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { apiBase, withSlash } from '@/utils/url'

interface TeamMember {
  id: number
  name: string
  position: string
  description: string
  photo: string | null
  work_start_date: string | null
  experience_years: number | null
  order: number
  is_active: boolean
}

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

  team_title: string
  team_text: string
  team_members: TeamMember[]

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

  const hasTeamSection =
    aboutData.team_title || aboutData.team_text || aboutData.team_members?.length > 0

  return (
    <div className="bg-white pt-32 pb-20">
      <div className="container mx-auto px-4">
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mx-auto mb-16 max-w-4xl text-center"
        >
          <h1 className="mb-6 text-4xl font-light">{aboutData.title}</h1>

          {aboutData.content && (
            <p className="mx-auto max-w-3xl break-words text-lg leading-relaxed text-gray-600 [overflow-wrap:anywhere]">
              {aboutData.content}
            </p>
          )}

          {aboutData.image && (
            <div className="mx-auto mt-10 max-w-3xl overflow-hidden rounded-lg bg-gray-100">
              <img
                src={`${apiBase}${withSlash(aboutData.image)}`}
                alt=""
                className="h-auto w-full"
              />
            </div>
          )}
        </motion.section>

        {values.length > 0 && (
          <section className="mb-20">
            <div className="grid gap-8 md:grid-cols-3">
              {values.map((value, index) => (
                <motion.div
                  key={`${value.title}-${index}`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: index * 0.15 }}
                  className="rounded-lg bg-gray-50 p-8 text-center"
                >
                  {value.title && (
                    <h3 className="mb-4 text-xl font-medium">
                      {value.title}
                    </h3>
                  )}

                  {value.description && (
                    <p className="break-words leading-relaxed text-gray-600 [overflow-wrap:anywhere]">
                      {value.description}
                    </p>
                  )}
                </motion.div>
              ))}
            </div>
          </section>
        )}

        {hasTeamSection && (
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="mx-auto max-w-3xl text-center"
          >
            {aboutData.team_title && (
              <h2 className="mb-6 text-3xl font-light">
                {aboutData.team_title}
              </h2>
            )}

            {aboutData.team_text && (
              <p className="mb-8 break-words text-lg leading-relaxed text-gray-600 [overflow-wrap:anywhere]">
                {aboutData.team_text}
              </p>
            )}

            {aboutData.team_members?.length > 0 && (
              <Link
                href="/about/team"
                className="inline-block rounded bg-gray-900 px-8 py-3 text-white transition-colors hover:bg-gray-800"
              >
                Смотреть команду
              </Link>
            )}
          </motion.section>
        )}
      </div>
    </div>
  )
}