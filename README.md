# OCRanswer

一个基于屏幕截图、PaddleOCR 和 DeepSeek API 的桌面 OCR 问答助手。程序运行后会让用户框选屏幕区域，持续识别该区域中的文字；当 OCR 文本发生明显变化时，自动把识别结果发送给 DeepSeek，并在右下角悬浮窗中显示回答。

## 功能特点

- 屏幕区域框选：启动后用鼠标拖拽选择需要监控的屏幕区域。
- 自动 OCR：通过 PaddleOCR 识别选区内的中文内容。
- 文本变化检测：使用相似度阈值避免重复请求同一段内容。
- DeepSeek 问答：调用兼容 OpenAI SDK 的 DeepSeek API 获取答案。
- 悬浮窗显示：无边框、置顶、鼠标穿透的 PyQt6 悬浮窗口展示状态和结果。
- 快捷键控制：`F8` 重新框选区域，`Esc` 退出程序。
- 本地日志：OCR 内容、回答和异常会写入 `logs/YYYY-MM-DD.log`。

## 运行环境

建议环境：

- Windows 10/11
- Python 3.10 或 3.11
- DeepSeek API Key

主要依赖：

- `PyQt6`
- `paddleocr`
- `paddlepaddle`
- `dxcam`
- `pynput`
- `openai`

> `dxcam` 主要面向 Windows 桌面截图场景；PaddleOCR 首次运行时可能会下载 OCR 模型文件。

## 安装

1. 克隆项目或进入当前项目目录：

2. 创建并激活虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3. 安装依赖：

```powershell
python -m pip install --upgrade pip
pip install PyQt6 paddleocr paddlepaddle dxcam pynput openai
```

如果 PaddleOCR 安装或运行失败，优先检查 `paddlepaddle` 是否与当前 Python 版本匹配。

## 配置

编辑项目根目录下的 `config.json`：

```json
{
    "api_key": "your_deepseek_apikey",
    "base_url": "https://api.deepseek.com",
    "model": "deepseek-v4-flash",
    "ocr_interval": 1,
    "cooldown_after_answer": 2,
    "similarity_threshold": 0.95,
    "region": {
        "left": 346,
        "top": 259,
        "width": 811,
        "height": 670
    }
}
```

配置项说明：

| 字段 | 说明 |
| --- | --- |
| `api_key` | DeepSeek API Key|
| `base_url` | DeepSeek API 地址 |
| `model` | 调用模型名称 |
| `ocr_interval` | OCR 轮询间隔，单位为秒。 |
| `cooldown_after_answer` | 每次回答后的冷却时间，单位为秒。 |
| `similarity_threshold` | 文本相似度阈值|
| `region` | 最近一次框选的屏幕区域。启动时会重新框选并覆盖该值。 |

## 启动

```powershell
python main.py
```

启动后按以下流程使用：

1. 屏幕变暗后，用鼠标拖拽框选需要监控的区域。
2. 程序在右下角显示悬浮窗。
3. 当选区内文本变化并且 OCR 结果长度足够时，程序会调用 DeepSeek。
4. 回答会显示在悬浮窗中，同时写入 `logs/` 目录。

## 快捷键

| 快捷键 | 功能 |
| --- | --- |
| `F8` | 暂停识别并重新框选监控区域。 |
| `Esc` | 退出程序。 |

## 项目结构

```text
DeepSeek_OCR_Agent_V1/
├── main.py                  # 程序入口，负责初始化 UI、OCR、截图、热键和工作线程
├── config.json              # API、模型、轮询间隔、相似度阈值和屏幕区域配置
├── core/
│   ├── deepseek_client.py    # DeepSeek/OpenAI SDK 调用封装
│   ├── logger.py             # 日志写入
│   ├── ocr_engine.py         # PaddleOCR 识别封装
│   ├── screen_capture.py     # dxcam 屏幕截图
│   └── text_detector.py      # OCR 文本变化检测
├── ui/
│   ├── hotkey_manager.py     # F8 和 Esc 快捷键监听
│   ├── overlay_window.py     # 右下角悬浮窗
│   └── region_selector.py    # 全屏框选区域组件
└── logs/
    └── YYYY-MM-DD.log        # 运行日志
```

## 工作流程

```text
启动程序
  ↓
框选屏幕监控区域
  ↓
dxcam 截图
  ↓
PaddleOCR 识别文字
  ↓
TextDetector 判断文本是否变化
  ↓
DeepSeekClient 请求模型回答
  ↓
悬浮窗显示结果并写入日志
```

## 日志

程序会把每次有效 OCR、模型回答和异常写入 `logs/YYYY-MM-DD.log`。日志格式大致如下：

```text
2026-06-05 12:00:00
OCR:
识别到的文本
ANSWER:
模型回答
----------------------------------------
```
