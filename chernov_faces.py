import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# Константы
UPPER_FACE_MULTIPLIER = 1.9
UPPER_FACE_ADDITION = 0.25
LOWER_FACE_ADDITION = 0.2
NOSE_LENGTH_MULTIPLIER = 0.3
CURVATURE_MULTIPLIER = 5
EYES_SEPARATION_DIVIDER = 5
EYES_SLANT_MULTIPLIER = 2
EYES_SHAPE_ADDITION = 0.05
EYES_SIZE_ADDITION = 0.1
PUPIL_POSITION_MULTIPLIER = 0.5
BROWS_VERTICAL_POSITION_MULTIPLIER = 0.25
BROWS_SLANT_MULTIPLIER = 0.5
BROWS_SIZE_ADDITION = 0.1


def adjust_parameters(params):
    params[2] *= UPPER_FACE_MULTIPLIER
    params[3] += UPPER_FACE_ADDITION
    params[4] += LOWER_FACE_ADDITION
    params[5] *= NOSE_LENGTH_MULTIPLIER
    params[7] *= CURVATURE_MULTIPLIER
    params[10] /= EYES_SEPARATION_DIVIDER
    params[11] *= EYES_SLANT_MULTIPLIER
    params[12] += EYES_SHAPE_ADDITION
    params[13] += EYES_SIZE_ADDITION
    params[14] *= PUPIL_POSITION_MULTIPLIER
    params[15] *= BROWS_VERTICAL_POSITION_MULTIPLIER
    params[16] *= BROWS_SLANT_MULTIPLIER
    params[17] += BROWS_SIZE_ADDITION
    return params


def compose_face(ax, *params):
    params = adjust_parameters(list(params))
    upper_face_center = (0, (params[0] + params[2]) * 0.5)
    lower_face_center = (0, (-params[0] + params[1] + params[2]) * 0.5)

    create_ellipse(ax, upper_face_center, params[3] * 2, params[0] - params[2])
    create_ellipse(ax, lower_face_center, params[4] * 2, params[0] + params[1] + params[2])
    ax.plot([0, 0], [-params[5] / 2, params[5] / 2], 'k')  # Рисуем нос
    
    create_mouth(ax, params[6], params[7], params[8])

    create_eyes(ax, params[9], params[10], params[11], params[12], params[13])

    create_eyebrows(ax, params[9], params[10], params[11], params[12], params[13], params[15], params[16], params[17])
    
    return ax


def create_ellipse(ax, center, width, height):
    ellipse = mpatches.Ellipse(center, width, height, fc='white', edgecolor='black', linewidth=2)
    ax.add_patch(ellipse)


def create_mouth(ax, vertical_position, curvature, width):
    arc_center = (0, -vertical_position + 0.5 / curvature)
    theta_start = 270 - 180 / np.pi * np.arctan(curvature * width)
    theta_end = 270 + 180 / np.pi * np.arctan(curvature * width)
    arc = mpatches.Arc(arc_center, 1 / curvature, 1 / curvature, theta1=theta_start, theta2=theta_end)
    ax.add_patch(arc)


def create_eyes(ax, vertical_position, separation, slant, eccentricity, size):
    # Создание областей для глаз с учетом заданных параметров
    left_eye_center = (-separation - size * 0.5, vertical_position)
    right_eye_center = (separation + size * 0.5, vertical_position)
    
    left_eye = mpatches.Ellipse(left_eye_center, size, eccentricity * size, angle= -180 / np.pi * slant, facecolor='white', edgecolor='black')
    right_eye = mpatches.Ellipse(right_eye_center, size, eccentricity * size, angle= 180 / np.pi * slant, facecolor='white', edgecolor='black')
    
    ax.add_patch(left_eye)
    ax.add_patch(right_eye)
    
    # Добавление зрачков
    left_pupil_center = (left_eye_center[0] - size * 0.25, vertical_position)
    right_pupil_center = (right_eye_center[0] + size * 0.25, vertical_position)
    
    ax.add_patch(mpatches.Ellipse(left_pupil_center, 0.05, 0.05, facecolor='black'))
    ax.add_patch(mpatches.Ellipse(right_pupil_center, 0.05, 0.05, facecolor='black'))


def create_eyebrows(ax, vertical_position, separation, slant, eccentricity, size, brow_vertical_position, brow_slant, brow_size):
    # Определение параметров бровей
    eyebrow_height = vertical_position + eccentricity * size * (brow_vertical_position + brow_slant)
    
    left_eyebrow_start = ((-separation - size - size * brow_size) * 0.5, eyebrow_height)
    left_eyebrow_end = ((-separation - size + size * brow_size) * 0.5, eyebrow_height)
    
    right_eyebrow_start = ((separation + size + size * brow_size) * 0.5, eyebrow_height)
    right_eyebrow_end = ((separation + size - size * brow_size) * 0.5, eyebrow_height)
    
    # Рисование бровей
    ax.plot([left_eyebrow_start[0], left_eyebrow_end[0]], [left_eyebrow_start[1], left_eyebrow_end[1]], 'k')
    ax.plot([right_eyebrow_start[0], right_eyebrow_end[0]], [right_eyebrow_start[1], right_eyebrow_end[1]], 'k')