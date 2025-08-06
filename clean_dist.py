import os
import shutil

def get_dir_size(directory):
    """Recursively computes the size of a directory in bytes."""
    total = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except Exception:
                pass
    return total

def remove_except(dir_path, keep_files):
    """Remove all files in dir_path except those listed in keep_files."""
    removed_size = 0
    if not os.path.exists(dir_path):
        return removed_size
    for f in os.listdir(dir_path):
        if f not in keep_files:
            file_path = os.path.join(dir_path, f)
            try:
                if os.path.isdir(file_path):
                    removed_size += get_dir_size(file_path)
                    shutil.rmtree(file_path)
                else:
                    removed_size += os.path.getsize(file_path)
                    os.remove(file_path)
            except Exception:
                pass
    return removed_size

def remove_unwanted_files(dir_path, keep_keywords, ext=None):
    """Remove files not matching keywords or extension, return total removed size."""
    removed_size = 0
    if not os.path.exists(dir_path):
        return removed_size
    for f in os.listdir(dir_path):
        keep = any(kw in f for kw in keep_keywords)
        if ext and not f.endswith(ext):
            keep = False
        if not keep:
            file_path = os.path.join(dir_path, f)
            try:
                removed_size += os.path.getsize(file_path)
                os.remove(file_path)
            except Exception:
                pass
    return removed_size

def remove_unwanted_translations(trans_dir, keep_langs=("zh_CN", "en")):
    """Only keep .qm translation files for specified languages."""
    removed_size = 0
    if not os.path.exists(trans_dir):
        return removed_size
    for f in os.listdir(trans_dir):
        if not any(f.endswith(f"{lang}.qm") for lang in keep_langs):
            try:
                file_path = os.path.join(trans_dir, f)
                removed_size += os.path.getsize(file_path)
                os.remove(file_path)
            except Exception:
                pass
    return removed_size

def remove_unwanted_locales(locales_dir, keep_langs=("zh-CN", "en-US")):
    """Only keep .pak locale files for specified languages in qtwebengine_locales."""
    removed_size = 0
    if not os.path.exists(locales_dir):
        return removed_size
    for f in os.listdir(locales_dir):
        if not any(f.startswith(lang) for lang in keep_langs):
            try:
                file_path = os.path.join(locales_dir, f)
                removed_size += os.path.getsize(file_path)
                os.remove(file_path)
            except Exception:
                pass
    return removed_size

def clean_dist(dist_dir):
    print(f"开始清理: {dist_dir}")
    before = get_dir_size(dist_dir)
    total_removed = 0

    # 保留必要的平台插件
    platforms_dir = os.path.join(dist_dir, "PySide6", "Qt", "plugins", "platforms")
    total_removed += remove_except(platforms_dir, ["libqcocoa.dylib"])

    # 保留用到的图片格式插件
    imageformats_dir = os.path.join(dist_dir, "PySide6", "Qt", "plugins", "imageformats")
    keep_imageformats = ["libqjpeg.dylib", "libqpng.dylib"]
    total_removed += remove_except(imageformats_dir, keep_imageformats)

    # 精简其它插件
    plugins_dir = os.path.join(dist_dir, "PySide6", "Qt", "plugins")
    for subdir in os.listdir(plugins_dir):
        if subdir not in ["platforms", "imageformats"]:
            target = os.path.join(plugins_dir, subdir)
            if os.path.isdir(target):
                total_removed += get_dir_size(target)
                shutil.rmtree(target)

    # 保留 webengine 必要文件
    # 若文件分布在其它目录请自行补充
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
                    total_removed += os.path.getsize(path)
                    os.remove(path)
                except Exception:
                    pass

    # 精简 qtwebengine_locales 指定语言
    locales_dir = os.path.join(dist_dir, "qtwebengine_locales")
    total_removed += remove_unwanted_locales(locales_dir, ("zh-CN", "en-US"))

    # 精简 translations 指定语言
    translations_dir = os.path.join(dist_dir, "PySide6", "Qt", "translations")
    total_removed += remove_unwanted_translations(translations_dir, ("zh_CN", "en"))

    # 精简字体
    fonts_dir = os.path.join(dist_dir, "PySide6", "Qt", "lib", "fonts")
    if os.path.exists(fonts_dir):
        keep_fonts = ["DroidSansFallback.ttf"]
        total_removed += remove_except(fonts_dir, keep_fonts)

    after = get_dir_size(dist_dir)
    reduced = before - after
    print(f"清理前大小: {before/1024/1024:.2f} MB")
    print(f"清理后大小: {after/1024/1024:.2f} MB")
    print(f"本次共清理: {reduced/1024/1024:.2f} MB（约{reduced/1024:.0f} KB）")
    if reduced < 1024*1024:
        print("提示：本次清理量较少，可能原因：")
        print("1. 目录结构不符合预期，请检查 dist 目录结构。")
        print("2. 已经没有可清理的无用文件。")
        print("3. 请根据你的实际项目和依赖进一步完善保留文件列表。")

if __name__ == "__main__":
    # 修改此处路径为你的macOS打包输出（dist）目录
    dist_path = "dist/markrender.app/Contents/Resources"
    clean_dist(dist_path)
