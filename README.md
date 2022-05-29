# Blog

Site with articles on all topics

## Installation

1. Clone project from GitHub;
2. Go to directory `blog` in cmd;
3. Build project:
   - `docker-compose up --build`
4. Go into container:
   - `docker exec -it <Container Name> bash`
5. For creating migrations run following command: 
   - `python manage.py makemigrations`
6. To create an admin - `python manage.py createsuperuser`;
7. Run server - `python manage.py runserver`;
8. In your browser go to "http://127.0.0.1:8000" (this is the main page of site).

## Site management

- At "http://127.0.0.1:8000/admin" located the admin page
- For creating a profile of user go to "Profiles" on the left side of the screen
- For creating a tag (category) for posts go to "Tags"
- For creating a post (article) go to "Posts" 
- For manage users rights you can go to "Users" and "Groups"

## Usage

- On the main page of the site you can see all posts that exist
- On the right part of screen, you can choose a certain tag (category) of posts (articles)
- You can also login or sing-up from the main page
- If you go to your profile page, you will be able to change profile settings and write articles (if your have status "author")
