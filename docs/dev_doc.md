# Raytracer Service

> "There is no such thing as shadow, it's just the absence of light."

## 1. Introduction
Raytracer Service is a webapp providing 3D rendering with ray tracing algorithm. It aims to provide an easy-to-use demonstration of the algorithm, which can be handy for teaching and other purposes. 

## 2. High Level Structure
The app consists of four components:

- User Interface (front end webpage)
- Backend Logic
- Rendering Engine
- Database (DynamoDB tables)
- S3 Storage

Each of them are discussed in detail below.

### 2.1 User Interface
The webapp has these following pages:

<table>
<tr><td> Page </td><td>location </td><td> Functionality </td><td>notes</td> </tr>
<tr>
<td> Index </td><td>/index</td><td> Home page <br />Allows user to login or register </td><td>Request to the root "/" will be redirected here </td>
</tr>
<tr>
<td> Login </td><td>/login</td><td> User enters credential to log into the system. </td><td>A failed attempt of login will bring up an error message</td>
</tr>

<tr>
<td> Register </td><td>/register</td><td> Allow user to create new account. </td><td>Username must be unique. After successful registeration, user will be redirected to their dashboard</td>
</tr>
<tr>
<td> Dashboard </td><td>/dashboard</td><td> A user's personal page.<br /> displays user's past rendering request and allow new ones to be issued. Existing images can also be deleted.</td><td>An unauthenticated attempt to visit this page will be redirected to index page</td>
</tr>

<tr>
<td> Request Form </td><td>/form</td><td> Create new rendering request. User must specify the 3D objects to render </td><td>Currently allowed objects include sphere, triangle and rectangle</td>
</tr>
<tr>
<td> Image Page </td><td>/image/[id]</td><td> Displays result of a certain rendering request </td><td></td>
</tr>
<tr>
<td> Public Galleray </td><td>/public</td><td> Lists all public images that are rendered </td><td>User can set if a certain image is public</td>
</tr>

</table>

### 2.2 Backend Logic
The webapp is developed with Flask microframe work. It handles routing and processes form submitted by user. The backend also interacts with the database and the rendering engine.

####2.2.1 User Authentication
Upon registration, a "salt" (random string) is generated and then used to hash the password. The database only store salted and hashed password for security. When a user attempts to log in, the backend will query the database for stored salt and hashed password. Then password provided by user will be salted and hashed in the same way, before comparing with stored values.

###2.2.2 Database Connection
Since the backend is developed in Python, the standard boto3 library is used to interact with DynamoDB.

###2.2.3 Invoking the rendering engine

The rendering engine is deployed as a separated lambda function (more on this later), and invoked using boto3 library. 

Data about rendering request is sent in asyncronous "event" mode. The request will be set to "pending" state at first. Once the rendering is done, it will be set to "success" or "failed".

###2.2.4 Serverless Backend
The webapp can be deployed to AWS Lambda and API Gateway using a library called "Zappa".

###2.3 Database

DynamoDB is used store user related information. Two tables are used. Their structure is shown below in json form.

**Users Table**

	{
		"username": [str, hash key],
		"salt": [str,unique per user],
		"password": [str, salted and hashed]
	}

**Requests Table**

	{
		"requestID": [str, hash key],
		"stat":[str, can be either "pending", "success" or "failed"],
		"ownership": [str, either "public" or "private"],
		"timestamp": [long int, formatted datetime, e.g. 20171125123010 for 2017-11-25 12:30:10],
		"username": [str],
		"entities": [str, json string detailing the objects of the rendering request]
	}

	
###2.4 Rendering Engine

For rendering, a python libaray called PyRT is used. It is a simple raytracer written in Python 3.6, making it a good option to deploy to AWS lambda. A wrapper libray was created to accept json styled input. Once the input is parsed, a 3D scene will be created then rendered into image. The image file is then uploaded to a S3 bucket for persistent storage.

We are aware that python is not the best language to implement raytracing (for Lambda, C# or Java may be better in performance). But since the rendering engine is a stand-alone Lambda function, one can build another (potentially better) engine and replace the current one, as long as the following data interface is accepted.

####2.4.1 Rendering Data Interface
The request must be packed as a dictionary (in Python). It should conform the structure below:

	{
		"id":[str, unique string representing the filename of rendered image, file extension must be included],
		"entities": [list, a list of dictionaries(json objects) representing 3D objects, alongside with light and camera]
	}

The entities can include any of the following:

Sphere

	{
        "type":"sphere",
        "radius":"string representing a float number",
        "center":"x,y,z",#string of float numbers seperated by commas
        "color":"r,g,b" #int  0-255 seperated by commas,
        "reflectivity":"string representing a float number 0-1,"[optional]
    }

Triangle

	{
		"type":"triangle",
		"A":"x,y,z",#string of float numbers seperated by commas,
		"B":"x,y,z",#string of float numbers seperated by commas,
		"C":#string of float numbers seperated by commas,
		'color':'color string as in spheres',
		"reflectivity":"string representing a float number 0-1,"[optional]
	}

Rectangle
	
	{
		"type":"rectangle",
		"A":"x,y,z",#string of float numbers seperated by commas,
		"B":"x,y,z",#string of float numbers seperated by commas,
		"C":#string of float numbers seperated by commas,
		'color':'color string as in spheres',
		"reflectivity":"string representing a float number 0-1,"[optional]
	}
Note that only 3 vertices are required to specify a rectangle. The fourth will be calculated automatically.

Camera

	{	
		"type":"camera",
		'position':"x,y,z"#location of the camera,
		'center':"x,y,z", # the location of center of the view
		"width":[int or str representing an int],
		"height":[int or str representing an int] #width and height of rendered image
	}
Note: The camera will always set the "Up" vector to (0,0,1). The view vector is calculated by `center - position`. Only one camera is allowed. If multiple camera is specified, only the last one will be used. If no camera is provided, a default camera with `height=300, width=400, position=(0,-10,10), center=(0,0,0)` will be used.

Light

	{
		"type": "light",
		"position":"x,y,z" #location of the light"
	}

Note: Point light at given location. Same as the camera, only one light is allowed. If multiple ones are provided, only the last one is used. If no light is provided, a default one with `center=(0,0,15)` will be used.

