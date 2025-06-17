# Finfily

This simple Flask application allows users to manage a portfolio of assets. Users can add, remove, and update assets and see profit/loss information.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

The server will start on port 5000.

### Endpoints
- `POST /add` – Add an asset (`name`, `quantity`, `buy_price`)
- `POST /update` – Update current price (`name`, `current_price`)
- `POST /remove` – Remove an asset (`name`)
- `GET /portfolio` – View portfolio with profit/loss
