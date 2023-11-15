import sys
import math

def generate_solid_wheel_3d(num_sides=8, radius=1.0, wheel_width=0.5):

    with open("wheel.obj", "w") as obj_file:
        # Generar vértices
        for i in range(num_sides):
            angle = 2 * math.pi * i / num_sides
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            # Agregar vértices al archivo OBJ en 3D
            obj_file.write(f"v {x} {y} 0.0\n")
            obj_file.write(f"v {x} {y} {wheel_width}\n")

        # Generar caras laterales (forma el anillo de la rueda)
        for i in range(1, num_sides + 1):
            next_i = (i % num_sides) + 1
            obj_file.write(f"f {i*2-1} {next_i*2-1} {next_i*2}\n")
            obj_file.write(f"f {i*2} {i*2-1} {next_i*2}\n")

        # Generar caras superiores e inferiores
        obj_file.write("f ")
        for i in range(num_sides, 0, -1):
            obj_file.write(f"{i*2-1} ")
        obj_file.write("\n")

        obj_file.write("f ")
        for i in range(1, num_sides + 1):
            obj_file.write(f"{i*2} ")
        obj_file.write("\n")

        # Generar vectores normales (apuntando hacia afuera en la dirección z)
        for i in range(1, num_sides + 1):
            obj_file.write(f"vn 0.0 0.0 1.0\n")

    print("Archivo wheel.obj generado exitosamente.")

if __name__ == "__main__":
    num_sides = 8
    radius = 1.0
    wheel_width = 0.5

    if len(sys.argv) > 1:
        try:
            num_sides = int(sys.argv[1])
            radius = float(sys.argv[2])
            wheel_width = float(sys.argv[3])
        except (ValueError, IndexError):
            pass

    generate_solid_wheel_3d(num_sides, radius, wheel_width)
