import { Card, Title, Text } from '@tremor/react'
import { DeveloperCard } from './DeveloperCard'
import { ActivityChart } from './ActivityChart'
import { TeamMetrics } from './TeamMetrics'
import { mockDevelopers, mockTimeSeries } from '../data/mockData'

export function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-50 p-6 dark:bg-slate-900">
      <div className="mx-auto max-w-7xl space-y-6">
        <div>
          <Title>CogniStream Developer Flow Analytics</Title>
          <Text>Real-time insights into team productivity and flow state</Text>
        </div>

        <TeamMetrics />

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <ActivityChart data={mockTimeSeries} />
          <Card>
            <Title>Top Contributors</Title>
            <Text>Developers ranked by flow score</Text>
            <div className="mt-4 space-y-4">
              {mockDevelopers
                .slice()
                .sort((a, b) => b.flowScore - a.flowScore)
                .map((dev) => (
                  <DeveloperCard key={dev.developerId} developer={dev} />
                ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
