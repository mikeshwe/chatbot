const express = require('express');
const { exec } = require('child_process');
const cors = require('cors'); // Import the cors package

const app = express();
const port = 4000;

app.use(express.json());
app.use(cors()); // Use CORS middleware to allow cross-origin requests
    
app.post('/ask', (req, res) => {
  const question = req.body.question;
  const useRag = req.body.useRag; // Get the useRag value from the request body
  const fineTune = req.body.fineTune;

  console.log(`Received a question: "${question}"`);
  console.log(`value of useRag:  "${useRag}"`);
  console.log(`value of fineTune:  "${fineTune}"`);

  let command = `python /Users/mshwe/rlhf/rag.py --query="${question}"`;

  if (useRag) {
    command += ' --rag';
  }

  if (fineTune) {
    command += ' --fine_tune';
  }
  
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error}`);
      res.status(500).send('An error occurred.');
      return;
    }

    const response = stdout.trim();
    console.log(`Python script response: "${response}"`);
    res.json({ answer: response });
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});