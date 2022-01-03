# Blog

Site with articles on all topics

## Installation

1. Download project from github;
2. Go to directory `blog` in cmd;
3. For creating database run following commands: 
   - `python manage.py makemigrations` 
   - `python manage.py migrate`
4. To create an admin - `python manage.py createsuperuser`;
5. Run server - `python manage.py runserver`;
6. In your browser go to "http://127.0.0.1:8000" (this is the main page of site).

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

Thanks for your attention!
