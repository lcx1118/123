from inspect import isfunction
from torchvision.utils import make_grid, save_image
import torch
def extract(a, t, x_shape):
    b, *_ = t.shape
    out = a.gather(-1, t)
    return out.reshape(b, *((1,) * (len(x_shape) - 1)))


def exists(x):
    return x is not None


def default(val, d):
    if exists(val):
        return val
    return d() if isfunction(d) else d

def get_image_grid(batch, grid_size=4, to_normal=True):
    batch = batch.detach().clone()
    image_grid = make_grid(batch, nrow=grid_size)
    if to_normal:
        image_grid = image_grid.mul_(0.5).add_(0.5).clamp_(0, 1.)
    image_grid = image_grid.mul_(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to('cpu', torch.uint8).numpy()
    return image_grid