import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/utils/formatters.dart';
import '../../data/models/wealth_summary.dart';
import '../providers/core_providers.dart';
import '../providers/wealth_provider.dart';

class WealthLineChart extends ConsumerWidget {
  final List<WealthHistoryPoint> history;
  final String currency;

  const WealthLineChart({
    super.key,
    required this.history,
    required this.currency,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final chartRange = ref.watch(chartRangeProvider);
    final chartGranularity = ref.watch(chartGranularityProvider);
    final dateFormat = ref.watch(dateFormatProvider);

    if (history.isEmpty) {
      return Card(
        child: SizedBox(
          height: 250,
          child: Center(
            child: Text(
              'No data available',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ),
        ),
      );
    }

    final spots = history.asMap().entries.map((entry) {
      return FlSpot(
        entry.key.toDouble(),
        entry.value.totalWealth,
      );
    }).toList();

    final minY = spots.map((s) => s.y).reduce((a, b) => a < b ? a : b);
    final maxY = spots.map((s) => s.y).reduce((a, b) => a > b ? a : b);
    final range = maxY - minY;
    final padding = range > 0 ? range * 0.1 : maxY * 0.1;
    final gridInterval = range > 0 ? range / 4 : maxY / 4;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Period selector
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: [
                _RangeChip(
                  label: '30d',
                  selected: chartRange == 30,
                  onTap: () =>
                      ref.read(chartRangeProvider.notifier).state = 30,
                ),
                _RangeChip(
                  label: '90d',
                  selected: chartRange == 90,
                  onTap: () =>
                      ref.read(chartRangeProvider.notifier).state = 90,
                ),
                _RangeChip(
                  label: '6m',
                  selected: chartRange == 180,
                  onTap: () =>
                      ref.read(chartRangeProvider.notifier).state = 180,
                ),
                _RangeChip(
                  label: '1y',
                  selected: chartRange == 365,
                  onTap: () =>
                      ref.read(chartRangeProvider.notifier).state = 365,
                ),
                _RangeChip(
                  label: '2y',
                  selected: chartRange == 730,
                  onTap: () =>
                      ref.read(chartRangeProvider.notifier).state = 730,
                ),
                _RangeChip(
                  label: 'All',
                  selected: chartRange == 3650,
                  onTap: () =>
                      ref.read(chartRangeProvider.notifier).state = 3650,
                ),
              ],
            ),
            const SizedBox(height: 8),
            // Granularity selector
            SegmentedButton<String>(
              segments: const [
                ButtonSegment(value: 'daily', label: Text('Daily')),
                ButtonSegment(value: 'monthly', label: Text('Monthly')),
              ],
              selected: {chartGranularity},
              onSelectionChanged: (selected) {
                ref.read(chartGranularityProvider.notifier).state =
                    selected.first;
              },
              showSelectedIcon: false,
              style: ButtonStyle(
                visualDensity: VisualDensity.compact,
                tapTargetSize: MaterialTapTargetSize.shrinkWrap,
              ),
            ),
            const SizedBox(height: 16),
            // Chart
            SizedBox(
              height: 200,
              child: LineChart(
                LineChartData(
                  gridData: FlGridData(
                    show: true,
                    drawVerticalLine: false,
                    horizontalInterval: gridInterval,
                    getDrawingHorizontalLine: (value) => FlLine(
                      color: Theme.of(context)
                          .colorScheme
                          .outlineVariant
                          .withValues(alpha: 0.5),
                      strokeWidth: 1,
                    ),
                  ),
                  titlesData: FlTitlesData(
                    topTitles: const AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    rightTitles: const AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 24,
                        interval: (spots.length / 4).ceilToDouble(),
                        getTitlesWidget: (value, meta) {
                          final index = value.toInt();
                          if (index < 0 || index >= history.length) {
                            return const SizedBox.shrink();
                          }
                          // Skip first and last to avoid edge cutoff
                          if (index == 0 || index == history.length - 1) {
                            return const SizedBox.shrink();
                          }
                          final date = history[index].dateTime;
                          // Use day.month.year format for daily, month+year for monthly
                          final dateFormat = chartGranularity == 'daily'
                              ? DateFormat('d.M.yy')
                              : DateFormat('MMM yy');
                          return Padding(
                            padding: const EdgeInsets.only(top: 4),
                            child: Text(
                              dateFormat.format(date),
                              style: Theme.of(context)
                                  .textTheme
                                  .labelSmall
                                  ?.copyWith(
                                    color: Theme.of(context)
                                        .colorScheme
                                        .onSurfaceVariant,
                                  ),
                            ),
                          );
                        },
                      ),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 45,
                        interval: gridInterval,
                        getTitlesWidget: (value, meta) {
                          // Skip edge values to avoid overlap
                          if (value == meta.min || value == meta.max) {
                            return const SizedBox.shrink();
                          }
                          return Text(
                            formatChartAxisValue(value),
                            style:
                                Theme.of(context).textTheme.labelSmall?.copyWith(
                                      color: Theme.of(context)
                                          .colorScheme
                                          .onSurfaceVariant,
                                    ),
                          );
                        },
                      ),
                    ),
                  ),
                  borderData: FlBorderData(show: false),
                  minY: minY - padding,
                  maxY: maxY + padding,
                  lineBarsData: [
                    LineChartBarData(
                      spots: spots,
                      isCurved: true,
                      curveSmoothness: 0.2,
                      color: Theme.of(context).colorScheme.primary,
                      barWidth: 2,
                      isStrokeCapRound: true,
                      dotData: const FlDotData(show: false),
                      belowBarData: BarAreaData(
                        show: true,
                        color: Theme.of(context)
                            .colorScheme
                            .primary
                            .withValues(alpha: 0.1),
                      ),
                    ),
                  ],
                  lineTouchData: LineTouchData(
                    touchTooltipData: LineTouchTooltipData(
                      maxContentWidth: 180,
                      fitInsideHorizontally: true,
                      fitInsideVertically: true,
                      getTooltipColor: (touchedSpot) =>
                          Theme.of(context).colorScheme.surfaceContainerHighest,
                      getTooltipItems: (touchedSpots) {
                        return touchedSpots.map((spot) {
                          final index = spot.x.toInt();
                          if (index < 0 || index >= history.length) return null;
                          final point = history[index];
                          return LineTooltipItem(
                            '${formatDate(point.dateTime, dateFormat)}\n${formatCurrency(point.totalWealth, currency)}',
                            TextStyle(
                              color: Theme.of(context).colorScheme.onSurface,
                              fontWeight: FontWeight.w500,
                            ),
                          );
                        }).toList();
                      },
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _RangeChip extends StatelessWidget {
  final String label;
  final bool selected;
  final VoidCallback onTap;

  const _RangeChip({
    required this.label,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return FilterChip(
      label: Text(label),
      selected: selected,
      onSelected: (_) => onTap(),
      showCheckmark: false,
      visualDensity: VisualDensity.compact,
      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
      padding: EdgeInsets.zero,
      labelPadding: const EdgeInsets.symmetric(horizontal: 8),
    );
  }
}
