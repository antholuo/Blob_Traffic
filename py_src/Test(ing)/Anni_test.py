from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import time

name = 'ball_glut'

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400,400)
    glutCreateWindow(name)


    glClearColor(0.,0.,0.,1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [10.,4.,10.,1.]
    lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
    lightOnePosition = [1, 12, 1, 1]
    lightOneColor = [1.0, 0.2, 0.2, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT1, GL_POSITION, lightOnePosition)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightOneColor)
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT1)

    rotation()

    glutDisplayFunc(display)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,40.)
    glMatrixMode(GL_MODELVIEW)

    gluLookAt(0,0,10,
              0,0,0,
              0,1,0)

    glPushMatrix()
    glutMainLoop()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    color = [1.0,0.4,0.7,0.7]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)

    glutSolidSphere(2,200,200)
    glutSolidCube(3)

    glPopMatrix()
    glutSwapBuffers()
    return

def rotation():
    glMatrixMode(GL_MODELVIEW)
    modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    gluLookAt(0, 0, 10,
              0, 0, 0,
              0, 1, 0)

    while True:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotated(5, 1, 0, 0)

        glMultMatrixf(modelMatrix)
        modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        glLoadIdentity()
        glTranslatef(0, 0, -5)
        glMultMatrixf(modelMatrix)
        color = [1.0, 0.4, 0.7, 0.7]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)

        glutSolidSphere(2, 200, 200)
        glutSolidCube(3)

        glPopMatrix()
        glutSwapBuffers()

        time.sleep(1)


if __name__ == '__main__':
    main()
