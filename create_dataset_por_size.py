from distutils.log import error
import os
from glob import glob
import xml.etree.ElementTree as ET
import cv2
from pathlib import Path
import json


paths = './Agus/'  # Aqui va la ruta completa de donde estan la carpeta test


def crearCarpetasNuevas(path):
    conjuntos = ['dataset_size_0', 'dataset_size_1', 'dataset_size_2']
    nombres_json = ['TEST_objects_0.json',
                    'TEST_objects_1.json', 'TEST_objects_2.json']
    nombres_i_json = ['TEST_images_0.json',
                      'TEST_images_1.json', 'TEST_images_2.json']
    for folder in conjuntos:  # Creamos primero los folders
        os.makedirs(path + folder, exist_ok=True)

    os.makedirs(path + 'JSONFiles', exist_ok=True)
    # Primero obtendremos la lista de las imagenes y de los anotaciones con las filtraciones
    # Empezaremos a

    lista_paths_nuevos_imagenes = {0: [], 1: [], 2: []}
    lista_objetos = {0: [], 1: [], 2: []}

    for indice, folder in enumerate(conjuntos):
        anot, img = getPathImgXML(path, indice, 'Annotations', 'JPEGImages')
        for xml, jpg in zip(anot, img):
            nuevo_path = path + folder + '/' + Path(jpg).stem + '.jpg'
            lista_paths_nuevos_imagenes[indice].append(nuevo_path)
            pintarCajaGrisPorImagenYGuardado(nuevo_path, xml, jpg, indice)

        lista_objetos[indice] = getObjectsForXML(anot, indice)

    for indice, arreglo in zip(lista_paths_nuevos_imagenes.keys(), lista_paths_nuevos_imagenes.values()):
        with open(os.path.join(path + 'JSONFiles', nombres_i_json[indice]), 'w') as file:
            json.dump(arreglo, file)

    for indice, arreglo in zip(lista_objetos.keys(), lista_objetos.values()):
        with open(os.path.join(path + 'JSONFiles', nombres_json[indice]), 'w') as file:
            json.dump(arreglo, file)


def pintarCajaGrisPorImagenYGuardado(path_guardado, path_xml, path_img, indice):

    img = cv2.imread(path_img)

    tree = ET.parse(path_xml)
    root = tree.getroot()
    items = []
    for object in root.iter('object'):
        if int(object.find('size').text) != indice:
            bbox = object.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            items.append([(xmin, ymin), (xmax, ymax)])

    for xy in items:
        img = cv2.rectangle(img, xy[0], xy[1], (127, 127, 127), -1)

    cv2.imwrite(path_guardado, img)


def getPathImgXML(root, index_size, annotations='annotations', images='images'):
    '''
    Params:
    root (ruta raiz donde estan las carpetas de imagenes y anotaciones) 
    annotations (nombre de la carpeta de las anotaciones)
    images (nombre de la carpeta de las imagenes)
    Obtendremos todas las ubicaciones en orden alfabetico
    '''
    path = root + annotations + '/*.xml'
    annot = glob(path)
    annot.sort()

    path = root + images + '/*.jpg'
    imgs = glob(path)
    imgs.sort()

    if len(annot) == 0 or len(imgs) == 0:
        print('No hay imagenes')
        return

    print('Hay {} imagenes y anotaciones'.format(len(imgs)))

    aux_anot = []
    aux_imgs = []
    errors = 0
    inapropiate = 0

    for i, xml in enumerate(annot):
        tree = ET.parse(xml)
        root = tree.getroot()

        if int(root.find('faces').text) == -1:
            annot.pop(i)
            imgs.pop(i)
            inapropiate += 1

        if int(root.find('faces').text) == 0:
            annot.pop(i)
            imgs.pop(i)
            errors += 1

        for object in root.iter('object'):
            size = int(object.find('size').text)
            if size == index_size:
                aux_anot.append(annot[i])
                aux_imgs.append(imgs[i])
                break

    print("Hubieron {} inapropiadas y {} errores de deteccion - Imagenes que pasan el filtro: {}".format(
        inapropiate, errors, len(aux_imgs)))
    return aux_anot, aux_imgs


def getObjectsForXML(annot, indice):

    out = []

    for xml in annot:
        tree = ET.parse(xml)
        root = tree.getroot()
        dics = toDictionary(root, indice)

        out.append(dics)

    return out


def toDictionary(root, indice):
    boxes = []
    labels = []

    for object in root.iter('object'):
        if int(object.find('size').text) == indice:
            label = object.find('label').text
            bbox = object.find('bndbox')

            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)

            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(int(label))

    return {'boxes': boxes, 'labels': labels}


crearCarpetasNuevas(path=paths)
