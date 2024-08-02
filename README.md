# PDFRenamer
PDF识别重命名工具 (PDFRenamer) 是一个用于处理 PDF 文件、提取订单号码并重命名文件的工具。该工具使用 Baidu OCR API 来进行文本识别，并支持多种正则表达式模式来提取订单号码。

## 特性
* 批量处理 PDF 文件
* 提取订单号码并重命名文件
* 支持多种正则表达式模式
* 自动处理文件名冲突

## 安装
1. 克隆或下载此项目到本地：
```angular2html
git clone https://github.com/yourusername/OrderPDFRenamer.git
cd OrderPDFRenamer
```
2. 安装所需的 Python 库：
```angular2html
pip install -r requirements.txt
```

## 配置
确保你有 Baidu OCR API 的 API Key 和 Secret Key，并在命令行参数中提供它们。

## 使用
在命令行中运行以下命令来处理 PDF 文件夹：
```angular2html
python pdf_renamer.py -f <folder_path> -p <patterns> -a <api_key> -s <secret_key> -d <dpi>
```

## 参数说明
* -f, --folder_path：包含 PDF 文件的文件夹路径（默认：.\pdf）
* -p, --patterns：用于提取订单号码的正则表达式模式列表（默认：['订单号码([a-zA-Z0-9]+)', 'CG[a-zA-Z0-9]{10}', 'CG[a-zA-Z0-9]{8}']）
* -a, --api_key：Baidu OCR API 的 API Key
* -s, --secret_key：Baidu OCR API 的 Secret Key
* -d, --dpi：用于图像提取的 DPI（默认：175）

## 示例
```angular2html
python pdf_renamer.py -f "E:\Projects\code\Python\pdf\dist\pdf" -p "订单号码([a-zA-Z0-9]+)" "CG[a-zA-Z0-9]{10}" "CG[a-zA-Z0-9]{8}" -a "api_key" -s "secret_key" -d 175
```

## 贡献
欢迎贡献者！如果你有任何改进建议或发现了问题，请提交 issue 或 pull request。

## 许可证
此项目使用 MIT 许可证。详见 LICENSE 文件。