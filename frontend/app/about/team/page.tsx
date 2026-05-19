'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
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
  team_title: string
  team_text: string
  team_members: TeamMember[]
}

function formatExperience(years: number) {
  if (years === 0) {
    return 'меньше года'
  }

  const lastDigit = years % 10
  const lastTwoDigits = years % 100

  if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
    return `${years} лет`
  }

  if (lastDigit === 1) {
    return `${years} год`
  }

  if (lastDigit >= 2 && lastDigit <= 4) {
    return `${years} года`
  }

  return `${years} лет`
}

export default function TeamPage() {
  const [aboutData, setAboutData] = useState<AboutPageData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${apiBase}/api/about/`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Team content not found')
        }

        return res.json()
      })
      .then((data) => {
        setAboutData(data)
      })
      .catch((err) => {
        console.error('Error fetching team data:', err)
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
        Команда не настроена в админке.
      </div>
    )
  }

  const teamMembers = aboutData.team_members ?? []

  return (
    <div className="bg-white pt-32 pb-20">
      <div className="container mx-auto px-4">
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mx-auto mb-14 max-w-3xl text-center"
        >
          <h1 className="mb-6 text-4xl font-light">
            {aboutData.team_title || 'Наша команда'}
          </h1>

          {aboutData.team_text && (
            <p className="break-words text-lg leading-relaxed text-gray-600 [overflow-wrap:anywhere]">
              {aboutData.team_text}
            </p>
          )}
        </motion.section>

        {teamMembers.length === 0 ? (
          <p className="text-center text-gray-600">
            Сотрудники пока не добавлены.
          </p>
        ) : (
          <div className="mx-auto max-w-5xl space-y-12">
            {teamMembers.map((member, index) => (
              <motion.article
                key={member.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                className="grid overflow-hidden rounded-lg bg-gray-50 md:grid-cols-[0.9fr_1.1fr]"
              >
                <div className="bg-gray-100">
                  {member.photo ? (
                    <img
                      src={`${apiBase}${withSlash(member.photo)}`}
                      alt={member.name}
                      className="h-full min-h-[360px] w-full object-cover object-center"
                    />
                  ) : (
                    <div className="flex min-h-[360px] items-center justify-center text-gray-400">
                      Фото не добавлено
                    </div>
                  )}
                </div>

                <div className="flex flex-col justify-center p-8 md:p-10">
                  <h2 className="mb-3 break-words text-3xl font-medium leading-tight [overflow-wrap:anywhere]">
                    {member.name}
                  </h2>

                  {member.position && (
                    <p className="mb-4 break-words text-base text-gray-500 [overflow-wrap:anywhere]">
                      {member.position}
                    </p>
                  )}

                  {member.experience_years !== null && (
                    <p className="mb-6 text-sm font-medium uppercase tracking-wide text-gray-700">
                      Стаж: {formatExperience(member.experience_years)}
                    </p>
                  )}

                  {member.description && (
                    <p className="break-words leading-relaxed text-gray-600 [overflow-wrap:anywhere]">
                      {member.description}
                    </p>
                  )}
                </div>
              </motion.article>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}