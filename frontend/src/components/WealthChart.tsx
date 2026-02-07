import { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface HistoryPoint {
  date: string;
  total_wealth: number;
}

interface Props {
  history: HistoryPoint[];
  baseCurrency: string;
  onRangeChange: (days: number, granularity: 'daily' | 'monthly') => void;
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

export default function WealthChart({ history, baseCurrency, onRangeChange }: Props) {
  const [activeRange, setActiveRange] = useState(365);
  const [granularity, setGranularity] = useState<'daily' | 'monthly'>('daily');

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
    return `${dt.getDate()}.${dt.getMonth() + 1}`;
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
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={history} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
            <XAxis
              dataKey="date"
              tick={{ fill: 'var(--color-text-muted)', fontSize: 12 }}
              tickFormatter={formatDate}
              interval={Math.max(0, Math.floor(history.length / 10) - 1)}
            />
            <YAxis
              tick={{ fill: 'var(--color-text-muted)', fontSize: 12 }}
              tickFormatter={(v: number) => formatCurrency(v, baseCurrency)}
              width={100}
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
