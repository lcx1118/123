import '../styles/globals.css'; // 确保路径与你的 globals.css 文件路径匹配

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}

export default MyApp;
