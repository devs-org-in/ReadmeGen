import Link from 'next/link';

export const Navbar = () => {
  return (
    <nav className="bg-black/80 backdrop-blur-md shadow-lg rounded-lg px-8 py-3 fixed top-4 left-1/2 transform -translate-x-1/2 z-50 max-w-4xl w-full
                   transition-all duration-300 hover:shadow-[0_0_20px_5px_rgba(255,255,255,0.5)]">
      <div className="flex justify-between items-center">
        {/* Logo or Brand */}
        <Link href="/" className="text-white text-xl font-bold">
          ReadGen
        </Link>

        {/* Navigation Links */}
        <div className="flex space-x-6">
          <Link href="/" className="text-white hover:text-indigo-400 transition-colors duration-200">
            Home
          </Link>
          <Link href="/generate" className="text-white hover:text-indigo-400 transition-colors duration-200">
            Generate
          </Link>
        </div>
      </div>
    </nav>
  );
};
