import type { SVGProps } from 'react'

type IconProps = SVGProps<SVGSVGElement>

function IconBase({ children, ...props }: IconProps & { children: React.ReactNode }) {
  return <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...props}>{children}</svg>
}

export const OverviewIcon = (props: IconProps) => <IconBase {...props}><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></IconBase>
export const ActivityIcon = (props: IconProps) => <IconBase {...props}><path d="M3 12h4l2.2-5 4.2 10 2.2-5H21"/></IconBase>
export const ShieldIcon = (props: IconProps) => <IconBase {...props}><path d="M12 3 20 6v5c0 5-3.4 8.4-8 10-4.6-1.6-8-5-8-10V6l8-3Z"/><path d="m9 12 2 2 4-4"/></IconBase>
export const NodesIcon = (props: IconProps) => <IconBase {...props}><circle cx="6" cy="7" r="2.5"/><circle cx="18" cy="7" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="m8 8.5 2.7 7M16 8.5l-2.7 7M8.5 7h7"/></IconBase>
export const EvidenceIcon = (props: IconProps) => <IconBase {...props}><path d="M5 3h10l4 4v14H5z"/><path d="M15 3v5h4M8 12h8M8 16h6"/></IconBase>
export const ToolsIcon = (props: IconProps) => <IconBase {...props}><path d="M14.5 6.5a4 4 0 0 0-5 5L4 17l3 3 5.5-5.5a4 4 0 0 0 5-5l-2.5 2.5-3-3 2.5-2.5Z"/></IconBase>
export const MenuIcon = (props: IconProps) => <IconBase {...props}><path d="M4 7h16M4 12h16M4 17h16"/></IconBase>
export const RefreshIcon = (props: IconProps) => <IconBase {...props}><path d="M20 7v5h-5M4 17v-5h5"/><path d="M6.1 9A7 7 0 0 1 18 6l2 1M17.9 15A7 7 0 0 1 6 18l-2-1"/></IconBase>
export const ArrowIcon = (props: IconProps) => <IconBase {...props}><path d="M5 12h14M14 7l5 5-5 5"/></IconBase>
