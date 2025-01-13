# <span style="color:#333333">Git</span><span style="color:#ffcc00">Speak</span>

Welcome to **<span style="color:#333333">Git</span><span style="color:#ffcc00">Speak</span>**, a portfolio project designed as a platform to make it easier for developers to share their learning journeys on social media platforms such as LinkedIn and Twitter. It enables users to create and publish written posts highlighting their achievements, lessons learned, and challenges overcome. The primary objectives are to help developers enhance their professional growth, secure new opportunities, improve their skills, and build meaningful connections within the tech community.

---

## Features

- **User Profiles:** Tailored for developers to showcase their skills, job goals, and technical expertise.
- **Job Goals Selection:** Users can choose multiple short-term career objectives for personalized interactions.
- **Responsive Design:** Enjoy a sleek and responsive interface across devices.
- **User Authentication**: Secure login and registration functionality.
- **Create and Manage Posts**: Write, edit, and delete posts about your learning journey.
- **Social Media Sharing**: Share posts directly to LinkedIn and Twitter.
- **Responsive Design**: User-friendly experience across devices.
- **Database Integration**: Stores user profiles and posts in a PostgreSQL database.

---

## Getting Started

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.10+
- PostgreSQL
- Flask
- SQLAlchemy
- Psycopg2

-----


## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML and CSS
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy


---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gitspeak.git
   ```
2. Navigate to the project directory:
   ```bash
   cd gitspeak
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up the database:
   - Ensure PostgreSQL is installed and running.
   - Create a database for the app.
   - Update the `SQLALCHEMY_DATABASE_URI` in your configuration file with your database details.
   
6. Run the application:
   ```bash
   flask run
   ```

7. Access the app at `http://127.0.0.1:5000/`.

## Usage

1. Register or log in to your account.
2. Create and customize your profile.
3. Write posts to share your learning journey.
4. Share your posts on LinkedIn and Twitter to connect with the tech community.


## Contributing

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-branch
   ```
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For support or inquiries, please contact:
- **Author:** Daniel Berthran
- **Email:** berthran146@example.com
- **Location:** Nigeria


---

## Acknowledgements

- **Flask**: For providing a lightweight and flexible web framework.
- **SQLAlchemy**: For simplifying database operations.
- **PostgreSQL**: For robust and reliable database management.
- **Community Contributors**: Thanks to everyone who has contributed to this project!

---

**GitSpeak**: "Your Journey, Your Code, Your Voice."


