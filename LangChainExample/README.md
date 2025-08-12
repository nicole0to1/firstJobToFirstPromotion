# AI Kindergarten Teacher

An interactive AI-powered kindergarten teacher application built with LangChain and Ollama, featuring the GEMMA3 language model. This project demonstrates how to create a conversational AI system that can act as an educational assistant for young children.

## Features

- **Interactive Chat Interface**: Engage in conversations with an AI kindergarten teacher
- **Educational Responses**: Get age-appropriate answers to children's questions
- **Lesson Planning**: AI can create lesson plans for various topics
- **Local Model Support**: Runs entirely on your local machine using Ollama
- **LangChain Integration**: Built with modern LangChain patterns and best practices

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Ollama** installed and running locally
3. **GEMMA3 model** downloaded and available

## Installation

### 1. Install Ollama

Visit [ollama.ai](https://ollama.ai) and follow the installation instructions for your operating system.

### 2. Download GEMMA3 Model

After installing Ollama, download the GEMMA3 model:

```bash
ollama pull gemma3
```

### 3. Verify Installation

Test that the model is working correctly:

```bash
ollama run gemma3
```

### 4. Install Python Dependencies

Install the required Python packages:

```bash
pip install langchain langchain-ollama
```

## Usage

### Running the Application

Start the AI Kindergarten Teacher:

```bash
python3 AiKindergartenTeacher.py
```

### How It Works

1. The application starts with a greeting message and an initial lesson plan request
2. You can ask questions as if you're a kindergarten student
3. The AI teacher responds with age-appropriate explanations
4. Type 'exit' or 'quit' to close the application

### Example Interaction

```
Welcome to the Ai Kindergarten! Type 'exit' or 'quit' to leave.
...
Teacher: [AI generates a lesson plan for today's topic]

You: Why is the sky blue?
Teacher: [AI explains in simple terms suitable for kindergarten students]

You: How do plants grow?
Teacher: [AI provides an educational response with encouragement to learn more]
```

## Project Structure

- `AiKindergartenTeacher.py` - Main application file containing the AI teacher logic
- `README.md` - This documentation file

## Technical Details

- **Framework**: LangChain for AI application development
- **Model**: GEMMA3 via Ollama for local inference
- **Architecture**: Uses LangChain's ChatPromptTemplate and message schemas
- **Model Validation**: Includes model validation on initialization

## Customization

You can modify the system prompts in the code to:
- Change the teacher's personality or teaching style
- Adjust the complexity of responses
- Add new conversation patterns
- Modify the lesson planning functionality

## Troubleshooting

- **Model not found**: Ensure GEMMA3 is downloaded with `ollama pull gemma3`
- **Ollama not running**: Start Ollama service before running the application
- **Import errors**: Verify all Python dependencies are installed correctly

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is open source and available under the MIT License.
