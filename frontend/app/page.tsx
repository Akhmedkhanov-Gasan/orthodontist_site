'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { apiBase, withSlash } from '@/utils/url'

interface HomePageData {
  id: number
  hero_title: string
  hero_subtitle: string
  hero_button_text: string
  hero_button_url: string
  hero_image: string | null

  feature_1_title: string
  feature_1_description: string
  feature_2_title: string
  feature_2_description: string
  feature_3_title: string
  feature_3_description: string

  about_title: string
  about_text: string
  about_bullet_1: string
  about_bullet_2: string
  about_bullet_3: string
  about_bullet_4: string

  updated_at: string
}

export default function Home() {
  const [homeData, setHomeData] = useState<HomePageData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${apiBase}/api/home/`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Home page content not found')
        }

        return res.json()
      })
      .then((data) => {
        setHomeData(data)
      })
      .catch((err) => {
        console.error('Error fetching home page data:', err)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div className="min-h-screen bg-white" />
  }

  if (!homeData) {
    return (
      <div className="pt-40 text-center text-gray-600">
        Главная страница не настроена в админке.
      </div>
    )
  }

  const features = [
    {
      title: homeData.feature_1_title,
      description: homeData.feature_1_description,
    },
    {
      title: homeData.feature_2_title,
      description: homeData.feature_2_description,
    },
    {
      title: homeData.feature_3_title,
      description: homeData.feature_3_description,
    },
  ]

  const aboutBullets = [
    homeData.about_bullet_1,
    homeData.about_bullet_2,
    homeData.about_bullet_3,
    homeData.about_bullet_4,
  ].filter(Boolean)

  return (
    <div className="bg-white">
      <section className="relative isolate min-h-[720px] overflow-hidden bg-white pt-36 pb-20 md:min-h-[820px] md:pt-40">
        {homeData.hero_image && (
          <div className="pointer-events-none absolute inset-x-0 top-[100px] bottom-0 z-0 md:top-[120px]">
            <img
              src={`${apiBase}${withSlash(homeData.hero_image)}`}
              alt=""
              className="h-full w-full object-cover object-center opacity-80"
            />

            <div className="absolute inset-0 bg-white/20" />
            <div className="absolute inset-x-0 top-0 h-32 bg-gradient-to-b from-white via-white/80 to-transparent" />
            <div className="absolute inset-x-0 bottom-0 h-32 bg-gradient-to-t from-white via-white/70 to-transparent" />
          </div>
        )}

        <div className="container relative z-10 mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="mb-6 text-4xl font-light leading-tight text-gray-900 md:text-6xl"
            >
              {homeData.hero_title}
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="mx-auto mb-8 max-w-2xl text-xl leading-relaxed text-gray-600"
            >
              {homeData.hero_subtitle}
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <Link
                href={homeData.hero_button_url || '/appointment'}
                className="inline-block rounded bg-gray-900 px-8 py-3 text-white transition-colors hover:bg-gray-800"
              >
                {homeData.hero_button_text}
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      <section className="pt-14 pb-4 md:pt-16 md:pb-6">
        <div className="container mx-auto px-4">
          <div className="grid gap-8 md:grid-cols-3">
            {features.map((feature, index) => (
              <motion.div
                key={`${feature.title}-${index}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.2 }}
                className="rounded-lg bg-gray-50 p-8"
              >
                <h3 className="mb-4 text-xl font-medium">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-gray-50 pt-8 pb-20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-8 text-3xl font-light">{homeData.about_title}</h2>

            <p className="mb-8 text-gray-600">{homeData.about_text}</p>

            <ul className="space-y-2 text-left text-gray-600">
              {aboutBullets.map((bullet) => (
                <li key={bullet}>✓ {bullet}</li>
              ))}
            </ul>
          </div>
        </div>
      </section>
    </div>
  )
}
