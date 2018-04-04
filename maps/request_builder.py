import json
import bisect

filename = "test_football.json"

zoom_ratios = [1128.49722, 2256.99444, 4513.98888, 9027.977761, 18055.95552, 36111.91104, 72223.82209, 144447.6442, 288895.2884, 577790.5767, 1155581.153, 2311162.307, 4622324.614, 9244649.227, 18489298.45, 36978596.91, 73957193.82, 147914387.6, 295828775.3, 591657550.5]
zoom_levels = list(range(20, 0, -1))


def read(filename):
    with open(filename) as file:
        data = json.load(file)
        return data

def create_requests(polygon):
    api = "https://maps.googleapis.com/maps/api/staticmap"
    zoom = optimal_zoom(polygon)
    size = 600
    scale = 2
    maptype = "satellite"
    coords = build_path(polygon.get("vertices"))
    coords_simple = simplify_coords(coords, max_coords=120)
    key = "AIzaSyCbSK4DpQMnjtBcite62RK80LsPOnRELVg"
    

    path_color = "0xff8800ff"
    path_weight = 1
    path_fillcolor = "0xff8800ff"

    request = "{api}?zoom={zoom}&size={size}x{size}&scale={scale}&maptype={maptype}&visible={visible}".format(api=api,zoom=zoom,size=size,scale=scale,maptype=maptype,visible=coords_simple)

    image_request = request + "&key={key}".format(key=key)
    mask_request = request + "&path=color:{color}|weight:{weight}|fillcolor:{fillcolor}|{path}&key={key}".format(color=path_color,weight=path_weight,fillcolor=path_fillcolor,path=coords_simple,key=key)

    return image_request, mask_request

def optimal_zoom(polygon):
    x_coords = [point[0] for point in polygon['vertices']]
    y_coords = [point[1] for point in polygon['vertices']]

    x_max, x_min = max(x_coords), min(x_coords)
    y_max, y_min = max(y_coords), min(y_coords)

    delta_x = x_max - x_min
    delta_y = y_max - y_min

    delta_max = max(delta_x, delta_y)

    return delta_to_zoom(delta_max)

def delta_to_zoom(delta):
    zoom_index = bisect.bisect_right(zoom_ratios, 2e6 * delta)

    return zoom_levels[zoom_index]

def build_path(vertices):
    ret = ""
    for vertex in vertices:
        ret += str(vertex[1]) + ',' + str(vertex[0]) + '|'
    return ret[:-1]

def simplify_coords(coordinates, max_coords):
    '''Remove half of the coordinates, until there are less then max_coords '''
    coordinates = coordinates.split('|')
    while(len(coordinates) > max_coords):
        coordinates = [c for (i, c) in enumerate(coordinates) if i % 2 == 0]

    return '|'.join(coordinates)

def main():
    data = read(filename)
    request = create_requests(data[0])
    print(request)

if __name__ == '__main__':
    main()
