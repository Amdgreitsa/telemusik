const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

type LatestResponse = { version: string; download_url: string };
type ChangelogResponse = { version: string; changelog: string }[];

async function safeFetch<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${API}${path}`, { cache: 'no-store' });
    if (!response.ok) return fallback;
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

export async function getLatest(): Promise<LatestResponse | null> {
  return safeFetch<LatestResponse | null>('/app/latest', null);
}

export async function getChangelog(): Promise<ChangelogResponse> {
  return safeFetch<ChangelogResponse>('/app/changelog', []);
}

export async function getHealth(): Promise<{ status: string } | null> {
  return safeFetch<{ status: string } | null>('/health', null);
}
