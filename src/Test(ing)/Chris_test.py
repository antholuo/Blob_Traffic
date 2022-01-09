import numpy as np
from glumpy import app, gl, glm, gloo
import sys
import OpenGL.GLUT as glut

def display():
    glut.glutSwapBuffers()

def reshape(width,height):
    gl.glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == b'\x1b':
        sys.exit( )

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow('Hello world!')
glut.glutReshapeWindow(512,512)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)
glut.glutMainLoop()


'''
in opengl the coordinates go 

(-1, +1)    (+1, +1)

       (0 , 0)

(-1, -1)    (+1, -1)

important to know: barycentric interpolation !!

'''


data = np.zeros(4, dtype = [ ("position", np.float32, 3),
                                ("color",    np.float32, 4)] )
# the first 4 refers to the vertices, then there are 3 position values for x,y,z and 4 colour values for rgba
# if working in 2d we dont need the x axis so the 3 can be changed into 2
data = np.zeros(4, dtype = [ ("position", np.float32, 2),
                                ("color",    np.float32, 4)] )

# THIS IS THE VERTEX SHADER
vertex = """

// vec2 just means a tuple of 2 floats and vec4 means a tuple of 4 floats
// vertex shader now expects a vertex to possess 2 attributes: position and colour

uniform float scale;    // if we wanna scale all our vertexes by smth?
attribute vec2 position; 
attribute vec4 color;
varying vec4 v_color;   // used to pass info between vertex stage and fragment stage

void main()
{
    gl_Position = vec4(position*scale, 0.0, 1.0);
    v_color = color;    // we do this (plus the fragment code of gl_FragColor = v_colour to pass vertex color
                        // to fragment shader
}

"""

# THIS IS THE FRAGMENT SHADER
fragment = """

varying vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}

"""


print(data)

