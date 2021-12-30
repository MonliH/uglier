def draw_mandelbrot(maxX, minX, height, width, chars=".,-:;i+hHM$*#@ "):
    aspectRatio = width / height
    yScale = (maxX - minX) * (float(height) / width) * aspectRatio

    for y in range(height):
        line = ""
        for x in range(width):
            c = complex(
                minX + x * (maxX - minX) / width, y * yScale / height - yScale / 2
            )
            z = c
            for char in chars:
                if abs(z) > 2:
                    break
                z = z * z + c
            line += char
        print(line)


draw_mandelbrot(-2.0, 1, 36, 78)
