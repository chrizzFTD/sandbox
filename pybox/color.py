def get_color_lightness(rgb, light):
    r, g, b = rgb
    h, l, s = colorsys.rgb_to_hls(r / 255., g / 255., b / 255.)
    return tuple(i * 255 for i in colorsys.hls_to_rgb(h, light, s))


def rgb2hex(rgb):
    def clamp(x):
        return max(0, min(x, 255))

    return '{0:02x}{1:02x}{2:02x}'.format(*map(clamp, rgb))


def blendColors(start, end, percent):
    def _blend(first, second):
        step = float(second) - float(first)
        added = step / 100 * percent
        return first + added

    return tuple(_blend(*x) for x in zip(start, end))