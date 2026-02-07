import { Wallet } from 'lucide-react';

interface Props {
  totalWealth: number;
  baseCurrency: string;
  accountCount: number;
}

function formatCurrency(value: number, currency: string): string {
  return new Intl.NumberFormat('de-CH', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

export default function WealthSummaryCard({
  totalWealth,
  baseCurrency,
  accountCount,
}: Props) {
  return (
    <div className="card summary-card">
      <div className="summary-icon">
        <Wallet size={32} />
      </div>
      <div className="summary-content">
        <p className="summary-label">Total Wealth</p>
        <p className="summary-value">{formatCurrency(totalWealth, baseCurrency)}</p>
        <p className="summary-meta">
          {accountCount} account{accountCount !== 1 ? 's' : ''}
        </p>
      </div>
    </div>
  );
}
