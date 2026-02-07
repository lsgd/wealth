interface HistoryPoint {
  date: string;
  total_wealth: number;
}

interface Props {
  history: HistoryPoint[];
  baseCurrency: string;
}

function formatCurrency(value: number, currency: string): string {
  return new Intl.NumberFormat('de-CH', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

function formatPercent(value: number): string {
  const sign = value >= 0 ? '+' : '';
  return `${sign}${value.toFixed(1)}%`;
}

function getChangeForDays(history: HistoryPoint[], days: number): { absolute: number; percent: number } | null {
  if (history.length < 2) return null;

  const sorted = [...history].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  const latest = sorted[0];

  // Find entry closest to N days ago
  const targetDate = new Date();
  targetDate.setDate(targetDate.getDate() - days);

  let closest = sorted[sorted.length - 1];
  for (const point of sorted) {
    const pointDate = new Date(point.date);
    if (pointDate <= targetDate) {
      closest = point;
      break;
    }
  }

  if (closest === latest) return null;

  const absolute = latest.total_wealth - closest.total_wealth;
  const percent = closest.total_wealth !== 0
    ? ((latest.total_wealth - closest.total_wealth) / closest.total_wealth) * 100
    : 0;

  return { absolute, percent };
}

export default function RecentChanges({ history, baseCurrency }: Props) {
  const periods = [
    { label: '7 Days', days: 7 },
    { label: '30 Days', days: 30 },
    { label: '90 Days', days: 90 },
    { label: '1 Year', days: 365 },
  ];

  const changes = periods.map(p => ({
    ...p,
    change: getChangeForDays(history, p.days),
  }));

  const hasAnyData = changes.some(c => c.change !== null);

  return (
    <div className="card">
      <div className="chart-header">
        <h2>Recent Changes</h2>
      </div>
      {!hasAnyData ? (
        <div className="chart-empty">
          <p>Not enough history to show changes.</p>
        </div>
      ) : (
        <div className="recent-changes-grid">
          {changes.map(({ label, change }) => (
            <div key={label} className="recent-change-item">
              <span className="recent-change-label">{label}</span>
              {change ? (
                <>
                  <span className={`recent-change-percent ${change.absolute >= 0 ? 'positive' : 'negative'}`}>
                    {formatPercent(change.percent)}
                  </span>
                  <span className={`recent-change-absolute ${change.absolute >= 0 ? 'positive' : 'negative'}`}>
                    {change.absolute >= 0 ? '+' : ''}{formatCurrency(change.absolute, baseCurrency)}
                  </span>
                </>
              ) : (
                <span className="recent-change-na">—</span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
