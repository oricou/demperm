# demperm
Démocratie permanente - Democratic Participation Platform

## Database Setup

This Django project includes a comprehensive database schema for democratic participation:

### Models

- **Citizen**: Extended user model for democratic participation with verification status
- **Category**: Categories for organizing proposals (Environment, Economy, Social, etc.)
- **Proposal**: Proposals that citizens can vote on with status tracking
- **Vote**: Individual votes on proposals (Yes/No/Abstain)
- **Comment**: Discussion system for proposals with threading support
- **Poll**: Quick polls for gathering citizen opinions
- **PollOption**: Options for polls
- **PollVote**: Votes on poll options

### Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the admin interface at http://127.0.0.1:8000/admin/

### Database Features

- User authentication and verification system
- Proposal creation and voting mechanism
- Discussion threads with comments
- Poll system for quick opinion gathering
- Administrative interface for content management
- Democratic process tracking and status management
