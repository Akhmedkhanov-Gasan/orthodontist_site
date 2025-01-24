'use client';

import React from 'react';
import { motion } from 'framer-motion';

export default function Portfolio() {
  const categories = [
    'Брекет-системы',
    'Элайнеры',
    'Исправление прикуса',
    'Эстетическая ортодонтия',
  ];

  return (
    <div className="pt-32 pb-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-3xl mx-auto text-center mb-16"
        >
          <h1 className="text-4xl font-light mb-6">Наши работы</h1>
          <p className="text-gray-600">
            Результаты лечения наших пациентов - лучшее подтверждение нашего
            профессионализма
          </p>
        </motion.div>
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {categories.map((category) => (
            <button
              key={category}
              className="px-6 py-2 bg-gray-50 rounded-full hover:bg-gray-100 transition-colors"
            >
              {category}
            </button>
          ))}
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {[...Array(6)].map((_, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: index * 0.1 }}
              className="bg-gray-50 p-8 rounded-lg"
            >
              <div className="aspect-square bg-gray-100 rounded mb-4" />
              <h3 className="text-xl font-medium mb-2">
                Пример работы {index + 1}
              </h3>
              <p className="text-gray-600">
                Срок лечения: 18 месяцев
                <br />
                Использованная система: Damon Clear
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
