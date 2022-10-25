from distutils.log import error
import shutil
import argparse
import csv
import xlrd

def generate_txt_from_xls(file, columna_img, columna_grad, hoja, name, root_save = './'):
    
    wb = xlrd.open_workbook(file)

    hoja_ex = wb.sheet_by_name(hoja)
    txt_string = ''

    for i in range(1, hoja_ex.nrows):
        img = str(hoja_ex.cell_value(i, columna_img))
        grad = int(hoja_ex.cell_value(i, columna_grad))

        txt_string += "{} {}\n".format(img, grad)

    with open(root_save + name, 'w') as arch:
        arch.write(txt_string)
        arch.close()
    
    print('Se guardo el txt en la siguiente ruta: {}'.format(root_save + name))

    

def generate_txt_from_csv(file, columna_img, columna_grad, name ,root_save = './', ext = None):
    
    txt_string = ""

    with open(file, 'r') as arch:
        read = csv.reader(arch, delimiter=',')

        next(read, None)

        for fila in read:
            img = fila[columna_img]
            grad = fila[columna_grad]

            if ext == None:
                txt_string += "{} {}\n".format(img, grad)
            else:
                txt_string += "{}.{} {}\n".format(img, ext, grad)

    with open(root_save + name, 'w') as arch:
        arch.write(txt_string)
        arch.close()
    
    print('Se guardo el txt en la siguiente ruta: {}'.format(root_save + name))
    


def moverImagenes_from_txt(file, origen, destino):

    imgs = []
    grads = []

    dict_info = {
        0 : 0,
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        'errores': 0
    }

    with open(file, 'r') as arch:
        for info in arch:
            imgs.append(info.split(' ')[0])
            grads.append(int(info.split(' ')[1].rstrip('\n')))

    for img, grad in zip(imgs, grads):
        str_origen = r'' + origen + '/' + img
        str_destino = r'' + destino + '/' + str(grad) + '/' + img

        try:
            shutil.copy2(str_origen, str_destino)
            dict_info[grad] += 1
        except Exception as error:
            print(error)
            print("Ocurrio un error al intentar mover esta imagen {}".format(img))
            dict_info['errores'] += 1
            continue
    
    print('Total de imagenes que se movieron {}'.format(dict_info))
    print('Total de imagenes que no es movieron: {}'.format(dict_info['errores']))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')

    ### Accion xls
    parser.add_argument('--xls2txt', action='store_true', default=False)
    parser.add_argument('--hoja', default='Hoja1')
    
    ### Accion csv
    parser.add_argument('--csv2txt', action='store_true', default=False)

    ### Accion copiar imagenes

    parser.add_argument('--mv', action='store_true', default=False)
    parser.add_argument('--origen', default=None)
    parser.add_argument('--destino', default=None)

    parser.add_argument('--col_img', type=int, default=1)
    parser.add_argument('--col_grad', type=int, default=2)
    parser.add_argument('--file_root', default='data')
    parser.add_argument('--name', default=None)
    parser.add_argument('--root_save', default=None)

    parser.add_argument('--ext',default=None)

    args = parser.parse_args()

    if args.xls2txt:
        if args.name != None and args.root_save != None:
            generate_txt_from_xls(args.file_root,
                    args.col_img,
                    args.col_grad,
                    args.hoja,
                    args.name,
                    args.root_save)
        else:
            print('Debes agregar una ruta de guardado y un nombre')
    
    if args.csv2txt:
        if args.name != None and args.root_save != None:
            generate_txt_from_csv(args.file_root,
                    args.col_img,
                    args.col_grad,
                    args.name,
                    args.root_save, 
                    args.ext)
        else:
            print('Debes agregar una ruta de guardado y un nombre')

    if args.mv:
        if args.origen != None and args.destino != None:
            moverImagenes_from_txt(args.file_root,
                    args.origen,
                    args.destino)
        else:
            print('El destino o origen son obligatorios')


