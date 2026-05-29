// pages/_app.jsx — global style reset
import '../dashboard/styles/global.css';
export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />;
}
