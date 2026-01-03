#version 330 core

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec3 in_tex;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform mat4 model_matrix;

out vec3 v_position;
out vec3 v_normal;

void main()
{
    vec4 worldPos = model_matrix * vec4(in_position, 1.0);

    v_position = worldPos.xyz;
    v_normal = mat3(model_matrix) * in_normal;

    gl_Position = projection_matrix * view_matrix * worldPos;
}
