export const Footer = () => {
  return (
    <footer className="bg-black/80 backdrop-blur-md shadow-lg px-8 py-4 w-full text-center text-white fixed bottom-0 left-0 z-50">
      <p className="text-sm">
        © 2023 - {new Date().getFullYear()} ReadGen. All rights reserved.
      </p>
    </footer>
  );
};
