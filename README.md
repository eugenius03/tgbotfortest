# Telegram shop template

### Prerequisites

- Telegram Bot API token. You can obtain it by contacting [@BotFather](https://t.me/botfather).

### Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/eugenius03/tgbotfortest.git
    cd tgbotfortest
    ```

2. Create a virtual environment:

    ```bash
    python -m venv env
    env\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Rename the `.env.copy` file to `.env` and replace `BOT_TOKEN` with your Telegram bot token, `LIQ_PUBLIC` and `LIQ_PRIVATE` with your LiqPay API keys

5. Run the bot:

    ```bash
    python main.py
    ```
