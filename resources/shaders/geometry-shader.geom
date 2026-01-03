#version 330 core

layout(triangles) in;
layout(triangle_strip, max_vertices = 3) out;

in vec3 v_normal[];

out vec3 g_normal;

void main() {
    for (int i = 0; i < 3; i++)
    {
        gl_Position = gl_in[i].gl_Position;
        g_normal = v_normal[i];
        EmitVertex();
    }
    EndPrimitive();
}
