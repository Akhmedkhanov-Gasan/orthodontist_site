'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

export default function Appointment() {
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [preferredDate, setPreferredDate] = useState('');
  const [comment, setComment] = useState('');
  const [status, setStatus] = useState('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('loading');
    setErrorMessage('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/appointments/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          phone,
          email,
          preferred_date: preferredDate,
          message: comment,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        if (data.preferred_date) {
          setErrorMessage(data.preferred_date[0]);
        } else {
          setErrorMessage('Произошла ошибка при отправке.');
        }
        setStatus('error');
        return;
      }

      setStatus('success');
    } catch (error) {
      console.error(error);
      setErrorMessage('Ошибка подключения к серверу.');
      setStatus('error');
    }
  };

  return (
    <div className="pt-32 pb-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-3xl mx-auto"
        >
          <h1 className="text-4xl font-light text-center mb-12">Запись на прием</h1>

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Ваше имя</label>
              <input
                type="text"
                className="w-full px-4 py-2 border border-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-gray-900"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Телефон</label>
              <input
                type="tel"
                className="w-full px-4 py-2 border border-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-gray-900"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                type="email"
                className="w-full px-4 py-2 border border-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-gray-900"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Предпочтительная дата</label>
              <input
                type="date"
                className="w-full px-4 py-2 border border-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-gray-900"
                value={preferredDate}
                onChange={(e) => setPreferredDate(e.target.value)}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Комментарий</label>
              <textarea
                className="w-full px-4 py-2 border border-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-gray-900 h-32"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
              />
            </div>

            <button
              type="submit"
              className="w-full px-8 py-3 bg-gray-900 text-white rounded hover:bg-gray-800 transition-colors"
              disabled={status === 'loading'}
            >
              {status === 'loading' ? 'Отправка...' : 'Отправить заявку'}
            </button>
          </form>

          {status === 'success' && (
            <p className="text-green-500 mt-4 text-center">Запись успешно отправлена!</p>
          )}
          {status === 'error' && errorMessage && (
            <p className="text-red-500 mt-4 text-center">{errorMessage}</p>
          )}
        </motion.div>
      </div>
    </div>
  );
}
