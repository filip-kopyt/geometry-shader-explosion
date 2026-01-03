#version 330 core

in vec3 v_position;
in vec3 v_normal;

out vec4 f_color;

const vec3 light_position = vec3(3.0, 3.0, 3.0);
const vec3 light_ambient = vec3(0.1, 0.1, 0.1);
const vec3 light_diffuse = vec3(1.0, 1.0, 1.0);
const vec3 light_specular = vec3(0.8, 0.8, 0.8);

uniform vec3 camera_position;

uniform vec3 material_ambient;
uniform vec3 material_diffuse;
uniform vec3 material_specular;
uniform float material_shininess;

void main()
{
    vec3 ambient = light_ambient * material_ambient;

    vec3 N = normalize(v_normal);
    vec3 L = normalize(light_position - v_position);
    vec3 V = normalize(camera_position - v_position);
    vec3 R = reflect(-L, N);

    float cosNL = clamp(dot(N, L), 0.0, 1.0);
    vec3 diffuse = light_diffuse * material_diffuse * cosNL;

    float cosVR = clamp(dot(V, R), 0.0, 1.0);
    float shininess = pow(cosVR, material_shininess);
    vec3 specular = light_specular * material_specular * shininess;

    vec3 phong_color = clamp(ambient + diffuse + specular, 0.0, 1.0);

    f_color = vec4(phong_color, 1.0);
}
