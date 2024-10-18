import Link from 'next/link';

export default function Home() {
  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-black">
      <div className="light-beams absolute inset-0 z-0" /> {/* Light Beams background */}
      <div className="relative z-10 flex flex-col items-center">
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl mb-6 text-white">
          Welcome to the GitHub README Generator!
        </h1>
        <p className="text-lg sm:text-xl text-center text-white max-w-2xl mb-10">
          Create stunning and informative README files for your GitHub repositories using our powerful tool powered by Groq AI.
        </p>
        <Link href="/generate" passHref>
          <button className="px-6 py-3 bg-white text-indigo-600 font-semibold rounded-md shadow-lg hover:bg-indigo-100 transition-all duration-200">
            Generate README Now
          </button>
        </Link>
      </div>
    </div>
  );
}
