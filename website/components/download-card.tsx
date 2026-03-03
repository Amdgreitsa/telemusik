export function DownloadCard({ version, url }: { version: string; url: string }) {
  return (
    <div className="rounded-xl border border-zinc-800 p-6">
      <h2 className="text-xl font-semibold">Последняя версия: {version}</h2>
      <a className="mt-4 inline-block rounded bg-emerald-500 px-4 py-2 font-medium text-black" href={url}>
        Скачать APK
      </a>
    </div>
  );
}
