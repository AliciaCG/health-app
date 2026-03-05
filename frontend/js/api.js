/**
 * api.js — all HTTP communication with the backend.
 * No DOM access here; returns data or throws errors.
 */

const API_BASE = 'http://localhost:8000';

/**
 * Shared fetch wrapper — centralises error handling.
 * @param {string} path
 * @param {RequestInit} [options]
 * @returns {Promise<any|null>} parsed JSON or null (for 204)
 */
async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const defaults = {
    headers: { 'Content-Type': 'application/json' },
    signal: AbortSignal.timeout(8000),
  };

  const response = await fetch(url, { ...defaults, ...options });

  if (response.status === 204) return null;

  const data = await response.json();

  if (!response.ok) {
    const message = data?.detail
      ?? `Request failed with status ${response.status}`;
    throw new Error(message);
  }

  return data;
}

// ── Public API surface ─────────────────────────────────────────────────────

const RecordsAPI = {
  /**
   * Check the API is reachable.
   * @returns {Promise<boolean>}
   */
  ping: async () => {
    try {
      await apiFetch('/health');
      return true;
    } catch {
      return false;
    }
  },

  /**
   * Fetch all records.
   * @returns {Promise<Record[]>}
   */
  list: () => apiFetch('/records/'),

  /**
   * Create a new record.
   * @param {{ firstname, lastname, age, sex, health }} payload
   * @returns {Promise<Record>}
   */
  create: (payload) => apiFetch('/records/', {
    method: 'POST',
    body: JSON.stringify(payload),
  }),

  /**
   * Delete a record by id.
   * @param {number} id
   * @returns {Promise<null>}
   */
  remove: (id) => apiFetch(`/records/${id}`, { method: 'DELETE' }),
};
