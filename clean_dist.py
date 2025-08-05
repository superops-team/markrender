import os
import shutil

def remove_except(dir_path, keep_files):
    """
    Remove all files in dir_path except those listed in keep_files.
    """
    if not os.path.exists(dir_path):
        return
    for f in os.listdir(dir_path):
        if f not in keep_files:
            file_path = os.path.join(dir_path, f)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)

def remove_unwanted_translations(trans_dir, keep_langs=("zh_CN", "en")):
    """
    Only keep .qm translation files for specified languages.
    """
    if not os.path.exists(trans_dir):
        return
    for f in os.listdir(trans_dir):
        if not any(f.endswith(f"{lang}.qm") for lang in keep_langs):
            os.remove(os.path.join(trans_dir, f))

def remove_unwanted_locales(locales_dir, keep_langs=("zh-CN", "en-US")):
    """
    Only keep .pak locale files for specified languages in qtwebengine_locales.
    """
    if not os.path.exists(locales_dir):
        return
    for f in os.listdir(locales_dir):
        if not any(f.startswith(lang) for lang in keep_langs):
            os.remove(os.path.join(locales_dir, f))

def clean_dist(dist_dir):
    # 1. 保留必要的平台插件
    platforms_dir = os.path.join(dist_dir, "PySide6", "Qt", "plugins", "platforms")
    remove_except(platforms_dir, ["libqcocoa.dylib"])

    # 2. 保留用到的图片格式插件
    imageformats_dir = os.path.join(dist_dir, "PySide6", "Qt", "plugins", "imageformats")
    keep_imageformats = ["libqjpeg.dylib", "libqpng.dylib"]  # 只保留jpeg和png，如需其它请补充
    remove_except(imageformats_dir, keep_imageformats)

    # 3. 保留webengine必要文件
    # 这些文件通常在 PySide6/Qt/lib 或 dist 根目录或其子目录
    webengine_files = [
        "QtWebEngineProcess",
        "resources.pak",
        "icudtl.dat",
        "qtwebengine_devtools_resources.pak",
        "qtwebengine_resources.pak",
        "qtwebengine_resources_100p.pak",
        "qtwebengine_resources_200p.pak",
    ]
    for f in os.listdir(dist_dir):
        if f.startswith("qtwebengine_locales"):
            continue
        if f not in webengine_files and "QtWebEngine" not in f and not f.endswith(".so") and not f.endswith(".dylib"):
            path = os.path.join(dist_dir, f)
            if os.path.isfile(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

    # 4. 保留 qtwebengine_locales 指定语言
    locales_dir = os.path.join(dist_dir, "qtwebengine_locales")
    remove_unwanted_locales(locales_dir, ("zh-CN", "en-US"))

    # 5. 保留 translations 指定语言
    translations_dir = os.path.join(dist_dir, "PySide6", "Qt", "translations")
    remove_unwanted_translations(translations_dir, ("zh_CN", "en"))

    # 6. 删除无用的 PySide6/Qt/plugins 其它子目录
    plugins_dir = os.path.join(dist_dir, "PySide6", "Qt", "plugins")
    for subdir in os.listdir(plugins_dir):
        if subdir not in ["platforms", "imageformats"]:
            target = os.path.join(plugins_dir, subdir)
            if os.path.isdir(target):
                shutil.rmtree(target)

    # 7. 删除无用字体
    fonts_dir = os.path.join(dist_dir, "PySide6", "Qt", "lib", "fonts")
    if os.path.exists(fonts_dir):
        # 只保留常用字体，可根据需求调整
        keep_fonts = ["DroidSansFallback.ttf"]
        for f in os.listdir(fonts_dir):
            if f not in keep_fonts:
                os.remove(os.path.join(fonts_dir, f))

if __name__ == "__main__":
    # 修改此处路径为你的macOS打包输出（dist）目录
    dist_path = "dist/markrender.app/Contents/Resources"
    clean_dist(dist_path)
    print("Clean done.")