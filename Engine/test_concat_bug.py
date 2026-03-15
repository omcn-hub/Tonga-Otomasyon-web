import subprocess
import os
import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def create_test_video():
    # create 2 simple colored images using PIL
    from PIL import Image
    Image.new('RGB', (1920, 1080), color='red').save('red.jpg')
    Image.new('RGB', (1920, 1080), color='blue').save('blue.jpg')
    
    with open("test_list.txt", "w") as f:
        f.write("file 'red.jpg'\n")
        f.write("duration 5\n")
        f.write("file 'blue.jpg'\n")
        f.write("duration 5\n")
        f.write("file 'blue.jpg'\n") # ffmpeg quirk
        
    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "concat", "-safe", "0", "-i", "test_list.txt",
        "-v", "debug",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "test_out.mp4"
    ]
    
    subprocess.run(cmd)
    
if __name__ == '__main__':
    create_test_video()
