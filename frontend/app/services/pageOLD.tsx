'use client'

import { motion } from 'framer-motion'

export default function Services() {
  const services = [
    {
      title: "Брекет-системы",
      description: "Классические и самолигирующие брекеты для эффективного исправления прикуса",
      details: ["Металлические", "Керамические", "Сапфировые"]
    },
    {
      title: "Элайнеры",
      description: "Прозрачные капы для незаметного исправления положения зубов",
      details: ["Индивидуальное изготовление", "3D-планирование", "Комфортное ношение"]
    },
    {
      title: "Ортодонтическая подготовка",
      description: "Подготовка к протезированию и имплантации",
      details: ["Исправление положения зубов", "Создание места для имплантатов", "Коррекция прикуса"]
    }
  ]

  return (
    <div className="pt-32 pb-20">
      <div className="container mx-auto px-4">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-4xl font-light text-center mb-12"
        >
          Наши услуги
        </motion.h1>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <motion.div
              key={service.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              className="bg-gray-50 p-8 rounded-lg"
            >
              <h2 className="text-2xl font-light mb-4">{service.title}</h2>
              <p className="text-gray-600 mb-6">{service.description}</p>
              <ul className="space-y-2">
                {service.details.map((detail) => (
                  <li key={detail} className="text-gray-600">• {detail}</li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}

