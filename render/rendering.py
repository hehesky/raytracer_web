#! python3

from pyrt.math import Vec3
from pyrt.scene import Scene
from pyrt.light import PointLight
from pyrt.geometry import Triangle, Sphere, Vertex
from pyrt.material import PhongMaterial
from pyrt.camera import PerspectiveCamera
from pyrt.renderer import SimpleRT
from PIL import Image


def render(ents):
    """entities is dictionary representing a json object listing all entities to be rendered"""
    
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
        camera = PerspectiveCamera(400, 300, 45)
        camera.setView(Vec3(0.,-10.,10.), Vec3(0.,0.,0.), Vec3(0.,0.,1.))
    #create scene and add objects to scene
    scene=Scene()
    for obj in objects:
        if type(obj)==list:
            for o in obj:
                scene.add(o)
        else:
            scene.add(obj)
    if light is None:
        light=PointLight(Vec3(-1,-8,1))
    scene.addLight(light)
    scene.setCamera(camera)
    engine=SimpleRT(shadow=True,iterations=2)
    pixles=engine.render(scene)
    image=Image.new('RGB',(camera.width,camera.height))
    image.putdata(pixles)
    return image

def lambda_handler(event,context):
	raise NotImplementedError