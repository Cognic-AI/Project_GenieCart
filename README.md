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
GEMINI_API_KEY_1=your_gemini_api_key_1
GEMINI_API_KEY_2=your_gemini_api_key_2
GEMINI_API_KEY_3=your_gemini_api_key_3
GEMINI_API_KEY_4=your_gemini_api_key_4
TAVILY_API_KEY=your_tavily_api_key
LLAMA_API_KEY=your_llama_api_key
OPENAI_API_KEY=your_openai_api_key
USER_AGENT=your_user_agent_string
DB_credentials=your_db_credentials(run the db dump in the root to create a local database)
SMTP server credentials=your_smtp_server_credentials(for sending emails)
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
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" >> .env
   echo "GEMINI_API_KEY_1=your_api_key_here" >> .env
   echo "GEMINI_API_KEY_2=your_api_key_here" >> .env
   echo "GEMINI_API_KEY_3=your_api_key_here" >> .env
   echo "GEMINI_API_KEY_4=your_api_key_here" >> .env
   echo "TAVILY_API_KEY=your_api_key_here" >> .env
   echo "LLAMA_API_KEY=your_api_key_here" >> .env
   echo "OPENAI_API_KEY=your_api_key_here" >> .env
   echo "USER_AGENT=your_web_browser_user_agent_here" >> .env
   echo "PRODUCT_CSV=product.csv" >> .env
   echo "DB_HOST=your_db_host_here" >> .env
   echo "DB_USER=your_db_user_here" >> .env
   echo "DB_PASSWORD=your_db_password_here" >> .env
   echo "DB_NAME=your_db_name_here" >> .env
   echo "DB_PORT=your_db_port_here" >> .env
   echo "SMTP_USER=your_smtp_user_here" >> .env
   echo "SMTP_PASSWORD=your_smtp_password_here" >> .env
   echo "SMTP_SERVER_HOST=your_smtp_server_here" >> .env
   ```

## Usage

### Running the Endpoint manually
```bash
python "Machine_Customer_Endpoint.py"
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
- **Google Gemini** (AI integration)
- **Tavily API** (Web search)
- **LLAMA 3.1 from Nvidia** (AI integration)
- **OpenAI ChatGPT 4o mini** (AI integration)
- **Machine Learning** (Recommendation system)
- **MySQL** (Database)
- **SMTP** (Email server)

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For inquiries, visit [Cognic AI](https://github.com/Cognic-AI) or email teamcognic.ai@gmail.com.
