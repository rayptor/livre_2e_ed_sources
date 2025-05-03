import math
import sys

WIDTH, HEIGHT = 150,150
MAX_DEPTH = 2
SUPERSAMPLING_FACTOR = 2

class Vecteur:
    __slots__ = ("x", "y", "z")
    
    def __init__(self, x = None, y = None, z = None) -> None:
        if isinstance(x, float) or isinstance(x, int) \
        and isinstance(y, float) or isinstance(y, int) \
        and isinstance(z, float) or isinstance(z, int):
            self.x = x
            self.y = y
            self.z = z
        else:
            raise TypeError("Type non conforme !")
    
    def __add__(self, other):
        return Vecteur(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vecteur(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vecteur(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Vecteur(self.x / scalar, self.y / scalar, self.z / scalar)

    def __rtruediv__(self, scalar):
        return Vecteur(scalar / self.x, scalar / self.y, scalar / self.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def normalize(self):
        mag = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        return Vecteur(self.x / mag, self.y / mag, self.z / mag) if mag != 0 else Vecteur(0, 0, 0)

    def component_mul(self, other):
        return Vecteur(self.x * other.x, self.y * other.y, self.z * other.z)

class Rayon:
    __slots__ = ("origin", "direction")
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()

class Sphere:
    __slots__ = ("center", "radius", "color", "roughness", "metallic", "transparency")
    def __init__(self, center, radius, color, roughness, metallic=False, transparency=0):
        self.center = center
        self.radius = radius
        self.color = color
        self.roughness = roughness
        self.metallic = metallic
        self.transparency = transparency

    def intersect(self, ray):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        disc = b * b - 4 * a * c
        if disc < 0:
            return None
        t = (-b - math.sqrt(disc)) * 0.5
        return t if t > 0 else None

class Plan:
    __slots__ = ("point", "normale")
    def __init__(self, point, normale):
        self.point = point
        self.normale = normale.normalize()

    def intersect(self, ray):
        denom = ray.direction.dot(self.normale)
        if abs(denom) > sys.float_info.epsilon:
            t = (self.point - ray.origin).dot(self.normale) / denom
            return t if t > 0 else None
        return None

def ggx_distribution(nh, roughness):
    alpha = roughness * roughness
    alpha2 = alpha * alpha
    n_dot_h2 = nh * nh
    denom = n_dot_h2 * (alpha2 - 1) + 1
    return alpha2 / (math.pi * denom * denom)

def fresnel(n1, n2, cos_i):
    sin_i = math.sqrt(max(0, 1 - cos_i**2))
    sin_t = n1 * sin_i / n2
    
    if sin_t >= 1:
        return 1.0

    cos_t = math.sqrt(max(0, 1 - sin_t**2))
    
    # Reflectance pour les ondes polarisées P et S
    r_s = ((n1 * cos_i - n2 * cos_t) / (n1 * cos_i + n2 * cos_t))**2
    r_p = ((n2 * cos_i - n1 * cos_t) / (n2 * cos_i + n1 * cos_t))**2
    
    return (r_s + r_p) / 2

def fresnel_vector(n1, n2, cos_i, f0):
    f = fresnel(n1, n2, cos_i)
    return Vecteur(
        f0.x + (1 - f0.x) * f,
        f0.y + (1 - f0.y) * f,
        f0.z + (1 - f0.z) * f
    )

def ggx_geometry(nv, nl, roughness):
    k = (roughness + 1) * (roughness + 1) / 8
    g1v = nv / (nv * (1 - k) + k)
    g1l = nl / (nl * (1 - k) + k)
    return g1v * g1l

def reflect(normale, incident) -> float:
    nl = max(normale.dot(incident), 0)
    if nl < 0:
        nl = -nl
    r = 2 * normale * nl - incident

    return r

def refract(incident, normale, n1_over_n2):
    cos_i = -normale.dot(incident)
    sin_t2 = n1_over_n2 * n1_over_n2 * (1.0 - cos_i**2)
    if sin_t2 > 1.0:
        return None
    cos_t = math.sqrt(1.0 - sin_t2)
    return incident * n1_over_n2 + normale * (n1_over_n2 * cos_i - cos_t)

BLACK = Vecteur(0, 0, 0)
WHITE = Vecteur(1, 1, 1)
BLUE = Vecteur(0, 0, 1)
RED = Vecteur(1, 0, 0)
GREEN = Vecteur(0, 1, 0)
YELLOW = Vecteur(1, 1, 0)

LIGHT_POSITION = Vecteur(5, 10, 20)
LIGHT_INTENSITY = 2

sphere1 = Sphere(Vecteur(0, 0, -5), 1, Vecteur(0.8, 0.8, 0.8), 0.1, transparency=0.5)
sphere2 = Sphere(Vecteur(-2, 0, -4), 0.7, RED, 0.1, metallic=True)
sphere3 = Sphere(Vecteur(2, 0, -4), 0.7, GREEN, 0.3, metallic=True)
sphere4 = Sphere(Vecteur(0, -0.5, -3), 0.5, BLUE, 0.5, metallic=True)
plane = Plan(Vecteur(0, -1, 0), Vecteur(0, 1, 0))

objects = [sphere1, sphere2, sphere3, sphere4, plane]

def ray_color(ray, depth=0):
    if depth >= MAX_DEPTH:
        return BLACK

    closest_t = float('inf')
    closest_obj = None

    for obj in objects:
        t = obj.intersect(ray)
        if t and t < closest_t:
            closest_t = t
            closest_obj = obj

    if closest_obj:
        hit_point = ray.origin + ray.direction * closest_t
        if isinstance(closest_obj, Sphere):
            normale = (hit_point - closest_obj.center).normalize()
        else:  # Plan
            normale = closest_obj.normale

        light_dir = (LIGHT_POSITION - hit_point).normalize()
        view_dir = (ray.origin - hit_point).normalize()
        half_vector = (light_dir + view_dir).normalize()

        nl = max(normale.dot(light_dir), 0)
        nv = max(normale.dot(view_dir), 0)
        nh = max(normale.dot(half_vector), 0)
        vh = max(view_dir.dot(half_vector), 0)

        if isinstance(closest_obj, Sphere):
            D = ggx_distribution(nh, closest_obj.roughness)
            G = ggx_geometry(nv, nl, closest_obj.roughness)
            if closest_obj.metallic:
                F = fresnel_vector(1.0, 2.5, vh, closest_obj.color)  # conducteurs
            else:
                F = fresnel_vector(1.0, 1.5, vh, Vecteur(0.04, 0.04, 0.04)) # diélectriques

            specular = D * F * G / (4 * nv * nl + 0.001)
            if closest_obj.metallic:
                diffuse = BLACK
            else:
                kd = Vecteur(1, 1, 1) - F
                diffuse = closest_obj.color.component_mul(kd) * (nl / math.pi)

            color = (diffuse + specular) * LIGHT_INTENSITY * nl

            if closest_obj.transparency > 0:
                reflected_dir = ray.direction - normale * 2 * ray.direction.dot(normale)
                reflected_ray = Rayon(hit_point + normale * 0.001, reflected_dir)
                reflected_color = ray_color(reflected_ray, depth + 1)
                
                refracted_dir = refract(ray.direction, normale, 1.5) # verre
                if refracted_dir:
                    refracted_ray = Rayon(hit_point - normale * 0.001, refracted_dir)
                    refracted_color = ray_color(refracted_ray, depth + 1)
                    color = color * (1 - closest_obj.transparency) + refracted_color * closest_obj.transparency
                else:
                    color = color * (1 - closest_obj.transparency) + reflected_color * closest_obj.transparency
            elif depth < MAX_DEPTH - 1:
                reflected_dir = ray.direction - normale * 2 * ray.direction.dot(normale)
                reflected_ray = Rayon(hit_point + normale * 0.001, reflected_dir)
                reflected_color = ray_color(reflected_ray, depth + 1)
                color = color * 0.5 + reflected_color * 0.5
        else:  # Plan
            x, _, z = hit_point.x, hit_point.y, hit_point.z
            color = YELLOW if (int(x) + int(z)) % 2 == 0 else BLACK
            color = color * nl * LIGHT_INTENSITY

        return color

    # Ciel
    t = 0.5 * (ray.direction.y + 1)
    return WHITE * (1 - t) + BLUE * t

def supersample(i, j):
    color = Vecteur(0, 0, 0)
    for si in range(SUPERSAMPLING_FACTOR):
        for sj in range(SUPERSAMPLING_FACTOR):
            u = (i + (si + 0.5) / SUPERSAMPLING_FACTOR) / (WIDTH - 1)
            v = (j + (sj + 0.5) / SUPERSAMPLING_FACTOR) / (HEIGHT - 1)
            ray = Rayon(Vecteur(0, 0, 0), Vecteur(u - 0.5, v - 0.5, -1))
            sample_color = ray_color(ray)
            color = color + sample_color
    return color * (1 / (SUPERSAMPLING_FACTOR * SUPERSAMPLING_FACTOR))


def write_tga(filename, width, height):
    with open(filename, 'wb') as f:
        # Format TGA (18 octets)
        header = bytearray([
            0,
            0,
            2,
            0, 0, 0, 0, 0,
            0, 0,
            0, 0,
            width & 255, (width >> 8) & 255,
            height & 255, (height >> 8) & 255,
            24,
            0
        ])
        f.write(header)
        
        for j in range(height): 
            for i in range(width):
                color = supersample(i, j)
                r, g, b = [min(255, max(0, int(c * 255))) for c in (color.x, color.y, color.z)]
                f.write(bytes([b, g, r]))  # TGA uses BGR order

# Usage
nomImage = "output.tga"
write_tga(nomImage, WIDTH, HEIGHT)
