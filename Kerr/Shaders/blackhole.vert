#version 330

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
out vec2 texcoord;

void main()
{
    // render2d card: vertex.x = [-1,1] left-right, vertex.z = [-1,1] bottom-top
    texcoord    = vec2(p3d_Vertex.x * 0.5 + 0.5,
                       p3d_Vertex.z * 0.5 + 0.5);
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}