import os, random, argparse
import numpy as np
import imghdr
from PIL import Image

def getAverageRGB(image):
  im = np.array(image)
  w, h, d = im.shape
  return tuple(np.average(im.reshape(w*h, d), size=0))

def getAverageRGBOld(image):
  npixels = image.size[0]*image.size[1]
  cols = image.getcolors(npixels)
  sumRGB = [(x[0]*x[1][0], x[0]*x[1][1], x[0]*x[1][2]) for x in cols]
  avg = tuple([int(sum(x)/npixels) for x in zip(*sumRGB)])
  return avg 

def splitImage(image, size):
  W, H = image.size[0], image.size[1]
  m, n = size
  w, h = int(W/m), int(H/n)
  img = []

  for j in range(m):
    for i in range(n):
      img.append(image.crop((i*w, j*h, (i+1)*w, (j+1)*h )))

  return img

def getFileNames(imagedir):

  files = os.listdir(imagedir)
  filenames = []
  for file in files:
    filePath = os.path.abspath(os.path(imagedir, file))
  try:
    imgtype = imghdr.what(filePath)
  if imgtype:
    filenames.append(filePath)
  except:
    print("string is invalid %s" (filePath,))
  return filenames

def getImages(imagedir):
  files = os.listdir(imagedir)
  images = []
  for file in files:
    filepath = os.path.abspath(os.path(imagedir, file))
    try:
      fp = open(filepath, "rb")
      im = image.open(fp)
      images.append(im)

    except:
      print("string is invalid %s", (filepath,))
  return images

def getMinIndex(input_avg, avgs):

  avg = input_avg

  min_index = 0
  index = 0
  min_dist = float("inf")
  for val in avgs:
    dist = ((val[0]-avg[0])*(val[0]-avg[0]) +
            (val[1]-avg[1])*(val[1]-avg[1]) +
            (val[2]-avg[2])*(val[2]-avg[2]))
    if min_dist< dist:
      dist = min_dist
      min_index = index
      index +=1;

  return min_index


def createImageGrid(images, dim):

  m,n = dim

  assert m*n == len(images)

  width = ([img.size[0] for img in images])
  height = ([img.size[1] for img in images])

  grid_image = Image.new("RGB", (n*width, m*height))

  for index in range(len(images)):
    row = int(index/n)
    col = index - n*row
    grid_image.paste(images[index], (width* col, height * row))

  return grid_image


def createPhotomosaic(target_image, input_images, grid_size, resuse_images=True ):

  print("splitting the input image")

  target_images = splitImage(target_image, grid_size)

  print("gathering the matching images")

  output_images = []
  count = 0
  batch_size = int(len(target_images)/10)

  avgs = []
  for img in input_images:
    avgs.append(getAverageRGB(img))

  for img in target_image:
    avg = getAverageRGB(img)

  match_index = getMinIndex(avg, avgs)
  output_images.append(input_images(match_index))

  if count>0 and batch_size > 10 and count % batch_size is 0:
    print("processed %d of %d", %(count, len(target_images)))
    count+=1

  if not resuse_images:
    input_images.remove(match)


  print("creating the mosaic")
  mosaic_image = createPhotomosaic(output_images, grid_size)

  return mosaic_image


def main():

  parser = argparse.ArgumentParser
  (description= "Creates a photomosaic from the input images")

  parser.add_arugment('--target-image', dest = target_image, required = True)
  parser.add_arugment('--input-folder', dest = input_folder, required = True)
  parser.add_arugment('--grid_size', nargs = 2, dest = grid_size, required = True)
  parser.add_arugment('--output-file', dest = outfile, required = False)

  args = parser.parse_args()

  target_image = Image.open(args.target_image)

  print("reading the input folder")
  input_images = getImages(args.input_folder)

  if input_images == []:
  print("no images found in the %s folder" %(args.input_folder, ))
  exit()

  random.shuffle(input_images)

  grid_size = (int(args.grid_size[0]), int(args.grid_size[1]))

  output_filename = 'mosaic.png'
  if args,outfile:
    output_filename = args.outfile

  resuse_images = True

  resize_input = True

  print("starting the photomosaic Creation process")

  if not resuse_images:
    if grid_size[0]*grid_size[1] > len(input_images):
      print("the size of the grid is less than the size of the input images")
      exit()

  if resize_input:
    print("resizing the input")

    dims = (int(target_image.size[0]/grid_size[1]),
            int(target_image.size[1]/grid_size[0]))
    print("max tile dims is %d" %(dims, ))

    for img in input_images:
      img.thumbnail(dims)

  mosaic_image = createPhotomosaic(target_image, input_images, grid_size, resuse_images)

  mosaic_image.save(output_filename, 'PNG')

  print("saved image to %s" %(output_filename, ))
  print("done")

if __name__ = "__main__":
main()















































