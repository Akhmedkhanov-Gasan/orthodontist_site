// src/lib/url.ts
export const apiBase =
    (process.env.NEXT_PUBLIC_API_URL ?? '').replace(/\/$/, '');

export const withSlash = (path: string) =>
    path.startsWith('/') ? path : `/${path}`;
