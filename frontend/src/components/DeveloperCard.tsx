import { Card, Metric, Text, Title, Flex } from '@tremor/react'
import type { DeveloperMetric } from '../data/mockData'

interface Props {
  developer: DeveloperMetric
}

export function DeveloperCard({ developer }: Props) {
  return (
    <Card decoration="top" decorationColor="indigo">
      <Flex justifyContent="between" alignItems="center">
        <Title>{developer.name}</Title>
        <Text>{developer.developerId}</Text>
      </Flex>
      <Flex justifyContent="start" className="mt-4 gap-6">
        <div>
          <Text>Commits</Text>
          <Metric>{developer.commits}</Metric>
        </div>
        <div>
          <Text>PRs</Text>
          <Metric>{developer.prs}</Metric>
        </div>
        <div>
          <Text>IDE Hours</Text>
          <Metric>{developer.ideHours.toFixed(1)}</Metric>
        </div>
        <div>
          <Text>Flow Score</Text>
          <Metric>{developer.flowScore}</Metric>
        </div>
      </Flex>
    </Card>
  )
}
