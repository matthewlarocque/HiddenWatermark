from PIL import Image

# 打开PNG图像
image = Image.open('embedded.png')

# 获取图像的宽度和高度
width, height = image.size

# 计算要裁剪的宽度
crop_width = int(width * 0.2)

# 计算要复制的宽度
copy_width = width - crop_width

# 裁剪图像的右边20%
left_crop = image.crop((0, 0, copy_width, height))

# 复制图像的左边20%并进行循环补齐
right_copy = left_crop.copy()

# 创建一个新的图像，将左边复制和右边裁剪合并在一起
result_image = Image.new('RGB', (width, height))
result_image.paste(left_crop, (0, 0))
result_image.paste(right_copy, (copy_width, 0))

# 保存结果图像
result_image.save('attack.png')

# 关闭原始图像
image.close()
