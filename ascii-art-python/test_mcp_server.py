#!/usr/bin/env python3
"""
测试ASCII Art MCP Server的工具
"""

import asyncio
from ascii_art_server import generate_ascii_art, generate_ascii_image
from pathlib import Path


async def test_ascii_art():
    """测试文本ASCII艺术生成"""
    print("=" * 60)
    print("测试 1: 生成文本ASCII艺术（使用绝对路径）")
    print("=" * 60)
    
    # 获取绝对路径
    abs_path = Path("scan_test.jpg").absolute()
    
    result = await generate_ascii_art(
        image_path=str(abs_path),
        width=80,
        charset="simple"
    )
    
    print(result)
    print()


async def test_ascii_image():
    """测试图片ASCII艺术生成"""
    print("=" * 60)
    print("测试 2: 生成ASCII艺术图片（使用绝对路径）")
    print("=" * 60)
    
    # 获取绝对路径
    abs_path = Path("scan_test.jpg").absolute()
    
    result = await generate_ascii_image(
        image_path=str(abs_path),
        width=100,
        charset="detailed",
        color_mode="gray"
    )
    
    print(result)
    print()


async def test_custom_output():
    """测试自定义输出文件名（同目录）"""
    print("=" * 60)
    print("测试 3: 自定义输出文件名")
    print("=" * 60)
    
    # 获取绝对路径
    abs_path = Path("scan_test.jpg").absolute()
    
    result_txt = await generate_ascii_art(
        image_path=str(abs_path),
        output_path="custom_output.txt",  # 只提供文件名
        width=60,
        charset="blocks"
    )
    print(result_txt)
    
    result_img = await generate_ascii_image(
        image_path=str(abs_path),
        output_path="custom_output.png",  # 只提供文件名
        width=80,
        charset="minimal"
    )
    print(result_img)
    print()


async def test_path_restrictions():
    """测试路径限制"""
    print("=" * 60)
    print("测试 4: 路径限制验证")
    print("=" * 60)
    
    # 测试相对路径（应该失败）
    print("4.1 测试相对路径（应该被拒绝）：")
    result = await generate_ascii_art(
        image_path="scan_test.jpg",  # 相对路径
        width=50
    )
    print(result)
    print()
    
    # 测试输出路径包含目录（应该失败）
    print("4.2 测试输出路径包含目录（应该被拒绝）：")
    abs_path = Path("scan_test.jpg").absolute()
    result = await generate_ascii_image(
        image_path=str(abs_path),
        output_path="output/test.png",  # 包含路径
        width=50
    )
    print(result)
    print()


async def main():
    """运行所有测试"""
    # 检查测试图片是否存在
    if not Path("scan_test.jpg").exists():
        print("错误: 找不到 scan_test.jpg 测试图片")
        print("请确保 scan_test.jpg 在当前目录中")
        return
    
    print("\n开始测试 ASCII Art MCP Server\n")
    
    await test_ascii_art()
    await test_ascii_image()
    await test_custom_output()
    await test_path_restrictions()
    
    print("=" * 60)
    print("所有测试完成！")
    print("=" * 60)
    print("\n生成的文件（在 scan_test.jpg 同目录下）：")
    print("- scan_test_ascii.txt")
    print("- scan_test_ascii.png")
    print("- custom_output.txt")
    print("- custom_output.png")
    print("\n路径限制：")
    print("✅ 输入必须是绝对路径")
    print("✅ 输出只能是文件名，会保存在输入图片的同一目录")
    print("\n下一步:")
    print("1. 配置 Claude Desktop (参考 claude_config_example.md)")
    print("2. 重启 Claude Desktop")
    print("3. 在 Claude 中测试工具")


if __name__ == "__main__":
    asyncio.run(main())
