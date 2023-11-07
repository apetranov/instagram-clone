# Instagram Clone
#### Video Demo:  <https://www.youtube.com/watch?v=fkOSPRHyO3M&ab_channel=AlexanderPetranov>
#### Description:
My Final Project for CS50x is a simple Instagram Clone, which has been an incredible learning experience. This project allows users to register, create posts with images by adding a text content for each post, and specifying an image URL for each image. I've combined various technologies for the front-end and back-end, aiming to replicate the essence of Instagram while also ensuring that it's a user-friendly project, despite being my first actual project.

On the front-end, I've used HTML, CSS, a bit of JavaScript, and Tailwind CSS for design. HTML forms the structure of the project, defining the layout and content of web pages. CSS is crucial for enhancing the visual appeal and Tailwind CSS, with its utility-first approach, simplifies the design process, enabling me to create an attractive and intuitive user interface. My choice to emulate Instagram's sleek design was challenging, but it pushed me to learn new skills and strive for excellence.

The back-end of my Instagram Clone is powered by Flask, a micro web framework for Python, and SQLite. Flask's simplicity and flexibility make it a great choice for web applications, and SQLite efficiently handles data storage and retrieval. These technologies work together to ensure the smooth functioning of core features, such as user registration, post creation, and image storage.

One of the significant accomplishments of this project is the implementation of a user authentication system. Creating a fully functioning user authentication system involves securely managing user data, enabling registration and login processes, and ensuring proper session management. I'm proud to have successfully implemented this system, as it's a crucial aspect of web development and adds real-world functionality to the project.

As I continue to work on this project, my goal is to enhance the user experience further. I'm considering adding features like the ability to like and comment on posts, user profiles, and the option to follow other users. Exploring the integration of cloud storage for images is also on the horizon, as it would make the application more scalable.

In summary, my Instagram Clone project for CS50x is a reflection of my growth as a web developer. It showcases my ability to create an appealing front-end, implement robust back-end functionality, and secure user data through authentication. This project has transformed my theoretical knowledge into practical skills, and I'm excited to see how it evolves as I continue to expand its features and capabilities. CS50x has been a remarkable journey, and this project is a testament to the progress I've made in the field of web development. I look forward to taking on more ambitious projects in the future and continuing to push my boundaries.

Here is what each file is used for:

app.py: this is where all the backend logic is including all the
routes for the Flask application, all the manipulations in the routes
with the SQLite database and so on

create_post.html: here is the logic for creating a post

forgotten_password.html: in this file is the logic for a user to create a new password if they have forgotten their old one

home.html: this is the home page of the site

layout.html: this is the layout for the site which all other pages are based on

messages.html: what "logic" there is for implementing the messaging feature

no_such_user.html: this shows up when you try to change your password
but you type in the wrong username

password_error: this shows up when the passwords don't match

profile.html: this is the current users profile page with all their posts

register.html: this is the register form page

user_error.html: this is the page which shows up when you type and invalid username and/or password on login

user_not_found.html: this page shows up when the user typed in the search bar is not found (not implemented yet)

user_profile.html: this is the page which shows up when you click on another users profile

username_unavailable.html: this shows up when you try to register with a username which is already in use

instagram.db: the database file with all the tables

tailwind.config.js: needed for the tailwind css to work

user_module.py: the file needed for user registration and login

README.md: this file with all the documentation

requirments.txt: the needed python packages to run the application