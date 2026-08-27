import { Card, Metric, Text, Grid } from '@tremor/react'
import { teamTotals } from '../data/mockData'

export function TeamMetrics() {
  const metrics = [
    { label: 'Total Commits', value: teamTotals.totalCommits.toString() },
    { label: 'Total PRs', value: teamTotals.totalPRs.toString() },
    { label: 'Total Reviews', value: teamTotals.totalReviews.toString() },
    { label: 'IDE Hours', value: teamTotals.totalIDEHours.toFixed(1) },
    { label: 'Messages', value: teamTotals.totalMessages.toString() },
    { label: 'Avg Flow Score', value: teamTotals.avgFlowScore.toFixed(1) },
  ]

  return (
    <Grid numItems={1} numItemsSm={2} numItemsLg={3} className="gap-4">
      {metrics.map((m) => (
        <Card key={m.label}>
          <Text>{m.label}</Text>
          <Metric>{m.value}</Metric>
        </Card>
      ))}
    </Grid>
  )
}
