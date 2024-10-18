

export const generateReadme = async (repoLink) => {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/generate_readme`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ repo_link: repoLink }),
    });

    if (!response.ok) {
      throw new Error('Failed to generate README');
    }

    const data = await response.json();
    return data.readme;
  } catch (error) {
    console.error('Error generating README:', error);
    throw error;
  }
};
