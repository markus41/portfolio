export function getApiKey() {
  // Prioritise environment variables injected at build time via Vite.
  const envKey = import.meta?.env?.VITE_API_KEY;
  if (envKey && envKey !== 'undefined') {
    return envKey;
  }

  // Fallback to runtime configuration (e.g. window.APP_CONFIG.apiKey)
  if (typeof window !== 'undefined' && window.APP_CONFIG?.apiKey) {
    return window.APP_CONFIG.apiKey;
  }

  return '';
}

