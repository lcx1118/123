import os

import ezdxf
import matplotlib
from django.shortcuts import render
from model import main as model_main
from floorplan_model.generate import do_generate
from diffusion.sample import do_sample

# Create your views here.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from myapp.serializers import CustomUserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from my_floorplan import settings
from pathlib import Path
from django.http import JsonResponse
# from ezdxf.render import RenderContext, MatplotlibBackend
User = get_user_model()

import ezdxf
from ezdxf import recover
from ezdxf.tools.standards import setup_linetypes
import matplotlib.pyplot as plt


def convert_dxf_to_png(dxf_path, png_path):
    # 尝试读取DXF文件
    doc = ezdxf.readfile(dxf_path)

    # 获取模型空间
    msp = doc.modelspace()

    # 准备绘图
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='datalim')
    ax.axis('off')

    # 绘制所有实体
    for entity in msp:
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            ax.plot([start[0], end[0]], [start[1], end[1]], 'k-')

    # 保存图像
    fig.savefig(png_path, dpi=300)
    plt.close(fig)


# convert_dxf_to_png('your_dxf_file.dxf', 'output_file.png')


class RegisterView(APIView):
    def post(self, request):
        print("1111")
        # print(request.data)
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "exists"}, status=status.HTTP_400_BAD_REQUEST)
        # print(serializer.errors)
        return Response({"error": "Email or phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        email_or_phone = request.data.get('name')
        password = request.data.get('password')
        user = authenticate(request, username=email_or_phone, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
# views.py


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        # 保存上传的图像
        file_obj = request.FILES['file']
        file_path = default_storage.save('uploads/' + file_obj.name, file_obj)
        image_path = os.path.join("media",file_path)
        print("开始生成")
        # print(image_path)
        timestamp = do_generate(image_path)
        image_url = os.path.join(settings.MEDIA_URL, f"GeneratedImage/{timestamp}")


        # 响应可以包括生成的文件的URL或其他信息
        return Response({"message": "文件上传成功", "image_url": image_url}, status=200)

class ImageUploadView2(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        # 保存上传的图像
        file_obj = request.FILES['file']
        file_path = default_storage.save('uploads/' + file_obj.name, file_obj)
        image_path = os.path.join("media",file_path)
        print("开始生成")
        # print(image_path)
        timestamp = do_sample(image_path)
        image_url = os.path.join(settings.MEDIA_URL, f"GeneratedImage/{timestamp}")


        # 响应可以包括生成的文件的URL或其他信息
        return Response({"message": "文件上传成功", "image_url": image_url}, status=200)

class BoundaryUploadView(APIView):
    def post(self, request, *args, **kwargs):
        # file = request.FILES['cadfile']
        # fs = FileSystemStorage()
        # filename = fs.save('uploads_CAD/'+file.name, file)
        # file_path = fs.path(filename)
        #
        # # 假设使用一个命令行工具进行转换
        # output_path = file_path + '.png'
        # convert_command = f"cad-to-image-tool {file_path} {output_path}"
        # subprocess.run(convert_command, shell=True)
        #
        # return Response({"message": "文件上传并转换成功", "imageUrl": fs.url(output_path + '.png')})

        file = request.FILES.get('cadfile')

        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.dxf'):
            return Response({"message": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)
        # print("11111")
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)
        output_path = str(Path(file_path).with_suffix('.png'))
        # print(file_path)
        # print(output_path)

        try:
            convert_dxf_to_png(file_path, output_path)
        except Exception as e:
            print(e)
            return Response({"message": "File conversion failed: " + str(e)})
        # print("333")
        relative_output_path = output_path.replace(str(Path(settings.MEDIA_ROOT)), '').lstrip('\\/')
        image_url = fs.url(relative_output_path)
        # print(image_url)
        return Response({"message": "文件上传并转换成功", "imageUrl": image_url})


class HousingAndCoreSubmitView(APIView):

    def post(self, request, *args, **kwargs):
        house_types = request.POST.getlist('houseTypes')
        traffic_cores = request.POST.getlist('trafficCores')
        # 你可以在这里添加进一步的处理逻辑，例如保存数据或触发其他操作
        return Response({
            "message": "接收到的户型有: {} 和交通核有: {}".format(", ".join(house_types), ", ".join(traffic_cores))
        }, status=status.HTTP_200_OK)



class ImageView(APIView):
    def get(self, request):
        # 图片存储的子目录
        floorplan_dir = os.path.join(settings.MEDIA_ROOT, 'floorplan_img')
        core_dir = os.path.join(settings.MEDIA_ROOT, 'core_img')
        # 列出所有图片并创建URL路径
        floorplan_list = [os.path.join(settings.MEDIA_URL, 'floorplan_img', image) for image in
                          os.listdir(floorplan_dir) if image.endswith(('jpg', 'png'))]
        core_list = [os.path.join(settings.MEDIA_URL, 'core_img', image) for image in os.listdir(core_dir) if
                     image.endswith(('jpg', 'png'))]
        # print(">>>>>>>>>>>>>>>>>>>>>>>>")
        print(floorplan_list)
        # print(JsonResponse(floorplan_list, safe=False))
        return JsonResponse({
            'floorplan': floorplan_list,
            'core': core_list
        }, safe=False)

    def extract_image_names(self,image_paths):
        image_names = []
        for path in image_paths:
            # 获取文件名（包括扩展名）
            base_name = os.path.basename(path)
            # 去除扩展名
            name, _ = os.path.splitext(base_name)
            image_names.append(name)
        return image_names

    def post(self, request):
        selected_images = request.data.get('selectedImages', [])
        # print(selected_images)
        if not selected_images:
            return JsonResponse({"error": "No images selected"}, status=400)
        image_names = self.extract_image_names(selected_images)
        # print(image_names)
        timestamp = model_main.main1(image_names)  # 假设这个函数返回图片的路径
        # 构建访问图片的 URL
        image_url = os.path.join(settings.MEDIA_URL, f"GeneratedImage/output_image_{timestamp}.png")
        # print(image_url)

        return JsonResponse({
            "message": "Image generated successfully",
            "imageUrl": image_url,
            "imageNames": image_names
        })

# urls.py
