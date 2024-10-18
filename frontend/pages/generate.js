import { useState } from 'react';
import Head from 'next/head';
import { FaCopy } from 'react-icons/fa'; // Import the copy icon

export default function Generate() {
  const [repoLink, setRepoLink] = useState('');
  const [generatedReadme, setGeneratedReadme] = useState('');
  const [loading, setLoading] = useState(false); // Add loading state

  const handleGenerateReadme = async () => {
    setLoading(true); // Set loading to true when the request starts
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/generate_readme`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ repo_link: repoLink }),
    });

    const data = await res.json();
    setGeneratedReadme(data.readme);
    setLoading(false); // Set loading to false when the request ends
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(generatedReadme);
    alert('README copied to clipboard!');
  };

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-black">
      <Head>
        <title>ReadmeGen - GitHub README Generator</title>
        <meta name="description" content="Generate a README file for your GitHub repository using our powerful tool powered by Groq AI." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="light-beams absolute inset-0 z-0" /> {/* Light Beams background */}
      <div className="relative z-10 flex flex-col items-center">
        <h1 className="text-4xl font-bold text-white mb-6">Generate your README</h1>
        <input
          type="text"
          className="px-4 py-2 rounded-lg shadow-sm w-80 sm:w-96 mb-4 border border-gray-300 focus:ring focus:ring-indigo-200 text-black"
          placeholder="Enter your GitHub repository link"
          value={repoLink}
          onChange={(e) => setRepoLink(e.target.value)}
        />
        <button
          onClick={handleGenerateReadme}
          className="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-md shadow-lg hover:bg-indigo-700 transition-all duration-200 flex items-center justify-center"
          disabled={loading} // Disable button while loading
        >
          {loading ? (
            <div className="loader"></div> // Show loader when loading
          ) : (
            'Generate README'
          )}
        </button>

        {generatedReadme && (
          <div className="mt-8 bg-white shadow-lg rounded-lg p-6 max-w-4xl w-full relative">
            <h2 className="text-2xl font-bold mb-4 text-black">Generated README</h2>
            <button
              onClick={handleCopyToClipboard}
              className="absolute top-4 right-4 text-gray-600 hover:text-gray-800"
            >
              <FaCopy size={24} />
            </button>
            <pre className="whitespace-pre-wrap text-black">{generatedReadme}</pre>
          </div>
        )}
      </div>
    </div>
  );
}