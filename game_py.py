import math
import random
import sys
import pygame

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60
WORLD_WIDTH = 5200

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Jelajah Alam Bengkulu Selatan")
clock = pygame.time.Clock()

font_title = pygame.font.Font(None, 28)
font_sub = pygame.font.Font(None, 20)
font_badge = pygame.font.Font(None, 18)
font_spot_tag = pygame.font.Font(None, 19)
font_card_title = pygame.font.Font(None, 26)
font_card_body = pygame.font.Font(None, 20)
font_btn = pygame.font.Font(None, 19)


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
    )


ATMOSPHERES = {
    "pagi": {
        "label": "Pagi",
        "sky_top": (48, 156, 210),
        "sky_mid": (132, 214, 222),
        "sky_bot": (228, 245, 224),
        "sun_color": (255, 248, 198),
        "glow_color": (255, 236, 150),
        "far_mtn": (72, 139, 155),
        "mid_hill": (44, 122, 108),
        "ground": (216, 195, 158),
        "water_top": (20, 145, 181),
        "stars": 0.0,
        "fireflies": 0.15,
    },
    "senja": {
        "label": "Senja",
        "sky_top": (36, 33, 79),
        "sky_mid": (194, 79, 92),
        "sky_bot": (252, 176, 86),
        "sun_color": (255, 196, 92),
        "glow_color": (255, 130, 70),
        "far_mtn": (84, 71, 110),
        "mid_hill": (52, 78, 92),
        "ground": (199, 154, 123),
        "water_top": (184, 93, 104),
        "stars": 0.25,
        "fireflies": 0.5,
    },
    "malam": {
        "label": "Malam",
        "sky_top": (6, 15, 31),
        "sky_mid": (13, 38, 64),
        "sky_bot": (23, 68, 86),
        "sun_color": (235, 246, 255),
        "glow_color": (148, 210, 255),
        "far_mtn": (20, 44, 66),
        "mid_hill": (17, 59, 61),
        "ground": (59, 77, 84),
        "water_top": (14, 71, 94),
        "stars": 0.92,
        "fireflies": 0.95,
    },
}

ZONES = [
    {"id": "pasar_bawah", "name": "Pantai Pasar Bawah", "subtitle": "Kota Manna - Pesisir Samudra Hindia", "x_start": 0, "x_end": 1060, "center_x": 520, "terrain": "beach", "color": (34, 211, 238)},
    {"id": "bengkenang", "name": "Pantai Bengkenang", "subtitle": "Pesisir Berpasir & Cemara Laut", "x_start": 1060, "x_end": 2100, "center_x": 1580, "terrain": "beach", "color": (56, 189, 248)},
    {"id": "air_manna", "name": "Sungai Air Manna", "subtitle": "Aliran Jernih & Lubuk Larangan", "x_start": 2100, "x_end": 3140, "center_x": 2620, "terrain": "river", "color": (45, 212, 191)},
    {"id": "geluguran", "name": "Air Terjun Geluguran", "subtitle": "Ulu Manna - Gugusan Bukit Barisan", "x_start": 3140, "x_end": 4160, "center_x": 3650, "terrain": "waterfall", "color": (52, 211, 153)},
    {"id": "bukit_barisan", "name": "Hutan Rafflesia", "subtitle": "Kawasan Hutan Hujan Tropis Bengkulu Selatan", "x_start": 4160, "x_end": WORLD_WIDTH, "center_x": 4680, "terrain": "forest", "color": (251, 113, 133)},
]

SPOTS = [
    {"zone_name": "Pantai Pasar Bawah - Kota Manna", "category": "Pesisir & Samudra", "title": "Ombak & Karang Pasar Bawah", "x": 420, "y_offset": -14, "desc": "Garis pantai Pasar Bawah berhadapan langsung dengan Samudra Hindia dengan gulungan ombak dan buih putih.", "detail": "Angin laut bergerak konstan menyapu pasir dan batuan tepi pantai Kota Manna."},
    {"zone_name": "Pantai Pasar Bawah - Kota Manna", "category": "Kehidupan Pesisir", "title": "Perahu Pesisir Selatan", "x": 760, "y_offset": -22, "desc": "Perahu melaju mengikuti alun gelombang di perairan pesisir Bengkulu Selatan.", "detail": "Warna langit dan permukaan air berubah lembut dari pagi, senja, hingga malam."},
    {"zone_name": "Pantai Bengkenang - Bengkulu Selatan", "category": "Vegetasi Pesisir", "title": "Cemara & Pasir Bengkenang", "x": 1460, "y_offset": -28, "desc": "Hamparan pasir pesisir Bengkenang ditemani pepohonan yang bergoyang pelan diterpa angin.", "detail": "Vegetasi pesisir memberi naungan sekaligus menahan hembusan angin laut."},
    {"zone_name": "Pantai Bengkenang - Bengkulu Selatan", "category": "Satwa Pesisir", "title": "Burung di Langit Pantai", "x": 1810, "y_offset": -90, "desc": "Burung pesisir melayang dan mengepakkan sayap memanfaatkan arus udara hangat.", "detail": "Gerakan burung menambah nuansa hidup di atas garis pantai."},
    {"zone_name": "Sungai Air Manna - Bengkulu Selatan", "category": "Ekosistem Sungai", "title": "Aliran & Batu Air Manna", "x": 2480, "y_offset": -16, "desc": "Sungai Air Manna mengalirkan air tawar segar dengan bebatuan dan lubuk alami.", "detail": "Arus sungai terus mengalir membelah bebatuan di tepi dan dasar aliran."},
    {"zone_name": "Sungai Air Manna - Bengkulu Selatan", "category": "Perairan Tawar", "title": "Riak Lubuk Air Manna", "x": 2840, "y_offset": -12, "desc": "Permukaan air yang tenang memantulkan cahaya langit dan pepohonan sekitar.", "detail": "Kelestarian lubuk membantu menjaga kebersihan lingkungan sungai."},
    {"zone_name": "Air Terjun Geluguran - Ulu Manna", "category": "Bukit Barisan", "title": "Air Terjun Geluguran", "x": 3560, "y_offset": -78, "desc": "Air terjun mengalir turun dari tebing hijau perbukitan Ulu Manna dengan percikan sejuk.", "detail": "Hutan Bukit Barisan menjaga pasokan air sepanjang tahun."},
    {"zone_name": "Air Terjun Geluguran - Ulu Manna", "category": "Mikroklimat", "title": "Embun & Tebing Bukit", "x": 3890, "y_offset": -34, "desc": "Udara di sekitar air terjun terasa lebih sejuk akibat percikan air dan naungan pepohonan.", "detail": "Tumbuhan hijau tumbuh subur di area yang lembap."},
    {"zone_name": "Hutan Hujan Tropis - Bengkulu Selatan", "category": "Flora Tropis", "title": "Bunga Rafflesia", "x": 4540, "y_offset": -20, "desc": "Hutan tropis Bengkulu Selatan menjadi habitat flora langka Rafflesia berkelopak merah berbintik.", "detail": "Tumbuh bergantung pada tanaman inang di lantai hutan yang lembap."},
    {"zone_name": "Hutan Hujan Tropis - Bengkulu Selatan", "category": "Hutan Tropis", "title": "Daun Gugur & Cahaya Hutan", "x": 4880, "y_offset": -55, "desc": "Daun jatuh perlahan di bawah kanopi hutan dan cahaya lembut tampak saat senja atau malam.", "detail": "Kanopi hutan berlapis menciptakan suasana teduh dan asri."},
]

stars = [(random.random(), random.random() * 0.52, random.uniform(1.0, 2.3), random.uniform(0, math.tau)) for _ in range(60)]
birds = [{"base_x": 250 + i * 410 + random.uniform(0, 140), "base_y": 0.16 + (i % 4) * 0.055, "speed": random.uniform(22, 38), "wing_phase": random.uniform(0, math.tau), "scale": random.uniform(0.75, 1.2)} for i in range(10)]
leaves = [{"x": random.uniform(0, WORLD_WIDTH), "y_ratio": random.uniform(0.25, 0.72), "vy": random.uniform(18, 36), "sway_speed": random.uniform(1.5, 3.0), "sway_amp": random.uniform(16, 34), "phase": random.uniform(0, math.tau), "size": random.uniform(4, 7), "color": (74, 222, 128) if i % 2 == 0 else (250, 204, 21)} for i in range(24)]
fireflies = [{"x": random.uniform(0, WORLD_WIDTH), "y_ratio": random.uniform(0.35, 0.74), "phase": random.uniform(0, math.tau), "vx": random.uniform(-14, 14), "r": random.uniform(2.0, 3.8)} for _ in range(28)]


class ExplorerGame:
    def __init__(self):
        self.w, self.h = WIDTH, HEIGHT
        self.time_key = "pagi"
        self.atm = dict(ATMOSPHERES["pagi"])
        self.elapsed = 0.0

        # Posisi & fisika karakter + lompat
        self.player_x = 320.0
        self.player_y = 0.0  # tinggi di atas tanah (0 = menapak tanah, positif = melayang ke atas)
        self.player_vx = 0.0
        self.player_vy = 0.0
        self.facing = 1
        self.walk_cycle = 0.0
        self.speed = 330.0
        self.jump_velocity = 560.0
        self.gravity = 1480.0
        self.on_ground = True
        self.coyote_timer = 0.0
        self.jump_buffer_timer = 0.0
        self.dust_particles = []  # [x, y_above_ground, vx, vy, radius, life]

        self.camera_x = 0.0
        self.selected_spot = None
        self.hovered_spot = None
        self.time_buttons = []
        self.zone_buttons = []
        self.close_btn_rect = pygame.Rect(0, 0, 0, 0)
        self.prev_btn_rect = pygame.Rect(0, 0, 0, 0)
        self.next_btn_rect = pygame.Rect(0, 0, 0, 0)

    def ground_y(self):
        return int(self.h * 0.76)

    def clamp_camera(self, cam):
        return max(0.0, min(max(0.0, WORLD_WIDTH - self.w), cam))

    def spawn_dust(self, count=7, spread_vy=110.0):
        for _ in range(count):
            self.dust_particles.append([
                self.player_x + random.uniform(-10, 10),
                max(1.0, self.player_y),
                random.uniform(-75, 75) + self.player_vx * 0.15,
                random.uniform(25, spread_vy),
                random.uniform(2.5, 5.0),
                1.0,
            ])

    def trigger_jump(self):
        self.jump_buffer_timer = 0.14

    def warp_to_zone(self, zone):
        self.player_x = float(zone["center_x"])
        self.player_y = 0.0
        self.player_vx = 0.0
        self.player_vy = 0.0
        self.on_ground = True
        self.camera_x = self.clamp_camera(self.player_x - self.w * 0.38)

    def inspect_nearest_spot(self):
        self.selected_spot = min(range(len(SPOTS)), key=lambda i: abs(SPOTS[i]["x"] - self.player_x))

    def update_atmosphere(self, dt):
        target = ATMOSPHERES[self.time_key]
        t = min(1.0, dt * 3.5)
        for key in ("sky_top", "sky_mid", "sky_bot", "sun_color", "glow_color", "far_mtn", "mid_hill", "ground", "water_top"):
            self.atm[key] = lerp_color(self.atm[key], target[key], t)
        self.atm["stars"] = lerp(self.atm["stars"], target["stars"], t)
        self.atm["fireflies"] = lerp(self.atm["fireflies"], target["fireflies"], t)

    def update(self, dt):
        self.elapsed += dt
        self.update_atmosphere(dt)

        keys = pygame.key.get_pressed()
        move_dir = (-1 if (keys[pygame.K_LEFT] or keys[pygame.K_a]) else 0) + (1 if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) else 0)
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump_buffer_timer = max(self.jump_buffer_timer, 0.06)

        if move_dir != 0:
            self.facing = move_dir
            accel = 12.0 if self.on_ground else 7.5
            self.player_vx = lerp(self.player_vx, move_dir * self.speed, min(1.0, dt * accel))
            if self.on_ground:
                self.walk_cycle += dt * 10.5
        else:
            decel = 10.0 if self.on_ground else 3.0
            self.player_vx = lerp(self.player_vx, 0.0, min(1.0, dt * decel))
            if abs(self.player_vx) < 4:
                self.player_vx = 0.0

        self.player_x = max(80.0, min(WORLD_WIDTH - 80.0, self.player_x + self.player_vx * dt))

        # Coyote time & jump buffer
        if self.on_ground:
            self.coyote_timer = 0.10
        else:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)

        if self.jump_buffer_timer > 0.0:
            self.jump_buffer_timer = max(0.0, self.jump_buffer_timer - dt)

        if self.jump_buffer_timer > 0.0 and self.coyote_timer > 0.0:
            self.player_vy = self.jump_velocity
            self.on_ground = False
            self.coyote_timer = 0.0
            self.jump_buffer_timer = 0.0
            self.spawn_dust(count=8, spread_vy=95.0)

        # Gravitasi & posisi vertikal
        if not self.on_ground:
            # Sedikit variabel tinggi lompat jika tombol dilepas saat naik
            holding_jump = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]
            grav_mult = 1.0 if (holding_jump or self.player_vy < 0) else 1.45
            self.player_vy -= self.gravity * grav_mult * dt
            self.player_y += self.player_vy * dt

            if self.player_y <= 0.0:
                self.player_y = 0.0
                self.player_vy = 0.0
                self.on_ground = True
                self.spawn_dust(count=9, spread_vy=80.0)

        # Update partikel debu lompat/mendarat
        for dp in self.dust_particles:
            dp[0] += dp[2] * dt
            dp[1] = max(0.0, dp[1] + dp[3] * dt)
            dp[3] -= 260.0 * dt
            dp[5] -= dt * 2.4
        self.dust_particles = [dp for dp in self.dust_particles if dp[5] > 0.02]

        self.camera_x = lerp(self.camera_x, self.clamp_camera(self.player_x - self.w * 0.38), min(1.0, dt * 6.5))

        for b in birds:
            b["wing_phase"] += dt * 8.5

        gy = self.ground_y()
        for lf in leaves:
            lf["y_ratio"] += (lf["vy"] * dt) / max(1, gy)
            lf["phase"] += lf["sway_speed"] * dt
            if lf["y_ratio"] * gy > gy + 10:
                lf["y_ratio"] = 0.22 + random.uniform(0, 0.08)
                lf["x"] = self.camera_x + random.uniform(0, self.w)

        for ff in fireflies:
            ff["phase"] += dt * 2.4
            ff["x"] = (ff["x"] + ff["vx"] * dt) % WORLD_WIDTH

        mx, my = pygame.mouse.get_pos()
        self.hovered_spot = None
        for idx, spot in enumerate(SPOTS):
            if math.hypot(mx - (spot["x"] - self.camera_x), my - (gy + spot["y_offset"])) <= 36:
                self.hovered_spot = idx
                break

    def handle_event(self, event):
        global screen
        if event.type == pygame.VIDEORESIZE:
            self.w, self.h = max(800, event.w), max(520, event.h)
            screen = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE)
            self.camera_x = self.clamp_camera(self.camera_x)
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                self.trigger_jump()
            elif event.key in (pygame.K_e, pygame.K_RETURN):
                self.inspect_nearest_spot()
            elif event.key == pygame.K_ESCAPE:
                self.selected_spot = None
            elif event.key == pygame.K_1:
                self.time_key = "pagi"
            elif event.key == pygame.K_2:
                self.time_key = "senja"
            elif event.key == pygame.K_3:
                self.time_key = "malam"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.selected_spot is not None:
                if self.close_btn_rect.collidepoint(pos):
                    self.selected_spot = None
                    return
                if self.prev_btn_rect.collidepoint(pos):
                    self.selected_spot = (self.selected_spot - 1) % len(SPOTS)
                    self.player_x = max(120.0, min(WORLD_WIDTH - 120.0, SPOTS[self.selected_spot]["x"] - 55))
                    return
                if self.next_btn_rect.collidepoint(pos):
                    self.selected_spot = (self.selected_spot + 1) % len(SPOTS)
                    self.player_x = max(120.0, min(WORLD_WIDTH - 120.0, SPOTS[self.selected_spot]["x"] - 55))
                    return
            for rect, t_key in self.time_buttons:
                if rect.collidepoint(pos):
                    self.time_key = t_key
                    return
            for rect, zone in self.zone_buttons:
                if rect.collidepoint(pos):
                    self.warp_to_zone(zone)
                    return
            gy = self.ground_y()
            for idx, spot in enumerate(SPOTS):
                if math.hypot(pos[0] - (spot["x"] - self.camera_x), pos[1] - (gy + spot["y_offset"])) <= 38:
                    self.selected_spot = idx
                    return
            if gy - 160 <= pos[1] <= gy + 90:
                world_x = max(90.0, min(WORLD_WIDTH - 90.0, pos[0] + self.camera_x))
                self.facing = 1 if world_x >= self.player_x else -1
                self.player_x = world_x
                if self.on_ground:
                    self.walk_cycle += 0.7

    def draw_panel(self, surf, rect, radius=14, col=(12, 34, 46)):
        pygame.draw.rect(surf, col, rect, border_radius=radius)
        pygame.draw.rect(surf, (90, 130, 145), rect, width=1, border_radius=radius)

    def draw_sky(self, surf):
        for y in range(0, self.h, 2):
            r = y / max(1, self.h)
            col = lerp_color(self.atm["sky_top"], self.atm["sky_mid"], r / 0.55) if r < 0.55 else lerp_color(self.atm["sky_mid"], self.atm["sky_bot"], (r - 0.55) / 0.45)
            pygame.draw.rect(surf, col, (0, y, self.w, 2))

        if self.atm["stars"] > 0.05:
            for sx_r, sy_r, rad, tw in stars:
                sx = int(((sx_r * self.w - self.camera_x * 0.03) % self.w + self.w) % self.w)
                sy = int(sy_r * self.h)
                if 0.6 + 0.4 * math.sin(self.elapsed * 2.5 + tw) > 0.5:
                    pygame.draw.circle(surf, (255, 255, 255), (sx, sy), max(1, int(rad)))

        sun_x = int(self.w * 0.74 - (self.camera_x * 0.04) % 180)
        sun_y = int(self.h * (0.20 if self.time_key == "pagi" else (0.35 if self.time_key == "senja" else 0.18)))
        pygame.draw.circle(surf, self.atm["glow_color"], (sun_x, sun_y), 54)
        pygame.draw.circle(surf, self.atm["sun_color"], (sun_x, sun_y), 25 if self.time_key == "malam" else 35)

    def draw_hills(self, surf):
        gy = self.ground_y()
        for mult, h_base, col in ((0.16, 115, self.atm["far_mtn"]), (0.34, 62, self.atm["mid_hill"])):
            pts = [(0, self.h)]
            for sx in range(0, self.w + 36, 36):
                wx = sx + self.camera_x * mult
                h = h_base + math.sin(wx * 0.0025) * 38 + math.cos(wx * 0.0055) * 18
                pts.append((sx, int(gy - h)))
            pts.append((self.w, self.h))
            pygame.draw.polygon(surf, col, pts)

    def draw_tree(self, surf, sx, gy, sway, kind):
        if kind == "palm":
            pygame.draw.line(surf, (124, 88, 54), (int(sx), gy), (int(sx + sway), gy - 102), 7)
            tx, ty = int(sx + sway), gy - 102
            for i in range(-2, 3):
                pygame.draw.ellipse(surf, (22, 163, 74), (tx + i * 15 - 16, ty + abs(i) * 4 - 5, 32, 10))
        elif kind == "cemara":
            pygame.draw.line(surf, (92, 64, 51), (int(sx), gy), (int(sx + sway * 0.4), gy - 92), 6)
            for tier in range(3):
                ty = gy - 42 - tier * 22
                w = 26 - tier * 5
                cx = int(sx + sway * 0.35)
                pygame.draw.polygon(surf, (15, 118, 110), [(cx, ty - 22), (cx - w, ty), (cx + w, ty)])
        else:
            pygame.draw.line(surf, (74, 53, 37), (int(sx), gy), (int(sx + sway * 0.3), gy - 110), 9)
            cx, cy = int(sx + sway * 0.5), gy - 120
            pygame.draw.circle(surf, (21, 128, 61), (cx, cy), 34)
            pygame.draw.circle(surf, (22, 163, 74), (cx - 22, cy + 14), 24)
            pygame.draw.circle(surf, (22, 163, 74), (cx + 22, cy + 14), 24)

    def draw_zones(self, surf):
        gy = self.ground_y()
        pygame.draw.rect(surf, self.atm["ground"], (0, gy, self.w, self.h - gy))

        for z in ZONES:
            z_start = z["x_start"] - self.camera_x
            z_end = z["x_end"] - self.camera_x
            if z_end < -120 or z_start > self.w + 120:
                continue
            left = max(0, int(z_start))
            width = max(0, min(self.w, int(z_end)) - left)

            if z["terrain"] == "beach":
                wave_top = gy + 16
                pygame.draw.rect(surf, self.atm["water_top"], (left, wave_top, width, max(0, self.h - wave_top)))
                for layer in range(3):
                    y_base = wave_top + 14 + layer * 24
                    pts = [(x, int(y_base + math.sin((x + self.camera_x) * 0.022 + self.elapsed * (2.6 - layer * 0.4) + layer) * 6)) for x in range(left, left + width + 18, 18)]
                    if len(pts) >= 2:
                        pygame.draw.lines(surf, (240, 253, 250), False, pts, max(1, 3 - layer))
                for tx in range(z["x_start"] + 140, z["x_end"] - 90, 250):
                    self.draw_tree(surf, tx - self.camera_x, gy, math.sin(self.elapsed * 1.7 + tx * 0.01) * 5, "cemara" if z["id"] == "bengkenang" else "palm")

            elif z["terrain"] == "river":
                stream_top = gy + 18
                pygame.draw.rect(surf, self.atm["water_top"], (left, stream_top, width, max(0, self.h - stream_top)))
                for rx in range(z["x_start"] + 60, z["x_end"] - 60, 110):
                    sx = int(rx + ((self.elapsed * 55) % 110) - self.camera_x)
                    sy = stream_top + 22 + ((rx % 3) * 18)
                    if -40 <= sx <= self.w + 40:
                        pygame.draw.line(surf, (224, 247, 250), (sx, sy), (sx + 34, sy - 2), 2)
                for bx in range(z["x_start"] + 130, z["x_end"] - 80, 220):
                    sx = int(bx - self.camera_x)
                    if -40 <= sx <= self.w + 40:
                        pygame.draw.ellipse(surf, (71, 85, 105), (sx - 24, gy + 4, 48, 22))

            elif z["terrain"] == "waterfall":
                cliff_x = int(3560 - self.camera_x)
                pygame.draw.rect(surf, (30, 77, 59), (cliff_x - 55, gy - 170, 110, 170))
                for s in range(-2, 3):
                    wx = cliff_x + s * 14
                    pts = [(int(wx + math.sin(y * 0.08 - self.elapsed * 14 + s) * 3.5), y) for y in range(gy - 160, gy + 12, 16)]
                    if len(pts) >= 2:
                        pygame.draw.lines(surf, (186, 230, 253), False, pts, 5)

            elif z["terrain"] == "forest":
                for fx in range(z["x_start"] + 120, z["x_end"] - 80, 210):
                    self.draw_tree(surf, fx - self.camera_x, gy, math.sin(self.elapsed * 1.2 + fx * 0.008) * 3.5, "forest")
                rx, ry = int(4540 - self.camera_x), gy - 8
                pulse = 1.0 + 0.05 * math.sin(self.elapsed * 2.4)
                for p in range(5):
                    a = (p * math.tau) / 5 - math.pi / 2
                    px, py = int(rx + math.cos(a) * 14 * pulse), int(ry + math.sin(a) * 14 * pulse)
                    pygame.draw.circle(surf, (225, 29, 72), (px, py), int(12 * pulse))
                pygame.draw.circle(surf, (76, 5, 25), (rx, ry), 8)

            surf.blit(font_spot_tag.render(z["name"].upper(), True, (255, 255, 255)), (int(z_start) + 20, gy + 34))

    def draw_particles(self, surf):
        gy = self.ground_y()
        for dp in self.dust_particles:
            sx = int(dp[0] - self.camera_x)
            sy = int(gy - dp[1])
            rad = max(1, int(dp[4] * dp[5]))
            if -20 <= sx <= self.w + 20:
                pygame.draw.circle(surf, (255, 250, 240), (sx, sy), rad)

        for b in birds:
            wx = ((b["base_x"] + self.elapsed * b["speed"]) % (WORLD_WIDTH + 300)) - 150
            sx = int(wx - self.camera_x)
            if -40 <= sx <= self.w + 40:
                sy = int(b["base_y"] * gy + math.sin(self.elapsed * 1.8 + b["wing_phase"]) * 10)
                flap = int(math.sin(b["wing_phase"]) * 7 * b["scale"])
                col = (226, 232, 240) if self.time_key == "malam" else (15, 23, 42)
                pygame.draw.line(surf, col, (sx - 8, sy - flap), (sx, sy), 2)
                pygame.draw.line(surf, col, (sx, sy), (sx + 8, sy - flap), 2)

        for lf in leaves:
            sx = int(lf["x"] - self.camera_x + math.sin(lf["phase"]) * lf["sway_amp"])
            sy = int(lf["y_ratio"] * gy)
            if -20 <= sx <= self.w + 20:
                pygame.draw.ellipse(surf, lf["color"], (sx - lf["size"], sy - 2, lf["size"] * 2, lf["size"]))

        if self.atm["fireflies"] > 0.2:
            for ff in fireflies:
                sx = int(ff["x"] - self.camera_x)
                sy = int(ff["y_ratio"] * gy + math.cos(ff["phase"] * 0.8) * 14)
                if -20 <= sx <= self.w + 20 and math.sin(ff["phase"]) > 0:
                    pygame.draw.circle(surf, (253, 224, 71), (sx, sy), int(ff["r"]))

    def draw_spots(self, surf):
        gy = self.ground_y()
        for idx, spot in enumerate(SPOTS):
            sx, sy = int(spot["x"] - self.camera_x), int(gy + spot["y_offset"])
            if sx < -90 or sx > self.w + 90:
                continue
            pulse = int(math.sin(self.elapsed * 3.4 + idx) * 5)
            ring_col = (253, 224, 71) if self.selected_spot == idx else ((110, 231, 183) if self.hovered_spot == idx else (255, 255, 255))
            core_col = (250, 204, 21) if self.selected_spot == idx else ((52, 211, 153) if self.hovered_spot == idx else (15, 23, 42))
            pygame.draw.circle(surf, ring_col, (sx, sy), max(8, 17 + pulse), 2)
            pygame.draw.circle(surf, core_col, (sx, sy), 9)
            pygame.draw.circle(surf, (255, 255, 255), (sx, sy), 3)

            label = font_spot_tag.render(spot["title"], True, (248, 250, 252))
            pill = pygame.Rect(sx - (label.get_width() + 16) // 2, sy - 38, label.get_width() + 16, 22)
            self.draw_panel(surf, pill, radius=11)
            surf.blit(label, (pill.x + 8, pill.y + 3))

    def draw_player(self, surf):
        sx, gy = int(self.player_x - self.camera_x), self.ground_y()
        moving = abs(self.player_vx) > 8 and self.on_ground
        bob = int(abs(math.sin(self.walk_cycle)) * 5) if moving else (0 if not self.on_ground else int(math.sin(self.elapsed * 2.2) * 1.5))

        # Bayangan di permukaan tanah mengecil saat karakter melompat tinggi
        height_factor = max(0.35, 1.0 - self.player_y / 220.0)
        shad_w = max(12, int(34 * height_factor))
        shad_h = max(4, int(10 * height_factor))
        pygame.draw.ellipse(surf, (60, 50, 38), (sx - shad_w // 2, gy - shad_h // 2 + 1, shad_w, shad_h))

        py = gy - bob - int(self.player_y)
        if not self.on_ground:
            swing = -7 if self.player_vy > 0 else 6
        else:
            swing = int(math.sin(self.walk_cycle) * 9) if moving else 0

        pygame.draw.line(surf, (30, 41, 59), (sx - 2 * self.facing, py - 16), (sx - 2 * self.facing - swing, py - 2), 5)
        pygame.draw.line(surf, (15, 23, 42), (sx + 2 * self.facing, py - 16), (sx + 2 * self.facing + swing, py - 2), 5)

        pack_x = sx - 12 if self.facing == 1 else sx + 4
        pygame.draw.rect(surf, (217, 119, 6), (pack_x, py - 36, 8, 18), border_radius=3)
        pygame.draw.rect(surf, (13, 148, 136), (sx - 7, py - 37, 15, 21), border_radius=5)

        pygame.draw.circle(surf, (252, 211, 77), (sx + self.facing, py - 45), 9)
        pygame.draw.circle(surf, (15, 23, 42), (sx + self.facing * 5, py - 46), 2)
        pygame.draw.ellipse(surf, (254, 240, 138), (sx + self.facing - 13, py - 55, 28, 7))
        pygame.draw.rect(surf, (234, 179, 8), (sx + self.facing - 6, py - 60, 14, 7), border_radius=3)

    def draw_hud(self, surf):
        cur_zone = next((z for z in ZONES if z["x_start"] <= self.player_x < z["x_end"]), ZONES[-1])
        title_box = pygame.Rect(16, 14, 480, 56)
        self.draw_panel(surf, title_box, radius=14)
        surf.blit(font_title.render("Jelajah Alam Bengkulu Selatan", True, (255, 255, 255)), (title_box.x + 14, title_box.y + 8))
        surf.blit(font_sub.render(f"{cur_zone['name']} - {cur_zone['subtitle']}", True, (153, 246, 228)), (title_box.x + 14, title_box.y + 32))

        self.time_buttons = []
        time_box = pygame.Rect(self.w - 244, 14, 228, 42)
        self.draw_panel(surf, time_box, radius=12)
        for idx, t_key in enumerate(("pagi", "senja", "malam")):
            rect = pygame.Rect(time_box.x + 6 + idx * 73, time_box.y + 6, 70, 30)
            self.time_buttons.append((rect, t_key))
            active = self.time_key == t_key
            pygame.draw.rect(surf, (252, 211, 77) if active else (30, 56, 70), rect, border_radius=8)
            lbl = font_btn.render(ATMOSPHERES[t_key]["label"], True, (15, 23, 42) if active else (226, 232, 240))
            surf.blit(lbl, lbl.get_rect(center=rect.center))

        self.zone_buttons = []
        nav_box = pygame.Rect(16, self.h - 52, min(self.w - 32, 760), 38)
        self.draw_panel(surf, nav_box, radius=12)
        zx = nav_box.x + 6
        for z in ZONES:
            lbl = font_btn.render(z["name"], True, (255, 255, 255))
            zw = lbl.get_width() + 18
            if zx + zw > nav_box.right - 6:
                break
            rect = pygame.Rect(zx, nav_box.y + 4, zw, 30)
            self.zone_buttons.append((rect, z))
            active = cur_zone["id"] == z["id"]
            pygame.draw.rect(surf, (20, 120, 145) if active else (24, 46, 58), rect, border_radius=8)
            surf.blit(lbl, lbl.get_rect(center=rect.center))
            zx += zw + 6

        hint_txt = font_sub.render("A/D atau <-/-> Jalan | Spasi/W/Up Lompat | Klik/E Amati | 1/2/3 Waktu", True, (226, 232, 240))
        hint_box = pygame.Rect(self.w - hint_txt.get_width() - 32, self.h - 48, hint_txt.get_width() + 16, 30)
        self.draw_panel(surf, hint_box, radius=10)
        surf.blit(hint_txt, (hint_box.x + 8, hint_box.y + 7))

    def draw_spot_card(self, surf):
        if self.selected_spot is None:
            return
        spot = SPOTS[self.selected_spot]
        card = pygame.Rect(self.w - 416, 72, 400, 340)
        self.draw_panel(surf, card, radius=18, col=(10, 28, 38))

        surf.blit(font_badge.render(spot["category"].upper(), True, (110, 231, 183)), (card.x + 18, card.y + 16))
        surf.blit(font_card_title.render(spot["title"], True, (255, 255, 255)), (card.x + 18, card.y + 36))
        surf.blit(font_sub.render(spot["zone_name"], True, (153, 246, 228)), (card.x + 18, card.y + 62))

        self.close_btn_rect = pygame.Rect(card.right - 44, card.y + 14, 28, 28)
        pygame.draw.rect(surf, (35, 55, 68), self.close_btn_rect, border_radius=8)
        x_lbl = font_btn.render("X", True, (255, 255, 255))
        surf.blit(x_lbl, x_lbl.get_rect(center=self.close_btn_rect.center))

        y_cursor = card.y + 92
        for para, col in ((spot["desc"], (241, 245, 249)), (spot["detail"], (253, 230, 138))):
            line = ""
            for w in para.split():
                test = f"{line} {w}".strip()
                if font_card_body.size(test)[0] <= card.width - 36:
                    line = test
                else:
                    surf.blit(font_card_body.render(line, True, col), (card.x + 18, y_cursor))
                    y_cursor += 20
                    line = w
            if line:
                surf.blit(font_card_body.render(line, True, col), (card.x + 18, y_cursor))
                y_cursor += 26

        self.prev_btn_rect = pygame.Rect(card.x + 18, card.bottom - 46, 175, 32)
        self.next_btn_rect = pygame.Rect(card.right - 193, card.bottom - 46, 175, 32)
        for rect, txt in ((self.prev_btn_rect, "<- Sebelumnya"), (self.next_btn_rect, "Berikutnya ->")):
            pygame.draw.rect(surf, (30, 64, 80), rect, border_radius=10)
            pygame.draw.rect(surf, (103, 232, 249), rect, width=1, border_radius=10)
            lbl = font_btn.render(txt, True, (255, 255, 255))
            surf.blit(lbl, lbl.get_rect(center=rect.center))

    def render(self):
        self.draw_sky(screen)
        self.draw_hills(screen)
        self.draw_zones(screen)
        self.draw_particles(screen)
        self.draw_spots(screen)
        self.draw_player(screen)
        self.draw_hud(screen)
        self.draw_spot_card(screen)
        pygame.display.flip()


def main():
    game = ExplorerGame()
    while True:
        dt = min(0.05, clock.tick(FPS) / 1000.0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
        game.update(dt)
        game.render()


if __name__ == "__main__":
    main()