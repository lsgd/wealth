import { useState, useEffect, useCallback } from 'react';
import { RefreshCw, Plus, PlusCircle, AlertCircle, CheckCircle2, Clock, X, Key, Trash2, History, Pencil, Check, XCircle, MinusCircle, Settings, Upload, Download } from 'lucide-react';
import { syncAccount, completeAccountAuth, deleteAccount, updateAccount, updateAccountCredentials, getAccountCredentials, getBroker } from '../api/client';
import AddSnapshotModal from './AddSnapshotModal';
import AddAccountModal from './AddAccountModal';
import SnapshotsModal from './SnapshotsModal';
import ImportModal from './ImportModal';
import ExportModal from './ExportModal';
import Toast from './Toast';

interface ToastData {
  id: string;
  type: 'success' | 'error';
  message: string;
}

interface Account {
  id: number;
  name: string;
  broker: { code: string; name: string };
  account_type: string;
  currency: string;
  is_manual: boolean;
  status: string;
  last_sync_at: string | null;
  last_sync_error: string;
  latest_snapshot: {
    balance: string;
    currency: string;
    balance_base_currency: string | null;
    snapshot_date: string;
  } | null;
}

interface Props {
  accounts: Account[];
  baseCurrency: string;
  onRefresh: () => void;
}

interface AuthPrompt {
  accountId: number;
  accountName: string;
  twoFaType: string;
}

function formatCurrency(value: number, currency: string): string {
  return new Intl.NumberFormat('de-CH', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

function StatusIcon({ status, isManual, onClick }: { status: string; isManual?: boolean; onClick?: () => void }) {
  if (isManual) {
    return <MinusCircle size={14} className="status-na" />;
  }
  switch (status) {
    case 'error':
      return (
        <button
          className="btn-status-error"
          onClick={onClick}
          title="Click to see error details"
        >
          <AlertCircle size={14} className="status-error" />
        </button>
      );
    case 'pending_auth':
      return <Clock size={14} className="status-pending" />;
    default:
      return <CheckCircle2 size={14} className="status-active" />;
  }
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('de-CH', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

export default function AccountsTable({ accounts, baseCurrency, onRefresh }: Props) {
  const [syncing, setSyncing] = useState<number | null>(null);
  const [deleting, setDeleting] = useState<number | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<Account | null>(null);
  const [snapshotAccount, setSnapshotAccount] = useState<Account | null>(null);
  const [snapshotsAccount, setSnapshotsAccount] = useState<Account | null>(null);
  const [showAddAccount, setShowAddAccount] = useState(false);
  const [showImport, setShowImport] = useState(false);
  const [showExport, setShowExport] = useState(false);
  const [authPrompt, setAuthPrompt] = useState<AuthPrompt | null>(null);
  const [authCode, setAuthCode] = useState('');
  const [authError, setAuthError] = useState('');
  const [submittingAuth, setSubmittingAuth] = useState(false);

  // Edit account name state
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editName, setEditName] = useState('');
  const [savingName, setSavingName] = useState(false);

  // Error details modal
  const [errorAccount, setErrorAccount] = useState<Account | null>(null);

  // Credentials editing modal
  const [credentialsAccount, setCredentialsAccount] = useState<Account | null>(null);
  const [credentialSchema, setCredentialSchema] = useState<Record<string, any> | null>(null);
  const [credentialValues, setCredentialValues] = useState<Record<string, string>>({});
  const [savingCredentials, setSavingCredentials] = useState(false);

  // Toast notifications
  const [toasts, setToasts] = useState<ToastData[]>([]);

  const addToast = useCallback((type: 'success' | 'error', message: string) => {
    const id = Date.now().toString();
    setToasts(prev => [...prev, { id, type, message }]);
  }, []);

  const dismissToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  // Close modals on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (editingId) setEditingId(null);
        if (authPrompt) setAuthPrompt(null);
        if (deleteConfirm) setDeleteConfirm(null);
        if (errorAccount) setErrorAccount(null);
        if (credentialsAccount) setCredentialsAccount(null);
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [authPrompt, deleteConfirm, editingId, errorAccount, credentialsAccount]);

  const startEditName = (account: Account) => {
    setEditingId(account.id);
    setEditName(account.name);
  };

  const cancelEditName = () => {
    setEditingId(null);
    setEditName('');
  };

  const handleSaveName = async (accountId: number) => {
    if (!editName.trim()) return;
    setSavingName(true);
    try {
      await updateAccount(accountId, { name: editName.trim() });
      setEditingId(null);
      setEditName('');
      onRefresh();
    } catch {
      // Error handling could be added here
    } finally {
      setSavingName(false);
    }
  };

  const openCredentialsModal = async (account: Account) => {
    setCredentialsAccount(account);
    setCredentialValues({});
    setCredentialSchema(null);
    try {
      // Fetch broker schema and current credentials in parallel
      const [broker, credData] = await Promise.all([
        getBroker(account.broker.code),
        getAccountCredentials(account.id),
      ]);
      setCredentialSchema(broker.credential_schema);
      // Pre-fill with current credentials (sensitive fields will be masked)
      if (credData.credentials) {
        setCredentialValues(credData.credentials);
      }
    } catch {
      setCredentialSchema(null);
    }
  };

  const handleSaveCredentials = async () => {
    if (!credentialsAccount) return;
    setSavingCredentials(true);
    try {
      await updateAccountCredentials(credentialsAccount.id, credentialValues);
      addToast('success', `Credentials updated for ${credentialsAccount.name}`);
      setCredentialsAccount(null);
      setCredentialValues({});
      onRefresh();
    } catch (err: any) {
      addToast('error', err.message || 'Failed to update credentials');
    } finally {
      setSavingCredentials(false);
    }
  };

  const handleSync = async (accountId: number) => {
    const account = accounts.find(a => a.id === accountId);
    const accountName = account?.name || 'Account';
    setSyncing(accountId);
    try {
      const result = await syncAccount(accountId);
      if (result.status === 'pending_auth') {
        // 2FA required - show modal
        setAuthPrompt({
          accountId,
          accountName,
          twoFaType: result.two_fa_type || 'totp',
        });
        setAuthCode('');
        setAuthError('');
      } else if (result.status === 'error') {
        addToast('error', `Failed to sync ${accountName}: ${result.error || 'Unknown error'}`);
        onRefresh();
      } else {
        addToast('success', `${accountName} synced successfully`);
        onRefresh();
      }
    } catch (err: any) {
      addToast('error', `Failed to sync ${accountName}: ${err.message || 'Unknown error'}`);
      onRefresh();
    } finally {
      setSyncing(null);
    }
  };

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!authPrompt || !authCode.trim()) return;

    setSubmittingAuth(true);
    setAuthError('');
    try {
      await completeAccountAuth(authPrompt.accountId, authCode.trim());
      addToast('success', `${authPrompt.accountName} synced successfully`);
      setAuthPrompt(null);
      setAuthCode('');
      onRefresh();
    } catch (err: any) {
      setAuthError(err.message || 'Authentication failed');
    } finally {
      setSubmittingAuth(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteConfirm) return;
    setDeleting(deleteConfirm.id);
    try {
      await deleteAccount(deleteConfirm.id);
      setDeleteConfirm(null);
      onRefresh();
    } catch {
      // Error handling could be added here
    } finally {
      setDeleting(null);
    }
  };

  return (
    <div className="card">
      <div className="chart-header">
        <h2>Accounts</h2>
        <div className="header-buttons">
          <button
            className="btn btn-sm btn-ghost"
            onClick={() => setShowImport(true)}
            title="Import CSV"
          >
            <Upload size={14} />
            Import
          </button>
          <button
            className="btn btn-sm btn-ghost"
            onClick={() => setShowExport(true)}
            title="Export CSV"
          >
            <Download size={14} />
            Export
          </button>
          <button
            className="btn btn-sm btn-primary"
            onClick={() => setShowAddAccount(true)}
          >
            <PlusCircle size={14} />
            Add Account
          </button>
        </div>
      </div>

      {accounts.length === 0 ? (
        <p className="table-empty">No accounts yet. Click "Add Account" to get started.</p>
      ) : (
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Broker</th>
                <th className="text-right">Balance</th>
                <th className="text-right">{baseCurrency}</th>
                <th>Last Snapshot</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {accounts.map((a) => {
                const snap = a.latest_snapshot;
                const balance = snap ? parseFloat(snap.balance) : null;
                const baseBal = snap?.balance_base_currency
                  ? parseFloat(snap.balance_base_currency)
                  : balance;
                const isEditing = editingId === a.id;
                return (
                  <tr key={a.id}>
                    <td>
                      {isEditing ? (
                        <div className="edit-name-row">
                          <input
                            type="text"
                            value={editName}
                            onChange={(e) => setEditName(e.target.value)}
                            className="edit-name-input"
                            autoFocus
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') handleSaveName(a.id);
                              if (e.key === 'Escape') cancelEditName();
                            }}
                          />
                          <button
                            className="btn btn-sm btn-ghost"
                            onClick={() => handleSaveName(a.id)}
                            disabled={savingName}
                            title="Save"
                          >
                            <Check size={14} />
                          </button>
                          <button
                            className="btn btn-sm btn-ghost"
                            onClick={cancelEditName}
                            title="Cancel"
                          >
                            <XCircle size={14} />
                          </button>
                        </div>
                      ) : (
                        <div className="name-cell">
                          <button
                            className="account-name-link"
                            onClick={() => setSnapshotsAccount(a)}
                            title="View snapshots"
                          >
                            {a.name}
                          </button>
                          <button
                            className="btn btn-sm btn-ghost btn-edit-name"
                            onClick={() => startEditName(a)}
                            title="Edit name"
                          >
                            <Pencil size={12} />
                          </button>
                        </div>
                      )}
                    </td>
                    <td>{a.broker.name}</td>
                    <td className="text-right mono">
                      {balance != null
                        ? formatCurrency(balance, snap!.currency)
                        : '—'}
                    </td>
                    <td className="text-right mono">
                      {baseBal != null
                        ? formatCurrency(baseBal, baseCurrency)
                        : '—'}
                    </td>
                    <td className="text-muted">
                      {snap ? formatDate(snap.snapshot_date) : '—'}
                    </td>
                    <td>
                      <StatusIcon
                        status={a.status}
                        isManual={a.is_manual}
                        onClick={a.status === 'error' ? () => setErrorAccount(a) : undefined}
                      />
                    </td>
                    <td>
                      <div className="action-buttons">
                        {!a.is_manual && (
                          <>
                            <button
                              className="btn btn-sm btn-ghost"
                              onClick={() => handleSync(a.id)}
                              disabled={syncing === a.id}
                              title="Sync"
                            >
                              <RefreshCw
                                size={14}
                                className={syncing === a.id ? 'spin' : ''}
                              />
                            </button>
                            <button
                              className="btn btn-sm btn-ghost"
                              onClick={() => openCredentialsModal(a)}
                              title="Edit Credentials"
                            >
                              <Settings size={14} />
                            </button>
                          </>
                        )}
                        <button
                          className="btn btn-sm btn-ghost"
                          onClick={() => setSnapshotsAccount(a)}
                          title="View Snapshots"
                        >
                          <History size={14} />
                        </button>
                        <button
                          className="btn btn-sm btn-ghost"
                          onClick={() => setSnapshotAccount(a)}
                          title="Add Snapshot"
                        >
                          <Plus size={14} />
                        </button>
                        <button
                          className="btn btn-sm btn-ghost btn-danger"
                          onClick={() => setDeleteConfirm(a)}
                          title="Delete Account"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {snapshotAccount && (
        <AddSnapshotModal
          accountId={snapshotAccount.id}
          accountName={snapshotAccount.name}
          defaultCurrency={snapshotAccount.currency}
          onClose={() => setSnapshotAccount(null)}
          onSaved={() => {
            setSnapshotAccount(null);
            onRefresh();
          }}
        />
      )}

      {showAddAccount && (
        <AddAccountModal
          onClose={() => setShowAddAccount(false)}
          onCreated={() => {
            setShowAddAccount(false);
            onRefresh();
          }}
        />
      )}

      {showImport && (
        <ImportModal
          onClose={() => setShowImport(false)}
          onImported={() => {
            onRefresh();
          }}
        />
      )}

      {showExport && (
        <ExportModal onClose={() => setShowExport(false)} />
      )}

      {/* 2FA Authentication Modal */}
      {authPrompt && (
        <div className="modal-overlay" onClick={() => setAuthPrompt(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>
                <Key size={18} style={{ marginRight: 8 }} />
                Authentication Required
              </h3>
              <button className="btn btn-ghost" onClick={() => setAuthPrompt(null)}>
                <X size={18} />
              </button>
            </div>

            {authError && <div className="form-error">{authError}</div>}

            <form onSubmit={handleAuthSubmit}>
              <p className="form-hint" style={{ marginBottom: 16 }}>
                Enter the one-time code from your authenticator app to sync{' '}
                <strong>{authPrompt.accountName}</strong>.
              </p>

              <div className="form-group">
                <label htmlFor="auth-code">
                  {authPrompt.twoFaType === 'totp' ? 'TOTP Code' : 'Authentication Code'}
                </label>
                <input
                  id="auth-code"
                  type="text"
                  inputMode="numeric"
                  autoComplete="one-time-code"
                  autoFocus
                  required
                  value={authCode}
                  onChange={(e) => setAuthCode(e.target.value)}
                  placeholder="Enter 6-digit code"
                  maxLength={6}
                />
              </div>

              <div className="form-actions">
                <button
                  type="button"
                  className="btn btn-ghost"
                  onClick={() => setAuthPrompt(null)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={submittingAuth || authCode.length < 6}
                >
                  {submittingAuth ? 'Verifying...' : 'Verify & Sync'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="modal-overlay" onClick={() => setDeleteConfirm(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>
                <Trash2 size={18} style={{ marginRight: 8 }} />
                Delete Account
              </h3>
              <button className="btn btn-ghost" onClick={() => setDeleteConfirm(null)}>
                <X size={18} />
              </button>
            </div>

            <p style={{ marginBottom: 16 }}>
              Are you sure you want to delete <strong>{deleteConfirm.name}</strong>?
              This will also delete all snapshots for this account.
            </p>

            <div className="form-actions">
              <button
                type="button"
                className="btn btn-ghost"
                onClick={() => setDeleteConfirm(null)}
              >
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-danger"
                onClick={handleDelete}
                disabled={deleting === deleteConfirm.id}
              >
                {deleting === deleteConfirm.id ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Snapshots Modal */}
      {snapshotsAccount && (
        <SnapshotsModal
          accountId={snapshotsAccount.id}
          accountName={snapshotsAccount.name}
          defaultCurrency={snapshotsAccount.currency}
          baseCurrency={baseCurrency}
          onClose={() => setSnapshotsAccount(null)}
          onChanged={() => {
            onRefresh();
          }}
        />
      )}

      {/* Error Details Modal */}
      {errorAccount && (
        <div className="modal-overlay" onClick={() => setErrorAccount(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>
                <AlertCircle size={18} style={{ marginRight: 8 }} className="status-error" />
                Sync Error
              </h3>
              <button className="btn btn-ghost" onClick={() => setErrorAccount(null)}>
                <X size={18} />
              </button>
            </div>

            <div style={{ marginBottom: 16 }}>
              <p style={{ marginBottom: 8 }}>
                Failed to sync <strong>{errorAccount.name}</strong>:
              </p>
              <div className="error-details">
                {errorAccount.last_sync_error || 'Unknown error'}
              </div>
            </div>

            <div className="form-actions">
              <button
                type="button"
                className="btn btn-ghost"
                onClick={() => setErrorAccount(null)}
              >
                Close
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => {
                  setErrorAccount(null);
                  handleSync(errorAccount.id);
                }}
              >
                <RefreshCw size={14} style={{ marginRight: 6 }} />
                Retry Sync
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Credentials Modal */}
      {credentialsAccount && (
        <div className="modal-overlay" onClick={() => setCredentialsAccount(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>
                <Settings size={18} style={{ marginRight: 8 }} />
                Update Credentials
              </h3>
              <button className="btn btn-ghost" onClick={() => setCredentialsAccount(null)}>
                <X size={18} />
              </button>
            </div>

            <p className="form-hint" style={{ marginBottom: 16 }}>
              Update credentials for <strong>{credentialsAccount.name}</strong>
            </p>

            {credentialSchema?.properties ? (
              <form onSubmit={(e) => { e.preventDefault(); handleSaveCredentials(); }}>
                {Object.entries(credentialSchema.properties).map(([key, field]: [string, any]) => (
                  <div className="form-group" key={key}>
                    <label htmlFor={`cred-${key}`}>{field.title || key}</label>
                    <input
                      id={`cred-${key}`}
                      type={field.format === 'password' ? 'password' : 'text'}
                      value={credentialValues[key] || ''}
                      onChange={(e) => setCredentialValues(prev => ({ ...prev, [key]: e.target.value }))}
                      placeholder={field.description || ''}
                    />
                    {field.description && (
                      <small className="form-hint">{field.description}</small>
                    )}
                  </div>
                ))}

                <div className="form-actions">
                  <button
                    type="button"
                    className="btn btn-ghost"
                    onClick={() => setCredentialsAccount(null)}
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={savingCredentials}
                  >
                    {savingCredentials ? 'Saving...' : 'Save Credentials'}
                  </button>
                </div>
              </form>
            ) : (
              <p className="text-muted">Loading credential fields...</p>
            )}
          </div>
        </div>
      )}

      {/* Toast notifications */}
      <Toast toasts={toasts} onDismiss={dismissToast} />
    </div>
  );
}
