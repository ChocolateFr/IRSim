# IRC Robot Telegram Bot



### Overview



 This is a Telegram bot that simulates an IRC (Internet Relay Chat) environment,

 allowing users to join channels, send messages, and manage admins and banned users.

 Built using the `pyrogram` library, it stores configuration and state in a JSON

 file managed by the [WatchDict](https://pypi.org/project/watchdict/) class, ensuring that changes are tracked and saved automatically.



 ## Features



 - **Channel Management**: Admins can create, delete, and manage channels.

 - **User Management**: Admins can promote/demote users, ban/unban them, and view

   user statistics.

 - **Nickname Support**: Users can set their nicknames, which are displayed with

   their messages.

 - **Message Handling**: Users can send messages and replies within channels.

 - **Backup Configuration**: Admins can download the current configuration.



 Prerequisites



 - Python 3.7 or higher

 - Git (optional, for cloning the repository)



 Installation



 1. Clone the repository (if applicable):

    ```bash

    git clone https://github.com/ChocolateFr/IRSim.git

    cd IRSim

    ```



 2. Install the required packages and set up configuration:

    ```bash

    python installer.py

    ```



    The `installer.py` script will:

    - Install required Python packages listed in `requirements.txt`.

    - Prompt you for your Telegram API credentials (`api_id`, `api_hash`,

      and `api_token`) if they are not already in `conf.json`.

    - Allow you to add admin user IDs.



    After completing the setup, you can run the bot using:

    ```bash

    python app.py

    ```



## Manual configuration (without installer.py)



 The `conf.json` file should look like this:



 ```json

 {

     "api_id": "YOUR_API_ID",

     "api_hash": "YOUR_API_HASH",

     "api_token": "YOUR_BOT_TOKEN",

     "admins": [YOUR_ADMIN_IDS],

     "banned": [],

     "channels": ["channel1", "channel2"],

     "nicknames": {}

 }

 ```



 Replace `YOUR_API_ID`, `YOUR_API_HASH`, and `YOUR_BOT_TOKEN` with your actual

 Telegram API credentials. Add the admin user IDs in the `admins` array.



 Usage



 1. **Start the Bot**: Run the bot script.

    ```bash

    python app.py

    ```



 2. **Basic Commands**:

    - `/start`: Welcome message.

    - `/join channel_name`: Join a specific channel.

    - `/channels`: List available channels.

    - `/nick your_nickname`: Set your nickname.
    - `/me`: Shows your nickname and where you are?
    - `/users`: Show users in current channel.

    - Admin commands (start with `/`):

      - `/status`: Check the bot status.

      - `/ban user_nickname`: Ban a user.

      - `/unban user_nickname`: Unban a user.

      - `/backup`: Download the configuration file.

      - `/stop`: Stops bot from answering to others.



 ## Development



 - Adding New Features



    To add new features, modify the bot's command handlers in the script. You can extend functionality by adding new commands or enhancing existing ones.



 ## Logging



 The bot logs activity using Python's logging framework. You can adjust the log level as needed.



## Contributing



 Feel free to submit issues or pull requests to enhance the functionality of the

 bot or fix bugs.



## License



 This project is licensed under the MIT License.


