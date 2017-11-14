from pyrt.math import Vec3
from pyrt.scene import Scene
from pyrt.light import PointLight
from pyrt.geometry import Triangle, Sphere, Vertex
from pyrt.material import PhongMaterial
from pyrt.camera import PerspectiveCamera
from pyrt.renderer import SimpleRT
from PIL import Image

import json

def parseSphere(entity):
    """process a dictionary (entity) containing 
    info about a sphere and return a pyrt.gemetry.Sphere() object
    
    entity=
    {
        "type":"sphere",
        "radius":"string representing a float number",
        "center":"x,y,z",#string of float numbers seperated by commas
        "color":"r,g,b" #int  0-255 seperated by commas,
        "reflectivity":"string representing a float number 0-1"
    }
    """

    if entity['type']!="sphere":
        raise ValueError("entity passed to parseSphere() is not a sphere")
    
    s_center=Vec3(entity['center'].split(','))
    s_color=entity['color'].split(',')
    if "reflectivity" in entity:
        s_reflect=entity['reflectivity']
        s_material=PhongMaterial(color=Vec3(s_color),reflectivity=s_reflect)
    else:
        s_material=PhongMaterial(color=Vec3(s_color))
    s_radius=float(entity['radius'])
    return Sphere(center=s_center,radius=s_radius,material=s_material)

def render(entities,imageID):
    """entities is a string representing a json object listing all entities to be rendered"""
    ents=json.load(entities)
    light=None
    camera=None
    objects=[]
    for ent in ents:
        if ent['type']=='sphere':
            objects.append(parseSphere(ent))
        #else:
            #parse other type of objects
    
    #create default camera
    if camera is None:
        camera = PerspectiveCamera(width, height, 45)
        camera.setView(Vec3(0.,-10.,10.), Vec3(0.,0.,0.), Vec3(0.,0.,1.))
    #create scene and add objects to scene
    scene=Scene()
    for obj in objects:
        if type(obj)==list:
            for o in obj:
                scene.add(o)
        else:
            scene.add(obj)
    if light=None:
        light=PointLight(Vec3(-1,-8,1))
    scene.addLight(light)
    engine=SimpleRT(shadow=True,iterations=1)
    image=engine.render(scene)
    image.save(imageID)

if __name__=="__main__":
    ent={"type":"sphere",
    "color":"255,0,0",
    "reflectivity":"0.5",
    'radius':1.25,
    'center':'0,1,1.5'
    }
    ball=parseSphere(ent)
    scene = Scene()
    floormaterial = PhongMaterial(color=Vec3(0.1,0.1,0.1))
    objects=[ball]
    A = Vertex(position=(-5.0, -5.0, 0.0))
    B = Vertex(position=( 5.0, -5.0, 0.0))
    C = Vertex(position=( 5.0,  5.0, 0.0))
    D = Vertex(position=(-5.0,  5.0, 0.0))
    plane=[Triangle(A,B,C, material=floormaterial),Triangle(A,C,D, material=floormaterial)]
    
    objects.append(plane)
    for obj in objects:
        if type(obj)==list:
            for o in obj:
                scene.add(o)
        else:
            scene.add(obj)
    print(scene.nodes)