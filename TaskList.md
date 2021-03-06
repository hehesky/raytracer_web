# Task List

Deadline: 2017-11-30 (demo)


## Back End Dev (Flask)
- [x] Logic for index page
- [x] Logic for user log-in and session management 
	- [x] password salting
	- [x] Login library
	- [x] Integrate with front end
- [x] Parsing render request (from user) [required data interface to be determined]
  - [x] Parse Sphere object info (center, radius, color, reflectivity)
  - [ ] ~~Parse Camera info~~ [cancelled]
  - [x] Parse Light Source info
  - [x] Parse Triangle
  - [x] Parse other type of objects
  - [x] Unit test
- [x] Render 3D image (pyrt)
  - [x] Scene and Camera
  - [x] Rendering Sphere
  - [x] Rendering Triangle
  - [x] Rendering other objects
  - [x] Unit test
  - [x] Create a separate Lambda function for rending  
- [x] Fetching results

## Front End Dev (html,css,js,etc.)
- [ ] Finalize css style
- [x] Index page
- [x] Login page (and form)
  - [x] Bare-bone page
  - [x] Login failed message
- [x] User dashboard page (displaying fetched results)
  - [x] Bare-bone dashboard
  - [x] Polish
   - [x] Logout button
   - [x] Generate image button
   - [x] See public images button
- [x] Public image page
  - [x] show image owner
- [x] Request page & request form (include pre-processing logic in js)
  - [x] allow adding/removing objects (that will be rendered) in the form
  - [x] provide different type of inputs for different type of objects
  - [x] set public or private
## DynamoDb
- [x] Set up new table
- [x] Query table for information (with boto3)
- [x] Store/update information (with boto3)
- [x] Get public requests
- [x] Integrate into Back End [status: integrated with login library]

## S3
- [x] Set up new bucket
- [X] Upload file to S3 (with boto3) [status: base library done]
- [x] Integrate with Renderer
- [x] Integrate into Back End

## Local Test
- [ ] Test on localhost

## Zappa (deploy)
- [x] Understand how to deploy using zappa
- [x] Check if Zappa can handle multiprocessing [status: Zappa cannot have background process if the http request has a shorter life span]

- [ ] ~~Check if Zappa can handle "local" files~~ [status: Cancelled. Handling file with in-memeory buffer]
- [ ] Deploy to AWS
- [ ] Test deployed app
