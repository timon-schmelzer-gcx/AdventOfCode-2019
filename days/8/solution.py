from collections import Counter
import itertools

VISUALISATION = {
    # Black
    0: '\x1b[0;30;40m' + ' ' + '\x1b[0m',
    # White
    1: '\x1b[0;30;47m' + ' ' + '\x1b[0m',
    # Transparent
    2: ' '
}


def read_data(path='days/8/data.txt'):
    with open(path, 'r') as infile:
        image = infile.read()
    return image.replace('\n', '')


def reshape(image, width=25, height=6):
    reshaped_image = []
    zeros_one_twos = []
    n_layers = int(len(image)/width/height)
    for l in range(n_layers):
        layer = []
        for i in range(height):
            i = int(i)
            start = i * width + l * width*height
            stop = i * width + width + l * width*height
            image_slice = image[start:stop]
            layer.append(image_slice)

        layer_flat = itertools.chain(*layer)
        counter_layer = Counter(layer_flat)
        zeros_one_twos.append(counter_layer)
        reshaped_image.append(layer)

    return reshaped_image, zeros_one_twos


def merge_layers(layers):
    base_layer = layers[0][:]
    base_layer = [list(row) for row in base_layer]
    for layer in layers:
        for nrow, row in enumerate(layer):
            for ncol, digit in enumerate(layer[int(nrow)]):
                if digit == '0':
                    base_layer[int(nrow)][int(ncol)] = '0'
                elif digit == '1':
                    base_layer[int(nrow)][int(ncol)] = '1'
                elif digit == '2':
                    # Nothing to do for transparent
                    continue

    return base_layer


def display_layer(layer):
    for row in layer:
        row_pretty = [VISUALISATION[int(bwt)] for bwt in row]
        print(''.join(row_pretty))


if __name__ == "__main__":
    image = read_data()

    reshaped_image, zeros_one_twos = reshape(image)
    zeros_one_twos_sorted = sorted(
        zeros_one_twos, key=lambda counter: counter['0']
    )
    print(
        'Solution part 1:',
        zeros_one_twos_sorted[0]['1'] * zeros_one_twos_sorted[0]['2']
    )

    print('Solution part 2:')
    display_layer(merge_layers(reshaped_image[::-1]))
