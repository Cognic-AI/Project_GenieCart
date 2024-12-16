# Project GenieCart

**Project GenieCart** is an AI-driven e-commerce tool designed to streamline product data management and categorization. It leverages advanced machine learning models and AI agents to automate data analysis, filtering, and organization.

## Key Features

- **AI Integration**: Utilizes cutting-edge AI models for product filtering and analysis.
- **Automated Data Conversion**: Converts JSON product data into structured CSV formats.
- **E-commerce Optimization**: Enhances the accuracy and efficiency of product categorization.
- **Frontend and Backend Support**: Modular structure for extensibility and scalability.

## Secrets Configuration

To fully utilize GenieCart, the following secrets need to be configured in the `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
LLAMA_API_KEY=your_llama_api_key
OPENAI_API_KEY=your_openai_api_key
USER_AGENT=your_user_agent_string
```

## Project Structure

```
Project_GenieCart/
├── AI_Agents/               # AI-driven components for decision-making and filtering
├── Final_products/          # JSON data files for products
├── ML-model/                # Machine learning models and scripts
├── frontend/                # Frontend code for user interaction
├── machine_platform_user_profile/ # User profile management
├── products.csv             # Consolidated product data in CSV format
├── .gitignore               # Git ignore file
└── README.md                # Project documentation
```

## Prerequisites

- **Python 3.8+**
- **Node.js** (for frontend functionality)
- **API Keys** as listed in the Secrets Configuration section

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Cognic-AI/Project_GenieCart.git
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the secrets in `.env`:

## Usage

### Running the AI Model
To filter product data and generate a CSV file:
```bash
python "AI Agents/Conversable Agent.py"
```

### Frontend Development
Navigate to the `frontend` directory and start the development server:
```bash
cd frontend
npm install
npm run dev
```

## Technologies Used

- **Python** (Backend)
- **TypeScript** (Frontend)
- **Google Gemini AI** (AI integration)
- **Tavily API** (Web search)
- **Llama API from Nvidia** (AI integration)
- **OpenAI API** (AI integration)
- **Machine Learning** (Recommendation system)

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For inquiries, visit [Cognic AI](https://github.com/Cognic-AI) or email teamcognic.ai@gmail.com.
