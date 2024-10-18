import '../styles/globals.css'; // This is where your global CSS should be imported
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';

function MyApp({ Component, pageProps }) {
  return (
    <div className="relative min-h-screen flex flex-col bg-black text-white">
      {/* Light Beams Background */}
      <div className="light-beams absolute inset-0 z-0" />

      {/* Content */}
      <div className="relative z-10 flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow">
          <Component {...pageProps} />
        </main>
        <Footer />
      </div>
    </div>
  );
}

export default MyApp;
