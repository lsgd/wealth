import { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

function useIsMobile(breakpoint = 480) {
  const [isMobile, setIsMobile] = useState(
    typeof window !== 'undefined' ? window.innerWidth <= breakpoint : false
  );

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth <= breakpoint);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [breakpoint]);

  return isMobile;
}

interface HistoryPoint {
  date: string;
  total_wealth: number;
}

interface Props {
  history: HistoryPoint[];
  baseCurrency: string;
  onRangeChange: (days: number, granularity: 'daily' | 'monthly') => void;
  defaultRange?: number;
  defaultGranularity?: 'daily' | 'monthly';
}

const RANGES = [
  { label: '30d', days: 30 },
  { label: '90d', days: 90 },
  { label: '6m', days: 180 },
  { label: '1y', days: 365 },
  { label: '2y', days: 730 },
  { label: 'All', days: 3650 },
];

function formatCurrency(value: number, currency: string): string {
  return new Intl.NumberFormat('de-CH', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

function formatCurrencyCompact(value: number): string {
  if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(1)}M`;
  }
  if (value >= 1_000) {
    return `${Math.round(value / 1_000)}k`;
  }
  return value.toString();
}

export default function WealthChart({ history, baseCurrency, onRangeChange, defaultRange = 365, defaultGranularity = 'daily' }: Props) {
  const [activeRange, setActiveRange] = useState(defaultRange);
  const [granularity, setGranularity] = useState<'daily' | 'monthly'>(defaultGranularity);
  const isMobile = useIsMobile();

  const handleRange = (days: number) => {
    setActiveRange(days);
    onRangeChange(days, granularity);
  };

  const handleGranularity = (g: 'daily' | 'monthly') => {
    setGranularity(g);
    onRangeChange(activeRange, g);
  };

  const formatDate = (d: string) => {
    const dt = new Date(d);
    if (granularity === 'monthly') {
      return dt.toLocaleDateString('de-CH', { month: 'short', year: '2-digit' });
    }
    // Show year for daily view as well
    const year = dt.getFullYear().toString().slice(-2);
    return `${dt.getDate()}.${dt.getMonth() + 1}.${year}`;
  };


  return (
    <div className="card chart-card">
      <div className="chart-header">
        <h2>Wealth Over Time</h2>
        <div className="chart-controls">
          <div className="granularity-buttons">
            <button
              className={`btn btn-sm ${granularity === 'daily' ? 'btn-primary' : 'btn-ghost'}`}
              onClick={() => handleGranularity('daily')}
            >
              Daily
            </button>
            <button
              className={`btn btn-sm ${granularity === 'monthly' ? 'btn-primary' : 'btn-ghost'}`}
              onClick={() => handleGranularity('monthly')}
            >
              Monthly
            </button>
          </div>
          <div className="range-buttons">
            {RANGES.map((r) => (
              <button
                key={r.days}
                className={`btn btn-sm ${activeRange === r.days ? 'btn-primary' : 'btn-ghost'}`}
                onClick={() => handleRange(r.days)}
              >
                {r.label}
              </button>
            ))}
          </div>
        </div>
      </div>
      {history.length === 0 ? (
        <div className="chart-empty">
          <p>No data yet. Add accounts and snapshots to see your wealth over time.</p>
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={isMobile ? 280 : 350}>
          <LineChart data={history} margin={{ top: 5, right: 28, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
            <XAxis
              dataKey="date"
              tick={{ fill: 'var(--color-text-muted)', fontSize: isMobile ? 9 : 11 }}
              tickFormatter={formatDate}
              interval={Math.max(0, Math.floor(history.length / (isMobile ? 4 : 6)) - 1)}
              angle={isMobile ? -45 : 0}
              textAnchor={isMobile ? 'end' : 'middle'}
              height={isMobile ? 45 : 30}
              dy={isMobile ? 5 : 0}
              padding={{ left: 0, right: 0 }}
            />
            <YAxis
              tick={{ fill: 'var(--color-text-muted)', fontSize: isMobile ? 9 : 11 }}
              tickFormatter={formatCurrencyCompact}
              width={isMobile ? 32 : 45}
            />
            <Tooltip
              contentStyle={{
                background: 'var(--color-card)',
                border: '1px solid var(--color-border)',
                borderRadius: '8px',
              }}
              formatter={(value) => [
                formatCurrency(Number(value) || 0, baseCurrency),
                'Total Wealth',
              ]}
              labelFormatter={(label) =>
                new Date(String(label)).toLocaleDateString('de-CH', {
                  year: 'numeric',
                  month: 'long',
                  day: granularity === 'daily' ? 'numeric' : undefined,
                })
              }
            />
            <Line
              type="monotone"
              dataKey="total_wealth"
              stroke="var(--color-primary)"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 5, fill: 'var(--color-primary)' }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
