import { DownloadCard } from '@/components/download-card';
import { getChangelog, getLatest } from '@/lib/api';

export default async function HomePage() {
  const latest = await getLatest();
  const changelog = await getChangelog();

  return (
    <main className="mx-auto max-w-4xl p-8">
      <h1 className="mb-4 text-4xl font-bold">TeleMusik</h1>
      <p className="mb-8 text-zinc-300">Android-клиент для стриминга музыки из публичных Telegram-каналов.</p>
      {latest ? <DownloadCard version={latest.version} url={latest.download_url} /> : <p>APK пока недоступен.</p>}
      <section className="mt-8">
        <h2 className="mb-3 text-2xl font-semibold">Changelog</h2>
        <ul className="space-y-4">
          {changelog.map((item: { version: string; changelog: string }) => (
            <li key={item.version} className="rounded border border-zinc-800 p-4">
              <p className="font-medium">v{item.version}</p>
              <p className="text-zinc-300">{item.changelog}</p>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
