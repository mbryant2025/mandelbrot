from PIL import Image
import asyncio

DIVERGENCE_ITERATIONS = 100
IMAGE_SIZE = 10000

#Returns integer [0-100) depending on how quickly z^2 + c diverges
#Return of 100 is convergence
def determine_divergence(c: complex) -> int:
    z = 0
    for i in range(0, DIVERGENCE_ITERATIONS):
        z = z**2 + c
        if abs(z) > 2:
            break
    return i
    

#Renders a row of the image asynchronously
async def render_row(row: int, img: Image.Image):
    for j in range(IMAGE_SIZE):
        c = complex((row-IMAGE_SIZE/2)/(IMAGE_SIZE/4), (j-IMAGE_SIZE/2)/(IMAGE_SIZE/4))
        divergence = determine_divergence(c)
        img.putpixel((row, j), (255 * divergence // 100, 0, 0))


async def call_async(img: Image.Image):
    tasks = []
    for i in range(IMAGE_SIZE):
        tasks.append(loop.create_task(render_row(i, img)))
    await asyncio.wait(tasks)
    

if __name__ == "__main__":
    #Real and imaginary axes are bounded [-2, 2]
    image = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(call_async(image))

    image.save('mandelbrot.png')
