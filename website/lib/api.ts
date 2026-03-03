const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export async function getLatest() {
  try {
    const r = await fetch(`${API}/app/latest`, { cache: 'no-store' });
    if (!r.ok) return null;
    return r.json();
  } catch {
    return null;
  }
}

export async function getChangelog() {
  try {
    const r = await fetch(`${API}/app/changelog`, { cache: 'no-store' });
    if (!r.ok) return [];
    return r.json();
  } catch {
    return [];
  }
}
