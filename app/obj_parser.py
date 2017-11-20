import json
from pyrt.geometry import Triangle, Sphere, Vertex
from pyrt.math import Vec3
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
    s_color=Vec3(s_color)
    s_color.normalize()
    if "reflectivity" in entity:
        s_reflect=float(entity['reflectivity'])
        s_material=PhongMaterial(color=s_color,reflectivity=s_reflect)
    else:
        s_material=PhongMaterial(color=s_color)
    s_radius=float(entity['radius'])
    return Sphere(center=s_center,radius=s_radius,material=s_material)

def parseTriangle(entity):
	if entity['type']!='triangle':
		raise ValueError("entity passed to parseTriangle is not a triangle")
	A_pos=entity['A'].split(',')
	B_pos=entity['B'].split(',')
	C_pos=entity['C'].split(',')
	assert len(A_pos)==3
	A=Vertex(position=A_pos)
	B=Vertex(position=B_pos)
	C=Vertex(position=C_pos)
	
	t_color_txt= entity['color'].split(',')
	t_color=Vec3(t_color)
	t_color.normalize()
	
	if "reflectivity" in entity:
        t_reflect=float(entity['reflectivity'])
        t_material=PhongMaterial(color=s_color,reflectivity=s_reflect)
    else:
        t_material=PhongMaterial(color=s_color)
    
	return Triangle(A,B,C,material=t_material)
	
	
	