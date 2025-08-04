'use client';

import { useEffect } from 'react';
import Script from 'next/script';

export default function ClientInit() {
    // ❶ запрашиваем CSRF-cookie
    useEffect(() => {
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/csrf/`, {
            credentials: 'include',
            mode: 'cors',
        });
    }, []);

    // ❷ загружаем reCAPTCHA-скрипт
    return (
        <Script
            src={`https://www.google.com/recaptcha/api.js?render=${process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY}`}
            strategy="afterInteractive"
        />
    );
}
