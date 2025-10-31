import json
import os
import time

import cv2
import numpy as np
from pyniryo import CalibrateMode, NiryoRobot
from red_rectangle_detector import RedRectangleDetector

"""
Posições fixas de juntas do NiryoNed para movimentação dentro do teste da
matriz de homografia não é necessário mudar isso.
"""
PRE_CAP = [0.02, 0.61, -0.55, -0.06, -1.50, 0.00]
HOME_POS = [0.02, 0.61, -1.33, -0.06, 0.03, -0.01]

"""
Altura minima que o robô vai chegar para "pegar" o objeto, a altura abaixo
corresponde ao objeto azul "redondo", caso você utilize um objeto diferente
medir a altura com o NiryoStudio, para evitar problemas.
"""
Z = 0.24

# Ja visto em Workshop
robot = NiryoRobot("169.254.200.200")
# robot = NiryoRobot("127.0.0.1")

"""
Abertura de camera primeiro argumento se trata da posição do dispositivo na
lista de cameras conectadas ao computador, geralmente esse número pode variar
de computador caso esteja abrindo a webcam do seu computador, mudar o
parametro para 0 ou 1, vai depender do que você está utilizando, Segundo
argumento opcional, porém facilita e agiliza a abertura de camera, a diferença
com e sem é gritante.
"""
camera = cv2.VideoCapture(2)

"""
Mudança na resolução da camera para uma especifica, lembre-se que o processo
de homografia está sendo feito nesta resolução então ao utilizar a mesma você
precisa ter certeza que a resolução da camera é a mesma.
"""
# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Criação de variáveis para o código
centroids = None
table_points = []
homography_matrix: np.ndarray = np.array([])

# Instanciação da classe RedRectangleDetector
red_rectangle_detector = RedRectangleDetector(min_contour_area=500)

"""
Requisição de uma nova calibração do braço, calibração e colocando o braço em
learning mode (molinho) perceba que tem alguns sleeps entre funções eles evitam
que aja um problema de comunicação com o robô
"""
robot.calibrate_auto()
time.sleep(0.5)
robot.calibrate(CalibrateMode.AUTO)
time.sleep(0.5)
robot.set_learning_mode(True)

"""
Todo o processo está dentro de um grande while para que o código parar de
executar apenas quando a matriz foi gerada e salva
"""
homography_matrix_save = False
while not homography_matrix_save:
    """
    While responsável por pegar os pontos em pixels dos retângulos vermelhos,
    esse while será quebrado apenas quando for apertado q / Q na camera, e essa
    tecla so deve ser pressionada caso as marcações estejam minimamente dentro
    do esperado.
    """
    ret, frame = camera.read()
    # centroids = red_rectangle_detector.get_rectangle_centroids(frame)
    roi_coords = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
    x, y, w, h = roi_coords
    print(x, y, w, h)
    x_roi = x + 10
    y_roi = y + 10
    x_max = x_roi + w - 20
    y_max = y_roi + h - 20
    centroids = [(x_roi, y_roi), (x_max, y_roi), (x_roi, y_max), (x_max, y_max)]
    if len(centroids) == 4:
        for centroid in centroids:
            frame = cv2.circle(frame, centroid, 5, (0, 0, 0), 5)

    cv2.imshow("Painted", frame)
    key = cv2.waitKey(1)
    if key == ord("q") or key == ord("Q"):
        homography_points_done = True

    cv2.destroyAllWindows()

    """
    Parte necessária para criação do ponto de teste da matriz criada, soma e
    divisão por 4 para encontrar o centro, um novo ponto sem ser os encontrados
    antes.
    """
    x_axis = 0
    y_axis = 0
    for centroid in centroids:
        x_axis += centroid[0]
        y_axis += centroid[1]

    center = [int(x_axis / 4), int(y_axis / 4)]
    print(center)

    """
    While responsável por mostrar os pontos na tela e ao o usuário levar o
    braço robótico até o ponto ao apertar q / Q ele irá pegar a posição
    cartesiana do robô atualmente, esse processo será repetido 4 vezes para
    pegar a quantidade minima de pontos necessários para fazer a homografia.
    """
    homography_matrix_finish = False
    centroid_n = 0
    while not homography_matrix_finish:
        ret, frame = camera.read()
        frame = cv2.circle(frame, centroids[centroid_n], 5, (0, 0, 0), 5)
        cv2.imshow("Painted", frame)
        key = cv2.waitKey(1)

        if key == ord("q") or key == ord("Q"):
            actual_pose = robot.get_pose()
            table_points.append((actual_pose.x, actual_pose.y))
            centroid_n += 1

        if centroid_n == len(centroids):
            homography_matrix_finish = True

    cv2.destroyAllWindows()

    """
    Trecho de código responsável por fazer gerar a matriz de homografia
    """
    image_points = np.array(centroids)
    robot_points = np.array(table_points)

    homography_matrix, _ = cv2.findHomography(
        image_points, robot_points, method=cv2.RANSAC
    )

    """
    Parte do código responsável por conferir se a matriz de homografia ficou
    condizente com o esperado, o robô deve conseguir acertar minimante o alvo
    desejado, irá aparecer um ponto dentro da imagem colocar o centro da peça
    nesse ponto para conferir a matriz.
    """
    conference_done = False
    while not conference_done:
        ret, frame = camera.read()

        frame = cv2.circle(frame, center, 5, (0, 0, 255), 5)

        cv2.imshow("frame", frame)

        key = cv2.waitKey(1)

        if (key == ord("q") or key == ord("Q")) and len(center) == 2:
            robot.move_joints(PRE_CAP)

            """
            #######################################
            #                                     #
            #             !!Atenção!!             #
            # Trecho de código a baixo e a forma  #
            #  como se utiliza a matriz de homo-  #
            #  grafia e será como você irão usar  #
            #     em seus respectivos códigos     #
            #                                     #
            #######################################

            Primeiramente criação de um array numpy com os pontos que objeto
            se encontra na imagem, após e passado na função np.dot
            primeiramente a matriz depois o array dos pontos que acabamos de
            criar, dessa forma a função irá retornar um array, depois disso
            iremos descobrir o valor de x dividindo o primeiro argumento do
            array pelo terceiro que é o denominador da matriz, depois e feito
            a mesma coisa para o y, porém dessa vez iremos dividir o segundo
            argumento do array pelo terceiro argumento, e de preferência fazer
            o cast das respostas para float para facilitar a utilização no
            resto do código.
            """
            dot_image = np.array([[*center, 1]], dtype=np.float32).T
            coordinates = np.dot(homography_matrix, dot_image)

            x = float((coordinates[0] / coordinates[2])[0])
            y = float((coordinates[1] / coordinates[2])[0])

            """
            Movimentação em forma cartesiana para as coordenadas obtidas pela
            matriz.
            """
            pose = [x, y, Z, 0.0, 1.527, 0.0]
            robot.move_pose(pose)
            time.sleep(2)
            robot.move_joints(PRE_CAP)

        if key == ord("s") or key == ord("S"):
            """
            Gravação de de arquivo json com a atual matrix de homografia, tal
            arquivo será gerado na pasta atual do arquivo.
            """
            path = os.getcwd()
            # path = "/assets"
            path = os.path.join(path, f"{path}/homography.json")
            with open(path, "w") as arch:
                json.dump(homography_matrix.tolist(), arch)
                print("Matriz de homography salva com sucesso")

            homography_matrix_save = True
            conference_done = True

        if (key == ord("n")) or key == ord("N"):
            """
            Caso a matriz não fique como o desejado reinicia todo o processo
            """
            homography_matrix_save = False
            centroids = None
            conference_done = True
            homography_matrix = np.array([])
            table_points = []
