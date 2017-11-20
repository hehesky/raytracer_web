# Task List

Deadline: 2017-11-30 (demo)

## Design Decisions
- Data interface [HIGH PRIORITY]
- Type of 3D objects allowed [HIGH PRIORITY]
- Limit of requested 3D objects to render

## Back End Dev (Flask)
- [ ] Logic for index page
- [ ] Logic for user log-in and session management 
	- [x] password salting
	- [x] Login library
	- [ ] Integrate with front end
- [ ] Parsing render request (from user) [required data interface to be determined]
  - [x] Parse Sphere object info (center, radius, color, reflectivity)
  - [ ] ~~Parse Camera info~~ [cancelled]
  - [ ] Parse Light Source info
  - [x] Parse Triangle
  - [ ] Parse other type of objects
  - [ ] Unit test
- [ ] Render 3D image (pyrt)
  - [x] Scene and Camera
  - [x] Rendering Sphere
  - [ ] Rendering Triangle
  - [ ] Rendering other objects
  - [ ] Unit test
  - [ ] Create a separate Lambda function for rending  
- [ ] Fetching results

## Front End Dev (html,css,js,etc.)
- [ ] Index page
- [ ] Login page (and form)
  - [ ] Bare-bone page
- [ ] User dashboard page (displaying fetched results)
  - [ ] Bare-bone dashboard
- [ ] Request page & request form (include pre-processing logic in js)
  - [ ] allow adding/removing objects (that will be rendered) in the form
  - [ ] provide different type of inputs for different type of objects

## DynamoDb
- [x] Set up new table
- [x] Query table for information (with boto3)
- [x] Store/update information (with boto3)
- [ ] Integrate into Back End [status: integrated with login library]

## S3
- [x] Set up new bucket
- [X] Upload file to S3 (with boto3) [status: base library done]
- [ ] Integrate with Renderer
- [ ] Integrate into Back End

## Local Test
- [ ] Test on localhost

## Zappa (deploy)
- [x] Understand how to deploy using zappa
- [x] Check if Zappa can handle multiprocessing [status: Zappa cannot have background process if the http request has a shorter life span]

- [ ] ~~Check if Zappa can handle "local" files~~ [status: Cancelled. Handling file with in-memeory buffer]
- [ ] Deploy to AWS
- [ ] Test deployed app
