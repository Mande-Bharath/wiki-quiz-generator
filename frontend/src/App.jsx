import React, { useState } from 'react';
import './App.css';
import GenerateQuizTab from './components/GenerateQuizTab';
import HistoryTab from './components/HistoryTab';

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <div className="app">
      <header className="app-header">
        <h1>📚 Wiki Quiz Generator</h1>
        <p>Generate quizzes from Wikipedia articles using AI</p>
      </header>

      <nav className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'generate' ? 'active' : ''}`}
          onClick={() => setActiveTab('generate')}
        >
          🎯 Generate Quiz
        </button>
        <button
          className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          📖 Past Quizzes
        </button>
      </nav>

      <main className="tab-content">
        {activeTab === 'generate' && <GenerateQuizTab />}
        {activeTab === 'history' && <HistoryTab />}
      </main>

      <footer className="app-footer">
        <p>© 2026 Wiki Quiz Generator | Powered by Gemini AI</p>
      </footer>
    </div>
  );
}

export default App;
