import os
import subprocess

def is_object_or_static(file_path):
    return file_path.endswith(('.o', '.a'))

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except Exception:
        return 0

def get_shared_libs(file_path):
    """Return a set of shared library paths that the binary depends on."""
    result = set()
    try:
        out = subprocess.check_output(["otool", "-L", file_path], stderr=subprocess.DEVNULL).decode("utf-8")
        for line in out.splitlines()[1:]:
            lib = line.strip().split(" ")[0]
            if lib and (lib.endswith(".dylib") or "/" in lib):
                result.add(lib)
    except Exception:
        pass
    return result

def collect_binaries(root_dir, exts=('.dylib', '', '.so', '.dll', '.exe')):
    """Collect all binary files under root_dir with given extensions."""
    binaries = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(exts) or (os.access(os.path.join(dirpath, f), os.X_OK) and '.' not in f):
                binaries.append(os.path.join(dirpath, f))
    return binaries

def classify_files(root_dir, must_have_libs=set(), optional_libs=set()):
    stats = {
        "must_have": {"size": 0, "files": []},
        "optional": {"size": 0, "files": []},
        "object_static": {"size": 0, "files": []},
        "non_object_static": {"size": 0, "files": []},
        "other": {"size": 0, "files": []},
    }

    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(file_path, root_dir)
            size = get_file_size(file_path)
            if is_object_or_static(file_path):
                stats["object_static"]["size"] += size
                stats["object_static"]["files"].append((rel_path, size))
            else:
                stats["non_object_static"]["size"] += size
                stats["non_object_static"]["files"].append((rel_path, size))
            # Classify binaries against must/optional libs
            if f in must_have_libs:
                stats["must_have"]["size"] += size
                stats["must_have"]["files"].append((rel_path, size))
            elif f in optional_libs:
                stats["optional"]["size"] += size
                stats["optional"]["files"].append((rel_path, size))
            else:
                stats["other"]["size"] += size
                stats["other"]["files"].append((rel_path, size))
    return stats

def analyze_binary_deps(root_dir, must_have_libs=None, optional_libs=None):
    if must_have_libs is None:
        must_have_libs = {
            'QtWebEngineProcess', 'icudtl.dat', 'resources.pak',
            'qtwebengine_devtools_resources.pak', 'qtwebengine_resources.pak',
            'qtwebengine_resources_100p.pak', 'qtwebengine_resources_200p.pak',
            'libqcocoa.dylib', 'libqjpeg.dylib', 'libqpng.dylib',
            'DroidSansFallback.ttf', 'qtbase_en.qm', 'qtbase_zh_CN.qm',
            'en-US.pak', 'zh-CN.pak'
        }
    if optional_libs is None:
        optional_libs = {
            'libqtiff.dylib', 'libqgif.dylib', 'libqwebp.dylib', 'libqminimal.dylib'
        }

    # Collect all binaries
    binaries = collect_binaries(root_dir, exts=('.dylib', '.so', '.dll', '.exe', ''))
    dep_map = {}
    all_deps = set()
    for binary in binaries:
        deps = get_shared_libs(binary)
        dep_map[os.path.relpath(binary, root_dir)] = deps
        all_deps.update(deps)

    # Classify files and compute stats
    stats = classify_files(root_dir, must_have_libs, optional_libs)

    # Print summary
    def humanize(n):
        for unit in ['B','KB','MB','GB','TB']:
            if n < 1024:
                return f"{n:.2f} {unit}"
            n /= 1024
        return f"{n:.2f} PB"

    print("==== 二进制依赖分析报告 ====")
    print("\n[依赖关系]")
    for binary, deps in dep_map.items():
        print(f"{binary}:")
        for dep in deps:
            print(f"  -> {dep}")

    print("\n[分类统计]")
    for cat in ['must_have', 'optional', 'object_static', 'non_object_static', 'other']:
        sz = stats[cat]['size']
        files = stats[cat]['files']
        print(f"- {cat}: {humanize(sz)}，文件数: {len(files)}")

    print("\n[对象/静态文件列表]")
    for rel, size in sorted(stats["object_static"]["files"], key=lambda x: -x[1])[:10]:
        print(f"  {rel}: {humanize(size)}")

    print("\n[非对象/静态文件列表]")
    for rel, size in sorted(stats["non_object_static"]["files"], key=lambda x: -x[1])[:10]:
        print(f"  {rel}: {humanize(size)}")

    print("\n[必须依赖文件列表]")
    for rel, size in sorted(stats["must_have"]["files"], key=lambda x: -x[1])[:10]:
        print(f"  {rel}: {humanize(size)}")

    print("\n[可选依赖文件列表]")
    for rel, size in sorted(stats["optional"]["files"], key=lambda x: -x[1])[:10]:
        print(f"  {rel}: {humanize(size)}")

    print("\n[其它文件列表]")
    for rel, size in sorted(stats["other"]["files"], key=lambda x: -x[1])[:10]:
        print(f"  {rel}: {humanize(size)}")

if __name__ == "__main__":
    # 修改此路径为你的二进制包根目录
    dist_path = "dist/markrender.app/Contents/Resources"
    analyze_binary_deps(dist_path)