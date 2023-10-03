from chernov_faces import compose_face
import pandas as pd
from sklearn.datasets import load_iris
import numpy as np
import matplotlib.pyplot as plt

# Загружаем датасет Iris
data = load_iris()
df_iris = pd.DataFrame(data.data, columns=data.feature_names)

# Инкодим целевую переменную
df_iris['target'] = data.target

# Датасет Iris имеет 4 числовых переменные
iris_num = df_iris.select_dtypes(include=[np.number]).values

# Инициализируем константы для всех переменных, кроме четырёх так как
# Функция, используемая для создания лиц, должна принимать 17 характеристик для отображения их в виде черт лица.
# Здесь у нас всего 4 числовые характеристики, и так как я не хотел изменять код функции,
# Использовались постоянные значения для остальных.
cf = np.ones((df_iris.shape[0], 18)) * 0.9

# Заполняем четыре переменные данными из Iris
cf[:, 0] = iris_num[:, 0]  # x1 - height of upper face
cf[:, 6] = iris_num[:, 1]  # x7 - vertical position of mouth
cf[:, 13] = iris_num[:, 2]  # x14 - size of eyes
cf[:, 3] = iris_num[:, 3]  # x4 - width of upper face

# Разделяем матрицу на три класса ирисов
cf_setosa = cf[df_iris["target"]==0, :]
cf_versicolor = cf[df_iris["target"]==1, :]
cf_virginica = cf[df_iris["target"]==2, :]

fig, ax = plt.subplots(3,5, figsize=(20,6))

# Рисуем лица для каждого класса ирисов
for i in range(5):
    compose_face(ax[0, i], *cf_setosa[i+10, :])
    ax[0, i].set_facecolor('xkcd:sky blue')
    ax[0, i].axis([-7, 7, -7, 7])
    ax[0, i].set_xticks([])
    ax[0, i].set_yticks([])

    compose_face(ax[1, i], *cf_versicolor[i+10, :])
    ax[1, i].set_facecolor('xkcd:salmon')
    ax[1, i].axis([-7, 7, -7, 7])
    ax[1, i].set_xticks([])
    ax[1, i].set_yticks([])

    compose_face(ax[2, i], *cf_virginica[i+10, :])
    ax[2, i].set_facecolor('xkcd:pale green')
    ax[2, i].axis([-7, 7, -7, 7])
    ax[2, i].set_xticks([])
    ax[2, i].set_yticks([])

plt.show()