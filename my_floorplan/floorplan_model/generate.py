import copy
import os
import datetime

import numpy as np
import time

import torch

from floorplan_model.options.test_options import TestOptions
from floorplan_model.models.pix2pixHD_model import Pix2PixHDModel
import floorplan_model.util.util as util
from PIL import Image
from torchvision import transforms




def do_preprocess(img, shape):
    preprocess = transforms.Compose([
        transforms.Resize(shape),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5),
                             (0.5, 0.5, 0.5)),
    ])

    return preprocess(img) * 255.0


def load_image(img_file, shape):
    img = Image.open(img_file).convert('RGB')

    return do_preprocess(img, shape)


def is_image(fn):

    return (fn.endswith(".png") or
            fn.endswith(".jpg") or
            fn.endswith(".webp") or
            fn.endswith(".jpeg"))



def do_inference(img, model,device='cuda'):
    shape = (256, 256)






    generated = model.inference(img.view(1, 3, *shape).to(device))

    img_out = util.tensor2im(generated.data[0])

    return img_out


def do_generate(img_path):

    # opt = TestOptions().parse(save=False)

    model = Pix2PixHDModel()
    model.initialize()
    print("11111")
    shape = (256,256)
    img = load_image(img_path, shape)

    img_out = do_inference(img, model,device="cuda")
    img_out = Image.fromarray(img_out)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_name = f"floorplan_output_image_{timestamp}.png"
    filename = os.path.join(base_dir, "../media/GeneratedImage", image_name)
    img_out.save(filename)

    del model
    return image_name











