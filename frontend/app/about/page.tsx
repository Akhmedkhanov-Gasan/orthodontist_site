'use client'

import { motion } from 'framer-motion'

export default function About() {
  const values = [
    {
      title: "Профессионализм",
      description: "Постоянное совершенствование навыков и применение передовых методик"
    },
    {
      title: "Инновации",
      description: "Использование современного оборудования и цифровых технологий"
    },
    {
      title: "Забота",
      description: "Индивидуальный подход и внимание к каждому пациенту"
    }
  ]

  return (
    <div className="pt-32 pb-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-3xl mx-auto text-center mb-16"
        >
          <h1 className="text-4xl font-light mb-6">О нас</h1>
          <p className="text-gray-600">
            JML ORTHO - это современная ортодонтическая клиника, где опыт и инновации 
            создают прекрасные улыбки. Мы специализируемся на исправлении прикуса 
            с использованием передовых технологий и методик.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {values.map((value, index) => (
            <motion.div
              key={value.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              className="text-center"
            >
              <h3 className="text-xl font-medium mb-4">{value.title}</h3>
              <p className="text-gray-600">{value.description}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="max-w-3xl mx-auto text-center"
        >
          <h2 className="text-2xl font-light mb-6">Наша команда</h2>
          <p className="text-gray-600">
            Наши специалисты регулярно проходят обучение и стажировки в ведущих 
            клиниках мира, чтобы предоставлять вам лечение на высочайшем уровне.
          </p>
        </motion.div>
      </div>
    </div>
  )
}

