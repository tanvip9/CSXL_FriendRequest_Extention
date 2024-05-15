# Friendship CSXL Team D1

- **Title:** Friendship CSXL
- **Team Members:** Arya Rao, Tanvi Pulipaka, Sarayu Yenumula, Srinidhi Ekkurthi

# Overview

Collaboration is an important aspect of software engineering, and the CSXL is a space that encourages this. The Friendship CSXL System allows students to find and work with other peers to further strengthen their communication skills. Not only does this promote collaborative efforts but also enables students to learn from one another and meet other students with a passion for technology.

# Key Personas

- **Sally Student**

  Sally Student can send Francesca Friend a friend request. Sally Student can also see whether or not her friends are in the CSXL. (All features of Sally Student also apply to Francesca Friend)

- **Francesca Friend**

  Francesca Friend can accept or deny Sally Student's friend request. Francesca Friend can also turn her Coworking status on or off to let her friends like Sally Student know if she is open to collaborating. (All features of Francesca Friend also apply to Sally Student)

- **Merritt Manager**

  Merritt Manager's goals are to be able to view who is checked into the CSXL at all times and have access to all registered users' friendships. Merritt Manager should also be able to check the Coworking status of students.

# User Stories

- **Persona 1: Sally Student**

  - As Sally Student, I want to be able to request friendship with specific peers who are registered with the CSXL, so I can connect with them on the XL platform.

  - As Sally Student, I want to see a list of my accepted friends' current coworking status if they are active and the seats they are sitting at when I view the Coworking Status, so I can easily find and join them at the XL.

- **Persona 2: Francesca Friend**

  - As Francesca Friend, I want to accept Sally Student’s friend request so that I can collaborate with Sally Student.

  - As Francesca Friend, I can turn on and off my Coworking status so I can let Sally Student know if I'm available to collaborate.

- **Persona 2: Merrit Manager**

  - As Merrit Manager, I want to be able to see a list of all students and their friendships as well as have access to remove/delete specific friends off user's accounts.

  - As Merrit Manager, I want to be able to see the Coworking status of all students so that I am aware of how many students are open to collaborating.

# Wireframes / Mockups

## Home Page

![WireFrame 1](<wireframe 1-1.png>)
<br>
This screen is the FriendshipXL home page that helps navigate you to your checked-in friends, friendship requests, and toggle your coworking status.

## Checked-In Friends and Coworking

![WireFrame 2](<WireFrame 2-1.png>)
<br>
This screen shows your friends already in the CSXL that are checked in and what friends are open to cowork.

## Pending Requests

![WireFrame 3](<WireFrame 3-1.png>)
<br>
This screen shows your pending requests and allows you to approve or deny a request.

## User Search and Friend Requests

![WireFrame 4](<WireFrame 4-1.png>)
<br>
This screen allows you to see the users registered at the CSXL and has the option for you to send a request.

# Technical Implementation

- **Code Base Dependencies:**

We would extend on the Coworking Service in frontend/src/app/coworking/coworking.service.ts and potentially the Coworking Module. This is integrated into the Friendship feature to indicate to students whether their friend is available to collaborate or not.

We would modify the Navigation component to add a new route to the Friendship feature. We would integrate and design a Friendship Component that would use the registered_user function at backend/api/authentication.py to receive the list of registered users. The registered users list is a potential list of friends that Sally Student can friend request.

We would also need to use the profile.py file to establish which user account Sally Student is sending friend requests from.

- **Frontend Components/Widgets:**

We would require a search bar component that would allow students to search for a specific registered user to friend request.

We would require a Pending Requests Widget for each incoming friend requests(look at third Wireframe screen for reference). It would include a yes button, no button, and the requesting user’s first and last name.

We would also require a Send Requests widget that includes the User’s first and last name and a send button.

- **Data Models:**

We can add an additional model in backend/models named friendship.py which includes the functions that are required for Sally Student to send, accept, and deny friend requests from potential friends like Francesca Friend.

- **API/Routes Modifications:**

We would need a GET route to get all the registered users that Sally could friend request.

We would need a POST route for when Sally Student presses the Send button so Felicia Friend can be notified that Sally Student friend requested her.

We would need a POST route for when Sally Student presses the No button so Francesca Friend can be notified her request was denied and Sally Student is not added to her list of friends.

We would need a POST route for when Sally Student presses the Yes button so Francesca Friend can be notified her request was accepted and Sally Student is added to her list of friends.

We would need a GET route to get each of Sally Student’s registered friends and categorize them into the section they are sitting in based on their seat reservation.

- **Security and Privacy:**

Only Merritt Manager should be able to view and change everyone’s data. Sally Student and Francesca Friend should not have the ability to view all students’ Coworking status and see who is checked into the CSXL. These features should only be available to Merritt Manager, as this is essential to protect the privacy of students’ data. Furthermore, when Sally Student sends a friend request to Francesca Friend, only Francesca Friend should be able to accept or deny it. Merritt Manager can then delete Francesca Friend as Sally Student’s friend if the request is accepted.
