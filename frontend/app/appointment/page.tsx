'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

/* ─────────── csrf cookie ─────────── */
function getCookie(name: string) {
  const m = document.cookie.match(`(?:^|; )${name}=([^;]*)`);
  return m ? decodeURIComponent(m[1]) : '';
}

const PHONE_RE = /^(?:\+7|8)\d{10}$/;

export default function Appointment() {
  const [name,  setName]  = useState('');
  const [phone, setPhone] = useState('');
  const [preferredDate, setPreferredDate] = useState('');
  const [comment, setComment] = useState('');

  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    setErrorMessage('');

    if (!name.trim()) {
      setErrorMessage('Введите имя');
      setStatus('error');
      return;
    }
    if (!PHONE_RE.test(phone)) {
      setErrorMessage('Неверный формат номера телефона');
      setStatus('error');
      return;
    }

    try {
      await new Promise<void>((resolve) => window.grecaptcha.ready(() => resolve()));


      const token = await window.grecaptcha.execute(
          process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY!,
          { action: 'appointment' }
      );

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/appointments/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          name,
          phone,
          preferred_date: preferredDate,
          message: comment,
          recaptcha_token: token,
        }),
      });

      if (!res.ok) {
        const data = await res.json();          // { phone: ["..."], name: ["..."] }
        const key  = Object.keys(data)[0];
        setErrorMessage(data[key]?.[0] ?? 'Не удалось отправить форму');
        setStatus('error');
        return;
      }

      setStatus('success');
      setName(''); setPhone(''); setPreferredDate(''); setComment('');
    } catch (err) {
      console.error(err);
      setErrorMessage('Ошибка подключения к серверу');
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
            <h1 className="text-4xl font-light text-center mb-12">Запись на приём</h1>

            <form className="space-y-6" onSubmit={handleSubmit}>
              {/* имя */}
              <div>
                <label className="block text-sm font-medium mb-2">Ваше имя</label>
                <input
                    type="text"
                    title="Введите имя"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-gray-900"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Телефон</label>
                <input
                    type="tel"
                    title="+7 (8) 123 45 67"
                    required
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-gray-900"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Предпочтительная дата</label>
                <input
                    type="date"
                    required
                    value={preferredDate}
                    onChange={(e) => setPreferredDate(e.target.value)}
                    className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-gray-900"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Комментарий</label>
                <textarea
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    className="w-full px-4 py-2 border rounded h-32 focus:ring-2 focus:ring-gray-900"
                />
              </div>

              <button
                  type="submit"
                  disabled={status === 'loading'}
                  className="w-full px-8 py-3 bg-gray-900 text-white rounded hover:bg-gray-800 transition"
              >
                {status === 'loading' ? 'Отправка…' : 'Отправить заявку'}
              </button>
            </form>

            {status === 'success' && (
                <p className="text-green-500 mt-4 text-center">Заявка отправлена, мы свяжемся с вами!</p>
            )}
            {status === 'error' && errorMessage && (
                <p className="text-red-500 mt-4 text-center">{errorMessage}</p>
            )}
          </motion.div>
        </div>
      </div>
  );
}
