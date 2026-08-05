## This script defines functions to calculate the volume of a cylinder and a sphere.
# It also demonstrates the use of lambda functions for the same calculations.
def find_cylinder_volume(radius, height=7):
    print("radius:", radius)
    print("height:", height)
    volume = 3.14*(radius**2)*height
    print(volume)
    return volume

def find_sphere_volume(radius):
    print("radius:", radius)
    volume = (4/3) * 3.14 * (radius**3)
    print(volume)
    return volume

r = 5
h = 10

print(f'The volume of the cylinder is: {find_cylinder_volume(r, h)}')
print(f'The volume of the sphere is: {find_sphere_volume(r)}')


## Using lambda functions to calculate volumes

cylinder_volume = lambda r,h: 3.14 * (r**2) * h
sphere_volume = lambda r: (4/3) * 3.14 * (r ** 3)

print(f'The volume of the cylinder is: {cylinder_volume(r, h)}')
print(f'The volume of the sphere is: {sphere_volume(r)}')
