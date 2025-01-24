'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function Services() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/services/`)
      .then((res) => res.json())
      .then((data) => setServices(data))
      .catch((err) => console.error(err));
  }, []);

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

        {services.length === 0 ? (
          <p className="text-center text-gray-600">Загрузка...</p>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {services.map((service, index) => (
              <motion.div
                key={service.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.2 }}
                className="bg-gray-50 p-8 rounded-lg"
              >
                <h2 className="text-2xl font-light mb-4">{service.title}</h2>
                <p className="text-gray-600 mb-6">{service.description}</p>
                {service.price && (
                  <p className="text-gray-600 font-medium mb-4">Цена: {service.price}₽</p>
                )}
                {service.image && (
                  <img
                    src={`${process.env.NEXT_PUBLIC_API_URL}${service.image}`}
                    alt={service.title}
                    className="rounded-lg w-full h-auto object-cover"
                  />
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
