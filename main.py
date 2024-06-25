import argparse
from blind_watermark import WaterMark
import sys

def embed_imgwm(input_image, watermark_image, output_image, mode, processes):
    bwm = WaterMark(password_wm=1, password_img=1, mode=mode, processes=processes)
    bwm.read_img(filename=input_image)
    bwm.read_wm(wm_content=watermark_image, mode='img')
    bwm.embed(filename=output_image)

def extract_imgwm(input_image, watermark_shape, output_image, mode, processes):
    bwm = WaterMark(password_wm=1, password_img=1, mode=mode, processes=processes)
    bwm.extract(filename=input_image, wm_shape=watermark_shape, out_wm_name=output_image, mode='img')

def embed_textwm(input_image, output_image, watermark_text, mode, processes):
    bwm1 = WaterMark(password_img=1, password_wm=1, mode=mode, processes=processes)
    bwm1.read_img(filename=input_image)
    bwm1.read_wm(wm_content=watermark_text, mode='str')
    bwm1.embed(filename=output_image)
    len_wm = len(bwm1.wm_bit)
    print(f'The bit length of embedded text watermark is {len_wm}')
    return len_wm

def extract_textwm(input_image, wm_length, mode, processes):
    bwm1 = WaterMark(password_img=1, password_wm=1, mode=mode, processes=processes)
    wm_extract = bwm1.extract(filename=input_image, wm_shape=wm_length, mode='str')
    print(wm_extract)
    return wm_extract

def main():
    parser = argparse.ArgumentParser(description='Comprehensive Blind Watermarking Tool')
    subparsers = parser.add_subparsers(dest='command', help='Sub-commands: addimg, extimg, addtext, exttext')

    # Subparser for embedding image watermark
    embed_img_parser = subparsers.add_parser('addimg', help='Embed a picture watermark into an image')
    embed_img_parser.add_argument('input_image', type=str, help='Path to the input image')
    embed_img_parser.add_argument('watermark_image', type=str, help='Path to the watermark image')
    embed_img_parser.add_argument('output_image', type=str, help='Path to save the watermarked image')
    embed_img_parser.add_argument('--mode', type=str, default='multithreading', help='Processing mode: common or multithreading')
    embed_img_parser.add_argument('--processes', type=int, default=4, help='Number of processes for multithreading')

    # Subparser for extracting image watermark
    extract_img_parser = subparsers.add_parser('extimg', help='Extract a picture watermark from an image')
    extract_img_parser.add_argument('input_image', type=str, help='Path to the watermarked image')
    extract_img_parser.add_argument('watermark_shape', type=int, nargs=2, help='Shape of the watermark (height, width)')
    extract_img_parser.add_argument('output_image', type=str, help='Path to save the extracted watermark')
    extract_img_parser.add_argument('--mode', type=str, default='multithreading', help='Processing mode: common or multithreading')
    extract_img_parser.add_argument('--processes', type=int, default=4, help='Number of processes for multithreading')

    # Subparser for embedding text watermark
    embed_text_parser = subparsers.add_parser('addtext', help='Embed a text watermark to an image')
    embed_text_parser.add_argument('input_image', type=str, help='Path to the input image')
    embed_text_parser.add_argument('output_image', type=str, help='Path to the output image with watermark')
    embed_text_parser.add_argument('watermark_text', type=str, help='Text to be used as the watermark')
    embed_text_parser.add_argument('--mode', type=str, default='multithreading', help='Processing mode: common or multithreading')
    embed_text_parser.add_argument('--processes', type=int, default=4, help='Number of processes for multithreading')

    # Subparser for extracting text watermark
    extract_text_parser = subparsers.add_parser('exttext', help='Extract a text watermark from an image')
    extract_text_parser.add_argument('input_image', type=str, help='Path to the image with watermark')
    extract_text_parser.add_argument('wm_length', type=int, help='Length of the watermark text in bits')
    extract_text_parser.add_argument('--mode', type=str, default='multithreading', help='Processing mode: common or multithreading')
    extract_text_parser.add_argument('--processes', type=int, default=4, help='Number of processes for multithreading')

    args = parser.parse_args()

    if args.command == 'addimg':
        embed_imgwm(args.input_image, args.watermark_image, args.output_image, args.mode, args.processes)
    elif args.command == 'extimg':
        watermark_shape = (args.watermark_shape[0], args.watermark_shape[1])
        extract_imgwm(args.input_image, watermark_shape, args.output_image, args.mode, args.processes)
    elif args.command == 'addtext':
        embed_textwm(args.input_image, args.output_image, args.watermark_text, args.mode, args.processes)
    elif args.command == 'exttext':
        extract_textwm(args.input_image, args.wm_length, args.mode, args.processes)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
