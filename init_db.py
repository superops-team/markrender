import os
from db_manager import ThemeManager

# 基础样式：代码高亮和一级标题样式
base_style = """
<style>
    /* 一级标题居中并设置颜色 */
    h1 {
        text-align: center;
        color: #333333;
    }

    /* 代码高亮样式 */
    pre {
        background-color: #f6f8fa;
        border-radius: 3px;
        font-size: 85%;
        line-height: 1.45;
        overflow: auto;
        padding: 16px;
    }

    code {
        background-color: rgba(27,31,35,.05);
        border-radius: 3px;
        font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
        font-size: 85%;
        margin: 0;
        padding: 0.2em 0.4em;
    }

    /* 代码块高亮 */
    .hljs {
        display: block;
        overflow-x: auto;
        padding: 0.5em;
        color: #333;
        background: #f8f8f8;
    }

    /* 不同语言高亮样式 */
    .language-python .hljs-keyword { color: #0000FF; }
    .language-python .hljs-string { color: #008000; }
    .language-python .hljs-number { color: #0000CD; }
    .language-python .hljs-comment { color: #808080; }

    .language-javascript .hljs-keyword { color: #0000FF; }
    .language-javascript .hljs-string { color: #008000; }
    .language-javascript .hljs-number { color: #0000CD; }
    .language-javascript .hljs-comment { color: #808080; }

    .language-html .hljs-tag { color: #000080; }
    .language-html .hljs-attr { color: #FF0000; }
    .language-html .hljs-string { color: #008000; }

    .language-css .hljs-selector-tag { color: #000080; }
    .language-css .hljs-property { color: #FF0000; }
    .language-css .hljs-value { color: #008000; }
</style>
"""

# 主题样式
themes = {
    "默认样式": """<style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; }
        h2 { border-bottom: 1px solid #eaecef; }
        blockquote { border-left: 0.25em solid #dfe2e5; padding: 0 1em; color: #6a737d; }
        table { border-collapse: collapse; }
        th, td { border: 1px solid #dfe2e5; padding: 6px 13px; }
    </style>""",
    "GitHub风格": """<style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; }
        h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; }
        blockquote { border-left: 0.25em solid #dfe2e5; padding: 0 1em; color: #6a737d; }
        table { border-collapse: collapse; }
        th, td { border: 1px solid #dfe2e5; padding: 6px 13px; }
    </style>""",
    "浅色主题": """<style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f9f9f9;
            color: #333;
        }
        h2 { color: #1a1a1a; border-bottom: 1px solid #ddd; }
        blockquote { border-left: 3px solid #666; color: #555; }
        table { border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 6px 13px; }
    </style>""",
    "深色主题": """<style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #2d2d2d;
            color: #e9e9e9;
        }
        h2 { color: #fff; border-bottom: 1px solid #444; }
        blockquote { border-left: 3px solid #777; color: #bbb; }
        a { color: #61afef; }
        table { border-collapse: collapse; }
        th, td { border: 1px solid #444; padding: 6px 13px; }
    </style>""",
    "文档风格": """<style>
        body {
            font-family: 'Times New Roman', Times, serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h2 { font-family: Arial, sans-serif; font-size: 22px; }
        blockquote { font-style: italic; }
        table { border-collapse: collapse; }
        th, td { border: 1px solid #ccc; padding: 6px 13px; }
    </style>""",
}


def run(db_path='markrender.db'):
    if not db_path:
        home_dir = os.path.expanduser('~')
        markrender_dir = os.path.join(home_dir, '.markrender')
        os.makedirs(markrender_dir, exist_ok=True)
        db_path = os.path.join(markrender_dir, db_path)
    manager = ThemeManager(db_path)
    for name, theme_style in themes.items():
        if manager.theme_exists(name):
            continue
        full_style = base_style + theme_style
        manager.create_theme(name, full_style)


if __name__ == "__main__":
    run()
