# Hitting Analytics Webapp

A comprehensive baseball hitting analytics dashboard built with Streamlit.

## Features

- **Player Analysis**: View individual player statistics and performance metrics
- **Team Comparison**: Compare hitting statistics across different teams
- **Advanced Metrics**: Analyze advanced baseball analytics (WAR, wOBA, BABIP, etc.)
- **Dashboard Overview**: Quick glance at key statistics

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Project Structure

```
hitting-analytics-webapp/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── legacy/
│   └── HittingAnalytics.py  # Core analytics module
├── tests/
│   ├── test_analytics.py    # Analytics tests
│   └── test_mlb_data.py     # MLB data tests
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── Data/
│   └── README.md            # Data directory information
└── DEPLOY.md                # Deployment instructions
```

## Configuration

Streamlit settings can be modified in `.streamlit/config.toml`

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Deployment

See [DEPLOY.md](DEPLOY.md) for deployment instructions.

## License

MIT License
