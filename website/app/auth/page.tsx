'use client';

import { useState } from 'react';

export default function AuthPage() {
  const [telegramUserId, setTelegramUserId] = useState('');
  const [token, setToken] = useState('');

  async function login() {
    const base = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
    const response = await fetch(`${base}/auth/telegram`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ telegram_user_id: telegramUserId }),
    });
    const data = await response.json();
    setToken(data.access_token || '');
  }

  return (
    <main className="mx-auto max-w-2xl p-8">
      <h1 className="text-3xl font-bold">Авторизация</h1>
      <p className="mt-3 text-zinc-300">Техническая страница получения JWT для теста API.</p>
      <input
        className="mt-5 w-full rounded border border-zinc-700 bg-zinc-900 p-3"
        value={telegramUserId}
        onChange={(e) => setTelegramUserId(e.target.value)}
        placeholder="Telegram user id"
      />
      <button onClick={login} className="mt-4 rounded bg-emerald-500 px-4 py-2 font-medium text-black">Войти</button>
      {token && <pre className="mt-5 overflow-auto rounded border border-zinc-700 p-3 text-xs">{token}</pre>}
    </main>
  );
}
