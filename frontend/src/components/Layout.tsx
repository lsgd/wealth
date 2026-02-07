import { Link } from 'react-router-dom';
import { LogOut, Settings, TrendingUp } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function Layout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();

  return (
    <div className="app-layout">
      <header className="app-header">
        <Link to="/" className="app-logo">
          <TrendingUp size={24} />
          <span>Wealth Tracker</span>
        </Link>
        {user && (
          <div className="header-right">
            <span className="header-user">{user.username}</span>
            <Link to="/settings" className="btn btn-ghost" title="Settings">
              <Settings size={18} />
            </Link>
            <button onClick={logout} className="btn btn-ghost" title="Logout">
              <LogOut size={18} />
            </button>
          </div>
        )}
      </header>
      <main className="app-main">{children}</main>
    </div>
  );
}
