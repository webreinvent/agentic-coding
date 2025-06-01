# agentic-coding
Experiments with agentic coding

# Install Python 3.10
pyenv install 3.10.13

# Install Python 3.11
pyenv install 3.11.8

# Install Python 3.12
pyenv install 3.12.2


# Set global Python version
pyenv global 3.10.13

# Set local Python version (per directory)
pyenv local 3.11.8


# If using pyenv
poetry env use $(pyenv which python3.10)


## Environment Variables

This project uses environment variables for configuration. To set up your environment:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your specific configuration values.

3. The environment variables are loaded automatically when you import the `config` module:
   ```python
   from config import config
   
   # Access configuration values
   api_key = config['api']['key']
   debug_mode = config['app']['debug']
   ```

### Available Configuration

The following environment variables can be configured:

| Variable | Description | Default |
|----------|-------------|---------|
| API_KEY | API authentication key | default_key |
| API_URL | API endpoint URL | https://api.example.com |
| DEBUG | Enable debug mode | False |
| LOG_LEVEL | Logging level | INFO |
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 5432 |
| DB_NAME | Database name | mydb |
| DB_USER | Database username | user |
| DB_PASSWORD | Database password | password |

## Usage Example

See `example.py` for a demonstration of how to use the environment variables in your code.
