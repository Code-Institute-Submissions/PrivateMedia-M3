# **Private Media** 
<img src="https://imgur.com/kmriMUr.jpg" style="margin: 0;">

Private Media is personal social space to share anything and everything with yourself. It provides a unique private media experience for users who still want to go online, express their thoughts and unburden their minds without ever having to worry about anyone snooping.
<a href="http://private-madia-m3.herokuapp.com/" target="_blank">click to visit Private Media.</a>
## User Experience

The user experience is quite intuitive and familiar for users who currently owns any social media account as well as for new users. The Ux consist of the following:
<ul>
<li>Registration Page</li>
<li>Login Page</li>
<li>Reset Password Page</li>
<li>Home/Profile Page</li>
<li>Edit Profile Page</li>
<li>Other user actions include: Create Post, edit, delete post and delete profile</li>
<ul>

*User stories include:*
<ul>
<li>As a user i will like to have a registration page to create an account</li>
<li>As a user i will like to be able to login using my username and passwoord</li>
<li>As a user i will like to be able to reset my password securely using using my username and security question.</li>
<li>As a user i will like to be able to logout of the application from home page</li>
<li>As a user i will like like to see my hobbies displayed left of the home page</li>
<li>As a user i will like to see my upcoming events displayed top right of the home page.</li>
<li>As a user i will like to see my profile info such as username, address and date of birth displayed top left of the home page</li>
<li>As a user i will like to be able to create a new post from my home page</li>
<li>As a user i will like to be able to delete an existing post.</li>
<li>As a user i will like to be able to edit a post.</li>
<li>As a user i will like to be able to update my profile when logged in.</li>
<li>As a user i will like to be able to delete my account from edit profile page</li>
<li>As a user, i will like to get a prompt asking me to confirm if i wanted to delete my account before proceeding to delete.</li>
<li>As a user i will like to have flash messages when i perform an action that is server related.</li>
</ul>

## **Mocks**
### Web and Mobile
**As a basic layout <a href="/Frames/ux-Mocks/" target="_blank">here is a link </a> to the web wireFrame and Mock up used in creating Private Media.**

## **Data Modelling**
### Entity Relationship Diagram
**As a basic layout <a href="/Frames/wireFrames-Architecture/" target="_blank">here is a link </a> to the entity relationship diagram used in creating Private Media.**

## **Features**
### Existing Features
<li>Create Account</li>
<li>Edit Profile</li>
<li>Delete Account</li>
<li>Create Post</li>
<li>Edit Post</li>
<li>Delete Post</li>
<li>Secure Password Reset</li>
<li>Displays User Information and Posts</li>
<li>Flash Messages</li>
</ul>

### Features Left to Implement
<ul>
<li>Upload Profile Images</li>
<li>Incremental Page Load</li>
</ul>

## **Technologies used**
<ul>
<li>HTML5</li>
<li>CSS3</li>
<li>Javascript: The Project uses javascript to make the application interactive as well as to define busines logic</li>
<li>JQuery: The project uses JQuery to simplify DOM manipulation.</li>
<li>W3school: W3school was used as the major templating for the application index page and logon.</li>
<li>Heroku: The Project uses Heroku for deployment</li>
<li>Flask</li>
<li>Python: An app.py file was created to aid deployment to heroku and render html template</li> 

</ul>

## **Testing**
<hr>
Testing on Private Media Website was carried out **manually** and by <a href="https://github.com/MichaelOsarumwense/e2e-Private-Media.git" target="_blank">Atutomated Testing</a> using **Cypress**. The test approach was to test every user story individually by creating 
user journies and scenarios required to navigate through the entire site. While testing, a few bugs were found and fixed and these are are all listed below. **Devtool** and **light house** was also used to debug and test the application.

<a href="https://github.com/MichaelOsarumwense/e2e-Private-Media.git" target="_blank">Here is the link to the test automation repo used for this project.</a>

### **Cases**
<ul>
<h3>Scenarios/Cases</h3>
<li>Register/Create Account: Navigate to Url, click on register,  fill in details and click get started, profile should be succesfully created with a success flash message. Required fields are Username, password and secret fields, a user will be unable to create an account if these three fields are not completed.</li>
<li>Login: 
<ul>
<li>Given that the user naviagtes to private media using a Url (http://private-madia-m3.herokuapp.com/)</li>
<li>When the user enters a valid username</li>
<li>And the user enters a valid password</li>
<li>Then the user should be logged into profile page with a success message</li>
<li>Given that the user enters incorrect combination of username and Passwords</li>
<li>When the user clicks on login</li>
<li>Then the user should get an error message saying incorrect details</li>
</ul> 
</li>
<li>Create a post: 
<ol>
<li>Given user is logged into private media</li>
<li>When user enters post content is the text box</li>
<li>Then the user should be able to create a new post by clicking Post and get a success flash message</li>
</ol>
</li>
<li>Delete Post: When user clicks on delete on a given post, the post should be deleted and user gets a success message</li>
<li>Edit Post: When user clicks on edit on a given post, and user updates post content and click save, post is edited and user is navigated back to home page with a success message.</li>
<li>Edit Profile: When user clicks on edit profile from home page, and user updates profile content and click update, profile is updated and user is navigated back to home page with a success message and user can verify the update content.</li>
<li>Logout: When user clicks on logout from home page then user should be navigated to login page</li>
<li>Responsiveness: UX is responsive on small and medium devices like mobile phones and tablets.</li>
<li>Delete Account: 
<ul>
<li>Given user is on home page</li>
<li>When user clicks on edit profile</li>
<li>And user clicks on delete Account</li>
<li>When user confirms delete, then the user should be logged out and account deleted</li>
</ul>
</li>
<li>Reset Password: On login page, when user clicks on reset password, user is only able to reset password if they enter matching username and secret word.</li>
<li>Mobile Resolutions:
<ol>
<li>In a mobile resolution upcoming events is not displayed.</li>
</ol>
</li>
</ul>
<hr>

### **Bugs**
<ul>
<li>Fixed a bug where update profile page was not rendering referenced static files like css styles and Js.</li>
<li>fixed a bug where logo onclick was resulting in url not found on login</li>
<li>Fixed a bug where new users upon regisration gets an error because of wrong username reference</li>
<li>Fixed a bug where password could be left blank when updating user profile details due to password input field missing the required remark</li>
<li>Fixed a bug where new post were not being displayed due to user reference tempering (bug caught by automation test after latest code change.</li>
<li>Fixed a bug where newly created users were being put into a seesion and logged into the application (caught by the test automation tests).</li>
<li>fixed a bug where deleting user account or profile broke the app because it wasn't deleting the user session</li>
</ul>

## **Deployment**
Private Media is deployed to Heroku and hosted on Heroku. The deployed branch is the master branch and can be found below: 
<ul>
<li>Deployed git Branch: <a href="https://github.com/MichaelOsarumwense/PrivateMedia-M3.git">Github Repo</a> </li>
<li>To run the code locally, clone the repo with the above link, open project with gitpod and in the terminal run the following command: <strong><em>python3 app.py</strong></em></li>
</ul>


## **Credit**
### **Content**
<ul>
<li>The user forms and media template was gotten from W3schools.com</li>
</ul>

### **Media**
<ul>
<li>The photos used in this site were obtained from https://pixabay.com/images/search/avatar/ and W3schools.com</li>
</ul>

### **Acknowledgements**
<ul>
<li>I received inspiration for this project from my introverted personality type and need.</li>
<li>Many thanks to my mentor Guido Cecilio Garcia Bernal for his guidiance.</li>
</ul>

--------

Michael Osarumwense.
