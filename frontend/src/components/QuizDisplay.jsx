import React, { useState } from 'react';
import '../styles/QuizDisplay.css';

function QuizDisplay({ title, preview, quizData, relatedTopics, url }) {
  const [userAnswers, setUserAnswers] = useState({});
  const [showAnswers, setShowAnswers] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleAnswerSelect = (questionIndex, option) => {
    setUserAnswers({
      ...userAnswers,
      [questionIndex]: option,
    });
  };

  const handleSubmitQuiz = () => {
    setSubmitted(true);
    setShowAnswers(true);
  };

  const calculateScore = () => {
    if (!quizData.questions) return 0;
    let correct = 0;
    quizData.questions.forEach((question, index) => {
      if (userAnswers[index] === question.answer) {
        correct++;
      }
    });
    return correct;
  };

  const score = calculateScore();
  const totalQuestions = quizData.questions?.length || 0;

  return (
    <div className="quiz-display">
      <div className="quiz-header">
        <h2>{title}</h2>
        <a href={url} target="_blank" rel="noopener noreferrer" className="source-link">
          🔗 View Original Article
        </a>
      </div>

      <div className="article-preview-section">
        <h3>📄 Article Preview</h3>
        <p>{preview}</p>
      </div>

      {relatedTopics && relatedTopics.length > 0 && (
        <div className="related-topics-section">
          <h3>🏷️ Related Topics</h3>
          <div className="topics-list">
            {relatedTopics.map((topic, index) => (
              <span key={index} className="topic-badge">
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}

      {submitted && (
        <div className="score-section">
          <h3>📊 Your Score</h3>
          <div className="score-display">
            <span className="score-number">{score}/{totalQuestions}</span>
            <span className="score-percentage">
              {Math.round((score / totalQuestions) * 100)}%
            </span>
          </div>
        </div>
      )}

      <div className="quiz-questions-section">
        <h3>❓ Quiz Questions ({totalQuestions})</h3>

        {quizData.questions && quizData.questions.map((question, questionIndex) => (
          <div key={questionIndex} className="question-card">
            <div className="question-header">
              <h4>Question {questionIndex + 1}</h4>
              <span className={`difficulty-badge difficulty-${question.difficulty}`}>
                {question.difficulty}
              </span>
            </div>

            <p className="question-text">{question.question}</p>

            <div className="options-container">
              {question.options.map((option, optionIndex) => {
                const isSelected = userAnswers[questionIndex] === option;
                const isCorrect = option === question.answer;
                const showCorrect = showAnswers && isCorrect;
                const showIncorrect = showAnswers && isSelected && !isCorrect;

                return (
                  <label
                    key={optionIndex}
                    className={`option-label ${isSelected ? 'selected' : ''} ${
                      showCorrect ? 'correct' : ''
                    } ${showIncorrect ? 'incorrect' : ''}`}
                  >
                    <input
                      type="radio"
                      name={`question-${questionIndex}`}
                      value={option}
                      checked={isSelected}
                      onChange={() => handleAnswerSelect(questionIndex, option)}
                      disabled={submitted}
                    />
                    <span className="option-text">{option}</span>
                    {showCorrect && <span className="correct-indicator">✓</span>}
                    {showIncorrect && <span className="incorrect-indicator">✗</span>}
                  </label>
                );
              })}
            </div>

            {showAnswers && (
              <div className="explanation-box">
                <p>
                  <strong>Explanation:</strong> {question.explanation}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>

      {!submitted ? (
        <button className="submit-button" onClick={handleSubmitQuiz}>
          📤 Submit Quiz
        </button>
      ) : (
        <button className="reset-button" onClick={() => window.location.reload()}>
          🔄 Try Again
        </button>
      )}
    </div>
  );
}

export default QuizDisplay;
