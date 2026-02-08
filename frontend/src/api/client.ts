const TOKEN_KEY = 'wealth_access_token';
const REFRESH_KEY = 'wealth_refresh_token';

export function getAccessToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setTokens(access: string, refresh: string) {
  localStorage.setItem(TOKEN_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

async function refreshAccessToken(): Promise<string | null> {
  const refresh = localStorage.getItem(REFRESH_KEY);
  if (!refresh) return null;

  const res = await fetch('/api/auth/refresh/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
    credentials: 'include',
  });

  if (!res.ok) {
    clearTokens();
    return null;
  }

  const data = await res.json();
  setTokens(data.access, data.refresh ?? refresh);
  return data.access;
}

export async function fetchWithAuth(
  url: string,
  options: RequestInit = {},
): Promise<Response> {
  let token = getAccessToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> ?? {}),
  };

  if (token) {
    // Use X-Auth-Token to avoid conflict with HTTP Basic Auth's Authorization header
    headers['X-Auth-Token'] = `Bearer ${token}`;
  }

  let res = await fetch(url, { ...options, headers, credentials: 'include' });

  if (res.status === 401 && token) {
    const newToken = await refreshAccessToken();
    if (newToken) {
      headers['X-Auth-Token'] = `Bearer ${newToken}`;
      res = await fetch(url, { ...options, headers, credentials: 'include' });
    }
  }

  return res;
}

// Auth API
export async function login(username: string, password: string) {
  const res = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
    credentials: 'include',
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || 'Login failed');
  }
  const data = await res.json();
  setTokens(data.access, data.refresh);
  return data;
}

export async function register(fields: {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  base_currency: string;
}) {
  const res = await fetch('/api/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(fields),
    credentials: 'include',
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    const msg = Object.values(data).flat().join(' ') || 'Registration failed';
    throw new Error(msg);
  }
  const data = await res.json();
  if (data.tokens) {
    setTokens(data.tokens.access, data.tokens.refresh);
  }
  return data;
}

export async function getCurrentUser() {
  const res = await fetchWithAuth('/api/auth/me/');
  if (!res.ok) throw new Error('Not authenticated');
  return res.json();
}

// Wealth API
export async function getWealthSummary() {
  const res = await fetchWithAuth('/api/wealth/summary/');
  if (!res.ok) throw new Error('Failed to fetch summary');
  return res.json();
}

export async function getWealthHistory(days: number, granularity: 'daily' | 'monthly' = 'daily') {
  const res = await fetchWithAuth(`/api/wealth/history/?days=${days}&granularity=${granularity}`);
  if (!res.ok) throw new Error('Failed to fetch history');
  return res.json();
}

export async function getWealthBreakdown(by: string) {
  const res = await fetchWithAuth(`/api/wealth/breakdown/?by=${by}`);
  if (!res.ok) throw new Error('Failed to fetch breakdown');
  return res.json();
}

// Broker API
export async function getBrokers() {
  const res = await fetchWithAuth('/api/brokers/');
  if (!res.ok) throw new Error('Failed to fetch brokers');
  return res.json();
}

export async function discoverAccounts(brokerCode: string, credentials: Record<string, string>) {
  const res = await fetchWithAuth('/api/brokers/discover/', {
    method: 'POST',
    body: JSON.stringify({ broker_code: brokerCode, credentials }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || 'Discovery failed');
  }
  return data;
}

export async function completeDiscoveryAuth(sessionToken: string, authCode: string) {
  const res = await fetchWithAuth('/api/brokers/discover/complete-auth/', {
    method: 'POST',
    body: JSON.stringify({ session_token: sessionToken, auth_code: authCode }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || 'Authentication failed');
  }
  return data;
}

export async function createAccountsBulk(
  brokerCode: string,
  credentials: Record<string, string>,
  accounts: { identifier: string; name: string; account_type: string; currency: string; balance?: number | null; balance_date?: string }[],
) {
  const res = await fetchWithAuth('/api/accounts/bulk/', {
    method: 'POST',
    body: JSON.stringify({ broker_code: brokerCode, credentials, accounts }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || 'Failed to create accounts');
  }
  return res.json();
}

// Account API
export async function getAccounts() {
  const res = await fetchWithAuth('/api/accounts/');
  if (!res.ok) throw new Error('Failed to fetch accounts');
  return res.json();
}

export async function createAccount(fields: {
  name: string;
  broker_code: string;
  account_identifier?: string;
  account_type: string;
  currency: string;
  is_manual: boolean;
  credentials?: Record<string, string>;
}) {
  const res = await fetchWithAuth('/api/accounts/', {
    method: 'POST',
    body: JSON.stringify(fields),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    const msg = Object.values(data).flat().join(' ') || 'Failed to create account';
    throw new Error(msg);
  }
  return res.json();
}

export async function syncAccount(accountId: number) {
  const res = await fetchWithAuth(`/api/accounts/${accountId}/sync/`, {
    method: 'POST',
  });
  const data = await res.json();
  if (!res.ok && !data.status) {
    throw new Error(data.error || 'Sync failed');
  }
  return data;
}

export async function completeAccountAuth(accountId: number, authCode: string) {
  const res = await fetchWithAuth(`/api/accounts/${accountId}/auth/`, {
    method: 'POST',
    body: JSON.stringify({ auth_code: authCode }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || 'Authentication failed');
  }
  return data;
}

export async function addSnapshot(
  accountId: number,
  balance: number,
  currency: string,
  snapshotDate: string,
) {
  const res = await fetchWithAuth(`/api/accounts/${accountId}/snapshots/`, {
    method: 'POST',
    body: JSON.stringify({
      balance,
      currency,
      snapshot_date: snapshotDate,
    }),
  });
  if (!res.ok) throw new Error('Failed to add snapshot');
  return res.json();
}

export async function getSnapshots(accountId: number, page = 1) {
  const url = `/api/accounts/${accountId}/snapshots/${page > 1 ? `?page=${page}` : ''}`;
  const res = await fetchWithAuth(url);
  if (!res.ok) throw new Error('Failed to fetch snapshots');
  return res.json();
}

export async function updateSnapshot(
  snapshotId: number,
  balance: number,
  currency: string,
  snapshotDate: string,
) {
  const res = await fetchWithAuth(`/api/snapshots/${snapshotId}/`, {
    method: 'PUT',
    body: JSON.stringify({
      balance,
      currency,
      snapshot_date: snapshotDate,
    }),
  });
  if (!res.ok) throw new Error('Failed to update snapshot');
  return res.json();
}

export async function deleteSnapshot(snapshotId: number) {
  const res = await fetchWithAuth(`/api/snapshots/${snapshotId}/`, {
    method: 'DELETE',
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || 'Failed to delete snapshot');
  }
}

export async function updateAccount(accountId: number, fields: { name?: string; sync_enabled?: boolean }) {
  const res = await fetchWithAuth(`/api/accounts/${accountId}/`, {
    method: 'PATCH',
    body: JSON.stringify(fields),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || 'Failed to update account');
  }
  return res.json();
}

export async function deleteAccount(accountId: number) {
  const res = await fetchWithAuth(`/api/accounts/${accountId}/`, {
    method: 'DELETE',
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || 'Failed to delete account');
  }
}

export async function getAccountCredentials(accountId: number) {
  const res = await fetchWithAuth(`/api/accounts/${accountId}/credentials/`);
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || 'Failed to fetch credentials');
  }
  return res.json();
}

export async function updateAccountCredentials(
  accountId: number,
  credentials: Record<string, string>,
) {
  const res = await fetchWithAuth(`/api/accounts/${accountId}/credentials/`, {
    method: 'PUT',
    body: JSON.stringify({ credentials }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || 'Failed to update credentials');
  }
  return res.json();
}

export async function getBroker(brokerCode: string) {
  const res = await fetchWithAuth(`/api/brokers/${brokerCode}/`);
  if (!res.ok) throw new Error('Failed to fetch broker');
  return res.json();
}

// CSV Import
export async function importCSV(
  accountId: number,
  csvData: string,
  skipDuplicates: boolean = true,
) {
  const res = await fetchWithAuth('/api/import/csv/', {
    method: 'POST',
    body: JSON.stringify({
      account_id: accountId,
      csv_data: csvData,
      skip_duplicates: skipDuplicates,
    }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || 'Import failed');
  }
  return data;
}

// Profile API
export async function getProfile() {
  const res = await fetchWithAuth('/api/profile/');
  if (!res.ok) throw new Error('Failed to fetch profile');
  return res.json();
}

export async function updateProfile(fields: {
  base_currency?: string;
  auto_sync_enabled?: boolean;
  send_weekly_report?: boolean;
  default_chart_range?: number;
  default_chart_granularity?: 'daily' | 'monthly';
}) {
  const res = await fetchWithAuth('/api/profile/', {
    method: 'PATCH',
    body: JSON.stringify(fields),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || 'Failed to update profile');
  }
  return res.json();
}

export async function updateUser(fields: {
  first_name?: string;
  last_name?: string;
  email?: string;
}) {
  const res = await fetchWithAuth('/api/user/', {
    method: 'PATCH',
    body: JSON.stringify(fields),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || 'Failed to update user');
  }
  return res.json();
}

export async function changePassword(
  oldPassword: string,
  newPassword: string,
  newPasswordConfirm: string,
) {
  const res = await fetchWithAuth('/api/auth/change-password/', {
    method: 'POST',
    body: JSON.stringify({
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPasswordConfirm,
    }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.old_password || data.new_password_confirm || data.error || 'Failed to change password');
  }
  return data;
}
