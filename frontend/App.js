import React, { useState } from 'react';
import './App.css';
import { toBeRequired } from '@testing-library/jest-dom/matchers';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [useRag, setUseRag] = useState(true);
  const [fineTune, setFineTune] = useState(true); // Default value is true


  const handleQuestionChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleAskQuestion = async () => {
    try {
      const response = await fetch('/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
  
        body: JSON.stringify({ question, useRag, fineTune }), // Include useRag, fineTune in the request body
      });

      if (!response.ok) {
        throw new Error('Failed to get a response from the server.');
      }

      const data = await response.json();
      setAnswer(data.answer);
    } catch (error) {
      console.error('An error occurred:', error);
      setAnswer('An error occurred while fetching the answer.');
    }
  };
  
  const handleDropdownChange = (event) => {
    const newValue = event.target.value === 'true';
    setUseRag(newValue);
  };

  const handleFineTuneChange = (event) => {
    const newValue = event.target.value === 'true';
    setFineTune(newValue);
  };

  
  return (
  <div className="App">
    <div style={{backgroundColor: "maroon"}}>

    <img src="./tree.jpg" className="App-logo" alt="logo" />

      <h1>Welcome to the Stanford Credit Union Chatbot!</h1>
      <div className="flex-container">
        <div className="input-container">
          <input
            type="text"
            placeholder="How do I become a member of Stanford FCU?"
            value={question}
            onChange={handleQuestionChange}
            size="60" 
            rows="4"
          />
          <button onClick={handleAskQuestion}>Ask Question</button>
          <textarea
            rows="10"
            cols="50"
            readOnly
            value={answer}
            placeholder="Answer will appear here"
          />
          <label htmlFor="useRagDropdown">Use RAG?</label>
          <select
            id="useRagDropdown"
            value={useRag.toString()}
            onChange={handleDropdownChange}
          >
            <option value="true">True</option>
            <option value="false">False</option>
          </select>
          <br />
          <label htmlFor="fineTuneDropdown">Use fine-tuned model?</label>
          <select
            id="fineTuneDropdown"
            value={fineTune.toString()}
            onChange={handleFineTuneChange}
          >
            <option value="true">True</option>
            <option value="false">False</option>
          </select>
          <br />
        </div>
      </div>
    </div>
  </div>
  );
}

export default App;


