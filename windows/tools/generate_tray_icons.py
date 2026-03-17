from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "20min20s" / "Resources"
SIZES = [16, 20, 24, 32, 40, 48, 64, 128, 256]


def _rounded_background(draw, size, color):
    inset = size * 0.08
    radius = size * 0.28
    draw.rounded_rectangle(
        [inset, inset, size - inset, size - inset],
        radius=radius,
        fill=color,
    )


def _eye_points(size):
    return [
        (size * 0.20, size * 0.52),
        (size * 0.35, size * 0.33),
        (size * 0.50, size * 0.26),
        (size * 0.65, size * 0.33),
        (size * 0.80, size * 0.52),
        (size * 0.65, size * 0.69),
        (size * 0.50, size * 0.76),
        (size * 0.35, size * 0.69),
    ]


def _draw_open_eye(draw, size, iris_color):
    draw.polygon(_eye_points(size), fill=(255, 255, 255, 255))
    iris_r = size * 0.11
    iris_c = (size * 0.50, size * 0.52)
    draw.ellipse(
        [
            iris_c[0] - iris_r,
            iris_c[1] - iris_r,
            iris_c[0] + iris_r,
            iris_c[1] + iris_r,
        ],
        fill=iris_color,
    )
    pupil_r = size * 0.045
    draw.ellipse(
        [
            iris_c[0] - pupil_r,
            iris_c[1] - pupil_r,
            iris_c[0] + pupil_r,
            iris_c[1] + pupil_r,
        ],
        fill=(15, 23, 42, 255),
    )
    shine_r = size * 0.018
    draw.ellipse(
        [
            iris_c[0] - iris_r * 0.28,
            iris_c[1] - iris_r * 0.45,
            iris_c[0] - iris_r * 0.28 + shine_r * 2,
            iris_c[1] - iris_r * 0.45 + shine_r * 2,
        ],
        fill=(255, 255, 255, 220),
    )


def _draw_closed_eye(draw, size):
    width = max(2, int(size * 0.07))
    draw.arc(
        [size * 0.24, size * 0.36, size * 0.78, size * 0.70],
        start=200,
        end=340,
        fill=(255, 255, 255, 255),
        width=width,
    )
    lash_y = size * 0.53
    for offset in (0.36, 0.48, 0.60):
        x = size * offset
        draw.line(
            [(x, lash_y), (x - size * 0.025, lash_y - size * 0.07)],
            fill=(255, 255, 255, 220),
            width=max(1, int(size * 0.035)),
        )


def _draw_sleep_marks(draw, size):
    width = max(2, int(size * 0.05))
    z1 = [
        (size * 0.61, size * 0.24),
        (size * 0.73, size * 0.24),
        (size * 0.61, size * 0.35),
        (size * 0.73, size * 0.35),
    ]
    z2 = [
        (size * 0.69, size * 0.12),
        (size * 0.79, size * 0.12),
        (size * 0.69, size * 0.21),
        (size * 0.79, size * 0.21),
    ]
    for points in (z1, z2):
        draw.line(points[:2], fill=(255, 255, 255, 255), width=width)
        draw.line(points[1:3], fill=(255, 255, 255, 255), width=width)
        draw.line(points[2:4], fill=(255, 255, 255, 255), width=width)


def _draw_attention_badge(draw, size):
    badge = [size * 0.66, size * 0.14, size * 0.88, size * 0.36]
    draw.ellipse(badge, fill=(255, 244, 214, 255))
    draw.rounded_rectangle(
        [size * 0.755, size * 0.18, size * 0.785, size * 0.28],
        radius=size * 0.015,
        fill=(220, 38, 38, 255),
    )
    draw.ellipse(
        [size * 0.755, size * 0.295, size * 0.785, size * 0.325],
        fill=(220, 38, 38, 255),
    )


def _draw_pause_slash(draw, size):
    width = max(2, int(size * 0.08))
    draw.line(
        [(size * 0.28, size * 0.76), (size * 0.76, size * 0.28)],
        fill=(255, 247, 237, 255),
        width=width,
    )


def render_active(size):
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    _rounded_background(draw, size, (13, 148, 136, 255))
    _draw_open_eye(draw, size, (20, 184, 166, 255))
    draw.ellipse(
        [size * 0.68, size * 0.18, size * 0.84, size * 0.34],
        fill=(255, 245, 157, 255),
    )
    return image


def render_disabled(size):
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    _rounded_background(draw, size, (217, 119, 6, 255))
    _draw_open_eye(draw, size, (146, 64, 14, 255))
    _draw_pause_slash(draw, size)
    return image


def render_sleeping(size):
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    _rounded_background(draw, size, (79, 70, 229, 255))
    _draw_closed_eye(draw, size)
    _draw_sleep_marks(draw, size)
    return image


def render_pending(size):
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    _rounded_background(draw, size, (220, 38, 38, 255))
    _draw_open_eye(draw, size, (251, 191, 36, 255))
    _draw_attention_badge(draw, size)
    return image


def save_icon(name, renderer):
    largest = max(SIZES)
    image = renderer(largest)
    image.save(RESOURCES / f"{name}.ico", sizes=[(size, size) for size in SIZES])


def main():
    save_icon("sunglasses", render_active)
    save_icon("dizzy", render_disabled)
    save_icon("sleeping", render_sleeping)
    save_icon("overheated", render_pending)
    print("Tray icons regenerated.")


if __name__ == "__main__":
    main()
