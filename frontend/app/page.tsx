'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'

export default function Home() {
  const features = [
    {
      title: "3D-планирование лечения",
      description: "Используем современные технологии для визуализации результатов до начала лечения"
    },
    {
      title: "Цифровые оттиски",
      description: "Забудьте о неприятных процедурах. Используем только цифровые сканеры"
    },
    {
      title: "Виртуальная консультация",
      description: "Первичная консультация возможна онлайн. Экономьте своё время"
    }
  ]

  return (
    <div className="pt-20">
      {/* Hero Section */}
      <section className="min-h-[60vh] flex items-center bg-gradient-to-b from-gray-50 to-white">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-4xl md:text-6xl font-light mb-6"
            >
              Создаем улыбки будущего
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl text-gray-600 mb-8"
            >
              Используем инновационные технологии и индивидуальный подход 
              для достижения идеального результата
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <Link 
                href="/appointment"
                className="inline-block px-8 py-3 bg-gray-900 text-white rounded hover:bg-gray-800 transition-colors"
              >
                Записаться на консультацию
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.2 }}
                className="bg-gray-50 p-8 rounded-lg"
              >
                <h3 className="text-xl font-medium mb-4">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl font-light mb-8">Почему выбирают нас</h2>
            <p className="text-gray-600 mb-8">
              JML ORTHO - это современная ортодонтическая клиника, где опыт и инновации 
              создают прекрасные улыбки. Мы специализируемся на исправлении прикуса 
              с использованием передовых технологий и методик.
            </p>
            <ul className="text-left text-gray-600 space-y-2">
              <li>✓ Команда высококвалифицированных специалистов</li>
              <li>✓ Индивидуальный подход к каждому пациенту</li>
              <li>✓ Использование современного оборудования</li>
              <li>✓ Комфортные условия лечения</li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  )
}

