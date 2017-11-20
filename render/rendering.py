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
    """entities is dictionary representing objects in scene"""

    

    #create scene and add objects to scene
    scene=Scene()
    for obj in ents['objects']:
        if isinstance(obj,list):
            for o in obj:
                scene.add(o)
        else:
            scene.add(obj)
    if ents['light'] is None:
        ents['light']=PointLight(Vec3(-1,-8,1))
    scene.addLight(ents['light'])
    scene.setCamera(ents['camera'])
    engine=SimpleRT(shadow=True,iterations=2)
    pixles=engine.render(scene)
    image=Image.new('RGB',(ents['camera'].width,ents['camera'].height))
    image.putdata(pixles)
    return image

def lambda_handler(event,context):
	raise NotImplementedError