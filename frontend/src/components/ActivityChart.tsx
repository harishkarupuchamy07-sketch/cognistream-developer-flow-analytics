import { Card, Text, Title } from '@tremor/react'
import type { TimeSeriesPoint } from '../data/mockData'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

interface Props {
  data: TimeSeriesPoint[]
}

export function ActivityChart({ data }: Props) {
  return (
    <Card>
      <Title>Activity Over Time</Title>
      <Text>Commits and IDE hours across the sprint</Text>
      <div className="h-72 mt-4">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorCommits" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorIDE" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="commits"
              stroke="#6366f1"
              fillOpacity={1}
              fill="url(#colorCommits)"
            />
            <Area
              type="monotone"
              dataKey="ideHours"
              stroke="#10b981"
              fillOpacity={1}
              fill="url(#colorIDE)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  )
}
