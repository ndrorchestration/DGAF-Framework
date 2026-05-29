// pages/_app.tsx — global app shell
import type { AppProps } from 'next/app'
import '../dashboard/styles/global.css'

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
