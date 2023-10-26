# NexCrow

Welcome to NexCrow, a social networking platform that allows users to share their thoughts, memories, and interact with a vibrant community. Inspired by the dynamics of social connectivity, NexCrow provides a space for individuals to express themselves, connect with others, and explore a world of content.

Table of Contents

- [Installation](#installation)
- [Setup](#Setup)
- [Usage](#usage)
- [Features](#Features)
- [Technologies Used](#Technologies)
- [Contributing](#contributing)
- [Contact](#contact)

## Installation

To get started with NexCrow, ensure you have Python, pip, and a virtual environment manager like virtualenv or conda installed.

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/NexCrow.git
   cd NexCrow

   ```

2. Create and activate a virtual environment: (bash)

   ```bash
   virtualenv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`

   ```

3. nstall the required packages:
   ```python
   pip install -r requirements.txt
   ```

- Setup

1. Set up the configuration in config.py, ensure to configure the database URI and other environment variables.
2. Run database migrations:

flask db upgrade

3. Start the application:
   flask run

4. Visit http://127.0.0.1:5000/ in your web browser.

## Usage

. Home Page: View posts from followed users, and create new posts.
. Profile Page: View and edit your user profile.
. Search: Search for other users.
. Alerts and Notifications: Stay up to date with interactions on your posts.

## Features

. User authentication and profiles.
. Posting text and images.
. Liking posts and comments.
. Commenting on posts.
. Following and unfollowing users.
. Real-time alerts and notifications.

## Technologies Used

. ackend: Flask, SQLAlchemy
. Frontend: HTML, CSS, JavaScript
. Database: PostgreSQL
. Deployment: [Add Deployment Platform]

## Contributing

Contributions to NexCrow are welcome! Please ensure you follow the Contributing Guidelines.

## Contact

For any inquiries or issues, please contact
Ali Jafarbeglou - zilogfa@live.com
