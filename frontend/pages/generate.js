import { useState } from 'react';
  // Make sure your light-beams CSS is in globals.css

export default function Generate() {
  const [repoLink, setRepoLink] = useState('');
  const [generatedReadme, setGeneratedReadme] = useState('');

  const handleGenerateReadme = async () => {
    const res = await fetch('http://localhost:8000/generate_readme', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ repo_link: repoLink }),
    });

    const data = await res.json();
    setGeneratedReadme(data.readme);
  };

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-black">
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
          className="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-md shadow-lg hover:bg-indigo-700 transition-all duration-200"
        >
          Generate README
        </button>

        {generatedReadme && (
          <div className="mt-8 bg-white shadow-lg rounded-lg p-6 max-w-4xl w-full">
            <h2 className="text-2xl font-bold mb-4 text-black">Generated README</h2>
            <pre className="whitespace-pre-wrap text-black">{generatedReadme}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
