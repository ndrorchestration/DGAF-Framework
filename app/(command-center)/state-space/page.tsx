import type { Metadata } from 'next'
import { StateSpaceView } from '../../components/state-space-view'

export const metadata: Metadata = {
  title: 'State Space — DGAF',
  description: 'DGAF discrete reachability and state-space projection.',
}

export default function StateSpacePage() {
  return <StateSpaceView />
}
