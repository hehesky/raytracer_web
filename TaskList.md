# Task List

Deadline: 2017-11-30 (demo)

## Design Decisions
- [ ] Data interface [HIGH PRIORITY]
- [ ] Type of 3D objects allowed [HIGH PRIORITY]
- [ ] Limit of requested 3D objects to render

## Back End Dev (Flask)
- [ ] Logic for index page
- [ ] Logic for user log-in and session management
- [ ] Parsing render request (from user) [required data interface to be determined]
  - [ ] Parse Sphere object info (center, radius, color, reflectivity)
  - [ ] Parse Camera info
  - [ ] Parse Light Source info
  - [ ] Parse Triangle
  - [ ] Parse other type of objects
  - [ ] Unit test
- [ ] Render 3D image (pyrt)
  - [x] Scene and Camera
  - [x] Rendering Sphere
  - [ ] Rendering Triangle
  - [ ] Rendering other objects
  - [ ] Unit test
- [ ] Fetching results

## Front End Dev (html,css,js,etc.)
- [ ] Index page
- [ ] Login page (and form)
- [ ] User homepage (displaying fetched results)
- [ ] Request page & request form (include pre-processing logic in js)
  - [ ] allow adding/removing objects (that will be rendered) in the form
  - [ ] provide different type of inputs for different type of objects

## DynamoDb
- [x] Set up new table
- [x] Query table for information (with boto3)
- [x] Store/update information (with boto3)
- [ ] Integrate into Back End

## S3
- [ ] Set up new bucket
- [X] Upload file to S3 (with boto3) [status: old code snippet available]
- [ ] Integrate into Back End

## Local Test
- [ ] Test on localhost

## Zappa (deploy)
- [x] Understand how zappa works
- [ ] Deploy to AWS
- [ ] Test deployed app
