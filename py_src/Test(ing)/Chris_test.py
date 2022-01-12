import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;
out vec3 v_color;

void main()
{
    gl_Position = vec4(a_position, 1.0);
    v_color = a_color;
}
"""

fragment_src = """
# version 330

in vec3 v_color;
out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0);
}
"""

# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(1280, 720, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# make the context current
glfw.make_context_current(window)

# okay so the vertices position and the colour values are all here
    # - the first three values in each row are the position of the vertices
    # - the second three values in each row are the colour of that vertex
    # - each value is 4 bits!
vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            -0.5,  0.5, 0.0, 0.0, 0.0, 1.0,
             0.5,  0.5, 0.0, 1.0, 1.0, 1.0]

vertices = np.array(vertices, dtype=np.float32)

# creating the shader program
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# create buffer, bind buffer and send data to buffer
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# this is for position (location = 0)
glEnableVertexAttribArray(0)
# so here the 24 dictates how many bits it jumps from one reading of the position to the next
    # - in this case it is 24 bc theres 6 values per row, so 6*4 = 24 and each of the position values are the first three vals of each row
    # - the ctypes = 0 specifies which index of each row (every 24 bits) it starts on, it is zero bc first three are position
    # - the one above is offset!!!!!!!!!
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

# this is for colour (location = 1)
glEnableVertexAttribArray(1)
# the same thing goes here but the ctypes = 12 means it starts reading from the 4th value in each row (12/4 = 3, next one is 4)
glVertexAttribPointer(1 , 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    # draws the actual thing :D
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()