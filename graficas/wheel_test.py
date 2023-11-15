import sys
import math

def generate_solid_wheel_3d(num_sides=8, radius=1.0, wheel_width=0.5):
    if num_sides < 3 or num_sides > 360:
        print("El número de lados del círculo debe estar entre 3 y 360.")
        return
    if radius <= 0 or wheel_width <= 0:
        print("El radio del círculo y el ancho de la rueda deben ser valores positivos.")
        return

    with open("wheel.obj", "w") as obj_file:
        # Generar vértices
        for i in range(num_sides):
            angle = 2 * math.pi * i / num_sides
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            obj_file.write(f"v {x} {y} 0.0\n")
            obj_file.write(f"v {x} {y} {wheel_width}\n")

        # Generar vértices centrales
        obj_file.write(f"v 0.0 0.0 0.0\n")
        obj_file.write(f"v 0.0 0.0 {wheel_width}\n")

        # Generar caras laterales (forma el cilindro y conecta los centros)
        for i in range(1, num_sides + 1):
            next_i = (i % num_sides) + 1
            obj_file.write(f"f {i*2-1} {next_i*2-1} {next_i*2}\n")
            obj_file.write(f"f {i*2} {i*2-1} {next_i*2}\n")
            obj_file.write(f"f {i*2-1} {i*2} {2*num_sides+1}\n")
            obj_file.write(f"f {i*2-1} {next_i*2} {2*num_sides+2}\n")
        
        # Generar vectores normales (apuntando hacia afuera)
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