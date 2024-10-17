import datetime
import random

import torch
from diffusion.model.BrownianBridgeModel import BrownianBridgeModel
from PIL import Image
import torchvision.transforms as transforms
from diffusion.model.utils import get_image_grid
import os

def process_image(img_path, image_size=(256, 256), flip=False, to_normal=True):
    """
    Process a single image given its file path.

    :param img_path: str, path to the image file
    :param image_size: tuple, the target size of the image (width, height)
    :param flip: bool, whether to apply horizontal flip to the image
    :param to_normal: bool, whether to normalize the image to the range [-1, 1]
    :return: torch.Tensor, processed image tensor
    """
    # 尝试打开图像文件
    try:
        image = Image.open(img_path).convert('RGB')
    except IOError as e:
        print(f"Error opening image {img_path}: {e}")
        return None

    # 定义图像转换流程
    transform = transforms.Compose([
        transforms.Resize(image_size),  # 调整图像大小
        transforms.ToTensor()  # 转换为PyTorch张量
    ])

    # 如果图像不是RGB模式，则先转换为RGB模式
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # 应用图像转换流程
    image = transform(image)

    # 如果需要，将图像归一化到[-1, 1]
    if to_normal:
        image = (image - 0.5) * 2.  # 归一化操作
        image.clamp_(-1., 1.)  # 确保值在[-1, 1]区间内

    return image





def do_sample(img_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # 使用示例


    processed_image = process_image(img_path, flip=True, to_normal=True)
    processed_image = processed_image.unsqueeze(0).to(device)
    print(processed_image.shape)
    bbdmnet = BrownianBridgeModel().to(device)
    model_states = torch.load('diffusion/model/latest_model_4.pth', map_location='cpu')
    bbdmnet.load_state_dict(model_states['model'])

    img=bbdmnet.sample(y=processed_image)
    image_grid = get_image_grid(img, 4, to_normal=True)
    im = Image.fromarray(image_grid)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_name = f"floorplan_output_image_{timestamp}.png"
    filename = os.path.join(base_dir, "../media/GeneratedImage", image_name)


    im.save(filename)
    return image_name

