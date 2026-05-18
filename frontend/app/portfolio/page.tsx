'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { apiBase, withSlash } from '@/utils/url';

export default function Portfolio() {
  const [works, setWorks] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${apiBase}/api/works/`)
        .then(res => res.json())
        .then(data => {
          const arr = Array.isArray(data) ? data : data.results ?? [];
          setWorks(arr);
        })
        .catch(console.error);
  }, []);

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
              Результаты лечения наших пациентов — лучшее подтверждение нашего профессионализма
            </p>
          </motion.div>

          {works.length === 0 ? (
              <p className="text-center text-gray-600">Загрузка...</p>
          ) : (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {works.map((work, index) => (
                    <motion.div
                        key={work.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: index * 0.1 }}
                        className="bg-gray-50 p-8 rounded-lg"
                    >
                      {work.image && (
                          <div className="aspect-square mb-4">
                            <img
                                src={`${apiBase}${withSlash(work.image)}`}
                                alt={work.title}
                                className="w-full h-full object-cover rounded-lg"
                            />
                          </div>
                      )}
                      <h3 className="text-xl font-medium mb-2">{work.title}</h3>
                      <p className="text-gray-600">{work.description}</p>
                    </motion.div>
                ))}
              </div>
          )}
        </div>
      </div>
  );
}
