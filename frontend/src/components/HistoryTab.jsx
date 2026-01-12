import React, { useState, useEffect } from 'react';
import QuizDisplay from './QuizDisplay';
import '../styles/HistoryTab.css';
import config from '../config';

function HistoryTab() {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedQuizId, setSelectedQuizId] = useState(null);
  const [selectedQuizDetails, setSelectedQuizDetails] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${config.API_BASE_URL}/history`);
      if (!response.ok) throw new Error('Failed to fetch history');
      const data = await response.json();
      setQuizzes(data.quizzes);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = async (quizId) => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/quiz/${quizId}`);
      if (!response.ok) throw new Error('Failed to fetch quiz details');
      const data = await response.json();
      setSelectedQuizDetails(data);
      setSelectedQuizId(quizId);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCloseModal = () => {
    setSelectedQuizId(null);
    setSelectedQuizDetails(null);
  };

  if (loading) {
    return <div className="history-tab"><p>⏳ Loading quiz history...</p></div>;
  }

  return (
    <div className="history-tab">
      {error && <div className="error-message">❌ {error}</div>}

      {quizzes.length === 0 ? (
        <div className="empty-state">
          <p>📚 No quizzes generated yet</p>
          <p>Go to the "Generate Quiz" tab to create your first quiz!</p>
        </div>
      ) : (
        <div className="quizzes-table-container">
          <table className="quizzes-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Title</th>
                <th>Preview</th>
                <th>Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {quizzes.map((quiz, index) => (
                <tr key={quiz.id}>
                  <td>{index + 1}</td>
                  <td className="title-cell">{quiz.title}</td>
                  <td className="preview-cell">{quiz.article_preview.substring(0, 100)}...</td>
                  <td className="date-cell">
                    {new Date(quiz.created_at).toLocaleDateString()}
                  </td>
                  <td>
                    <button
                      className="details-button"
                      onClick={() => handleViewDetails(quiz.id)}
                    >
                      👁️ View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Modal for quiz details */}
      {selectedQuizDetails && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close-button" onClick={handleCloseModal}>✕</button>
            <QuizDisplay
              title={selectedQuizDetails.title}
              preview={selectedQuizDetails.article_preview}
              quizData={selectedQuizDetails.quiz_data}
              relatedTopics={selectedQuizDetails.related_topics}
              url={selectedQuizDetails.url}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default HistoryTab;
