# NYTimes Article Loader
This application fetches and flattens articles from The New York Times API in batches.
Will continue to fetch until articles run out and will sleep for 60 seconds between rate limits.

[input.json](input.json) and [output.json](output.json) are provided as examples of the input and output formats respectively.

## Prerequisites
Ensure you have Python 3.12 installed on your system. This application has been tested with Python 3.12.

## Configuration
Before running the application: 
1. obtain an API key from The New York Times Developer Network and 
2. Set your desired query

set them in the config dict under the main function as shown below:
```python
if __name__ == "__main__":
    config = {
        "api_key": "YOUR_API_KEY",
        "query": "Silicon Valley",
    }
    ...
```

## Getting Started

### if you have GNU Make & Poetry (checkout [Makefile](Makefile))

```bash
# Install dependencies
make init-poetry

# Run the application
make run
```

### If you only have Poetry:
```bash
# Install dependencies
poetry install

# Run the application
poetry run python main.py
```

### If you have niether or none of the above worked, use virtualenv or whatever you use to manage virtual environments
```bash
#using virtualenv

# Install dependencies
virtualenv -p 3.12 env
source venv/bin/activate
pip install -r requirements.txt

# Run the application
python main.py
```