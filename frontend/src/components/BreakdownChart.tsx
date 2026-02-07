import { useState, useRef, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

interface BreakdownItem {
  category: string;
  amount: number;
  percentage: number;
}

interface Props {
  breakdown: BreakdownItem[];
  baseCurrency: string;
  onGroupChange: (by: string) => void;
}

const COLORS = [
  '#4f8cff', '#34d399', '#fbbf24', '#f87171',
  '#a78bfa', '#fb923c', '#38bdf8', '#e879f9',
];

const GROUPS = [
  { label: 'Broker', value: 'broker' },
  { label: 'Currency', value: 'currency' },
  { label: 'Type', value: 'account_type' },
];

function formatCurrency(value: number, currency: string): string {
  return new Intl.NumberFormat('de-CH', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

export default function BreakdownChart({ breakdown, baseCurrency, onGroupChange }: Props) {
  const [activeGroup, setActiveGroup] = useState('broker');
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  const legendRefs = useRef<(HTMLDivElement | null)[]>([]);

  // Reset refs array when breakdown changes
  useEffect(() => {
    legendRefs.current = legendRefs.current.slice(0, breakdown.length);
  }, [breakdown]);

  // Scroll legend item into view when hovering pie chart segments
  useEffect(() => {
    if (hoveredIndex !== null && legendRefs.current[hoveredIndex]) {
      legendRefs.current[hoveredIndex]?.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
      });
    }
  }, [hoveredIndex]);

  const handleGroup = (by: string) => {
    setActiveGroup(by);
    onGroupChange(by);
  };

  return (
    <div className="card">
      <div className="chart-header">
        <h2>Breakdown</h2>
        <div className="range-buttons">
          {GROUPS.map((g) => (
            <button
              key={g.value}
              className={`btn btn-sm ${activeGroup === g.value ? 'btn-primary' : 'btn-ghost'}`}
              onClick={() => handleGroup(g.value)}
            >
              {g.label}
            </button>
          ))}
        </div>
      </div>
      {breakdown.length === 0 ? (
        <div className="chart-empty">
          <p>No data to display.</p>
        </div>
      ) : (
        <div className="breakdown-content">
          <div className="breakdown-chart">
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={breakdown}
                  dataKey="amount"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={85}
                  paddingAngle={2}
                  onMouseLeave={() => setHoveredIndex(null)}
                >
                  {breakdown.map((_entry, index) => (
                    <Cell
                      key={index}
                      fill={COLORS[index % COLORS.length]}
                      opacity={hoveredIndex === null || hoveredIndex === index ? 1 : 0.4}
                      style={{ cursor: 'pointer' }}
                      onMouseEnter={() => setHoveredIndex(index)}
                    />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="breakdown-legend">
            {breakdown.map((item, index) => (
              <div
                key={item.category}
                ref={(el) => { legendRefs.current[index] = el; }}
                className={`breakdown-legend-item ${hoveredIndex === index ? 'highlighted' : ''} ${hoveredIndex !== null && hoveredIndex !== index ? 'dimmed' : ''}`}
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              >
                <span
                  className="breakdown-legend-color"
                  style={{ backgroundColor: COLORS[index % COLORS.length] }}
                />
                <span className="breakdown-legend-label">{item.category}</span>
                <span className="breakdown-legend-value">
                  {formatCurrency(item.amount, baseCurrency)}
                </span>
                <span className="breakdown-legend-pct">{item.percentage.toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
