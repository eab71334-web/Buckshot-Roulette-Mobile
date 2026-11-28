# Turns the checked out project into the light 32-bit Android build.
# Run only on the build machine, after the 64-bit builds are finished.
import re as _re

def _read(path):
    return open(path, encoding="utf-8").read()

def _write(path, text):
    open(path, "w", encoding="utf-8").write(text)

def edit(path, old, new):
    text = _read(path)
    assert text.count(old) == 1, (path, old, text.count(old))
    _write(path, text.replace(old, new))

def ensure(path, key, value, section="[rendering]"):
    """Set key=value under section. Replaces existing or appends after section header."""
    text = _read(path)
    pattern = r'(?m)^' + _re.escape(key) + r'\s*=.*$'
    full = key + "=" + value
    if _re.search(pattern, text):
        text = _re.sub(pattern, full, text, count=1)
    else:
        # Insert right after the section header line
        text = _re.sub(
            r'(' + _re.escape(section) + r'\n)',
            r'\1' + full + '\n',
            text, count=1)
    _write(path, text)

# ── project.godot ──────────────────────────────────────────────────────────────
# Vulkan is missing on most 32-bit phones: use OpenGL ES 3 renderer,
# draw at lower resolution, and use smaller shadow maps.
ensure("project.godot", 'renderer/rendering_method.mobile', '"gl_compatibility"')
ensure("project.godot", 'lights_and_shadows/directional_shadow/size.mobile', '512')
ensure("project.godot", 'lights_and_shadows/positional_shadow/atlas_size.mobile', '512')
ensure("project.godot", 'scaling_3d/scale', '0.7')
ensure("project.godot", 'anti_aliasing/quality/msaa_3d', '0')

# ── export_presets.cfg ─────────────────────────────────────────────────────────
# armeabi-v7a is already enabled in the base preset; only disable arm64 for the
# pure-32-bit build so the APK contains only the armeabi-v7a library.
edit("export_presets.cfg", "architectures/arm64-v8a=true", "architectures/arm64-v8a=false")
