import math

import glm
from OpenGL.GL import *


class Camera:
    def __init__(
        self,
        position,
        front,
        up,
        speed=0.05,
        fov=math.radians(60.0),
        aspect_ratio=1.0,
        near=1.0,
        far=100.0,
    ):
        self._position = position
        self._front = front
        self._up = up
        self._speed = speed
        self._fov = fov
        self._aspect_ratio = aspect_ratio
        self._near = near
        self._far = far

    def upload_uniforms(self, program):
        view = self._view_matrix()
        proj = self._proj_matrix()

        proj_loc = glGetUniformLocation(program, "projection_matrix")
        view_loc = glGetUniformLocation(program, "view_matrix")
        model_loc = glGetUniformLocation(program, "model_matrix")
        camera_loc = glGetUniformLocation(program, "camera_position")

        identity = glm.mat4(1.0)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(identity))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(proj))
        glUniform3fv(camera_loc, 1, glm.value_ptr(self._position))

    def move_forward(self):
        self._position += self._front * self._speed

    def move_backward(self):
        self._position -= self._front * self._speed

    def move_right(self):
        self._position += glm.normalize(glm.cross(self._front, self._up)) * self._speed

    def move_left(self):
        self._position -= glm.normalize(glm.cross(self._front, self._up)) * self._speed

    def _view_matrix(self):
        return glm.lookAt(self._position, self._position + self._front, self._up)

    def _proj_matrix(self):
        return glm.perspective(self._fov, self._aspect_ratio, self._near, self._far)
