import math
from pathlib import Path
from typing import override

import moderngl as mgl
import moderngl_window as mglw
from objloader import Obj
from pyglm import glm

from config import GL_VERSION, OBJECT_FILENAME, WINDOW_SIZE, WINDOW_TITLE
from util import load_file, root_dir


class GeometryModel:
    def __init__(self, ctx: mgl.Context, path: Path):
        obj = Obj.open(path)
        self.ctx = ctx
        self.vbo = ctx.buffer(obj.pack(("vx vy vz nx ny nz tx ty")))

    def vertex_array(self, program: mgl.Program) -> mgl.VertexArray:
        return self.ctx.vertex_array(
            program,
            [(self.vbo, "3f 3f 2f", "in_position", "in_normal", "in_uv")],
        )


class Window(mglw.WindowConfig):
    gl_version = GL_VERSION
    window_size = WINDOW_SIZE
    title = WINDOW_TITLE
    resource_dir = root_dir() / "resources"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shader_program = self._load_shader_program()
        self.model = self._load_model(OBJECT_FILENAME)
        self.vao = self.model.vertex_array(self.shader_program)

    def _load_shader_program(self) -> mgl.Program:
        shaders_path = self.resource_dir / "shaders"
        return self.ctx.program(
            vertex_shader=load_file(shaders_path / "vertex-shader.vert"),
            # geometry_shader=load_file(shaders_path / "geometry-shader.geom"),
            fragment_shader=load_file(shaders_path / "fragment-shader.frag"),
        )

    def _load_model(self, filename: str) -> GeometryModel:
        objects_path = self.resource_dir / "objects"
        return GeometryModel(self.ctx, objects_path / filename)

    def get_camera_matrices(self, time: float) -> tuple[glm.mat4, glm.mat4]:
        eye = (5.0 * math.sin(time), 5.0 * math.cos(time), 3.0)
        proj = glm.perspective(math.radians(60.0), self.wnd.aspect_ratio, 1.0, 1000.0)
        look = glm.lookAt(eye, (0, 0, 0), (0.0, 0.0, 1.0))
        return proj, look

    @override
    def on_render(self, time: float, frame_time: float) -> None:
        self.ctx.clear(0.25, 0.25, 0.25, 0.25)

        proj, view = self.get_camera_matrices(time)

        self.shader_program["projection_matrix"].write(proj)
        self.shader_program["model_matrix"].write(glm.mat4(1.0))
        self.shader_program["view_matrix"].write(view)

        self.vao.render(mgl.TRIANGLES)
