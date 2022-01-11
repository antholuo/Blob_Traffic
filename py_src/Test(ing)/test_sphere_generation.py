from glumpy import app, gloo, gl, glm
import math
import numpy as np

vertex_land = """
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    attribute vec3 position;
    attribute vec4 color;
    varying vec4 v_color;
    void main(){
        gl_Position = projection * view * model * vec4(position, 1.0);
        v_color = color; 
    } """

fragment_land = """
    varying vec4 v_color;
    void main() { 
        gl_FragColor = v_color; 
    } """

vertex_wall = """
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    attribute vec3 position;

    void main() {
        gl_Position = projection * view * model * vec4(position, 1.0);
    }
"""

fragment_wall = """
    void main() { 
        gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0); 
    } 
    """

# Create a window with a valid GL context
window = app.Window()


# Tell glumpy what needs to be done at each redraw
@window.event
def on_resize(width, height):
    ratio = width / float(height)
    quad['projection'] = glm.perspective(35.0, ratio, 2.0, 100.0)
    wall['projection'] = glm.perspective(35.0, ratio, 2.0, 100.0)


@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)
    wall.draw(gl.GL_TRIANGLES, I)

    model = np.eye(4, dtype=np.float32)

    glm.rotate(model, 30, 0, 1, 0)
    glm.rotate(model, 20, 1, 0, 0)

    quad['model'] = model
    wall['model'] = model


# Run the app
@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)


view = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -5)
projection = np.eye(4, dtype=np.float32)
model = np.eye(4, dtype=np.float32)

# vertices of the wall
V = np.zeros(8, [("position", np.float32, 3)])
V["position"] = [[0.5, 0.5, 0.5], [-0.5, 0.5, 0.5], [-0.5, 0, 0.5], [0.5, 0, 0.5],
                 [0.5, 0, 0], [0.5, 0.5, 0], [-0.5, 0.5, 0], [-0.5, 0, 0]]
V = V.view(gloo.VertexBuffer)
I = np.array([0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6, 0, 6, 1,
              1, 6, 7, 1, 7, 2, 7, 4, 3, 7, 3, 2, 4, 7, 6, 4, 6, 5], dtype=np.uint32)
I = I.view(gloo.IndexBuffer)

wall = gloo.Program(vertex_wall, fragment_wall)
wall.bind(V)
wall['model'] = np.eye(4, dtype=np.float32)
wall['view'] = glm.translation(0, 0, -5)

quad = gloo.Program(vertex_land, fragment_land, count=4)

quad['position'] = (-1, 0, +1), (+1, 0, +1), (-1, 0, -1), (+1, 0, -1)
quad['color'] = (1, 1, 0, 1), (1, 0, 0, 1), (0, 0, 1, 1), (0, 1, 0, 1)
quad['model'] = model
quad['view'] = view
quad['projection'] = projection
# quad['theta'] = 0.0


app.run()
