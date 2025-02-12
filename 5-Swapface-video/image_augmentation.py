import cv2
import numpy

from umeyama import umeyama

def random_channel_shift(x, intensity=10, channel_axis=2):
    x = numpy.rollaxis(x, channel_axis, 0)
    min_x, max_x = numpy.min(x), numpy.max(x)
    intensity = max_x/255*15.
    channel_images = [numpy.clip(x_channel + numpy.random.uniform(-intensity, intensity), min_x, max_x) for x_channel in x]
    x = numpy.stack(channel_images, axis=0)
    x = numpy.rollaxis(x, 0, channel_axis + 1)
    return x

def random_transform( image, rotation_range, zoom_range, shift_range, random_flip ):
    h,w = image.shape[0:2]
    #color_shifted_image = random_channel_shift(image)
    rotation = numpy.random.uniform( -rotation_range, rotation_range )
    scale = numpy.random.uniform( 1 - zoom_range, 1 + zoom_range )
    tx = numpy.random.uniform( -shift_range, shift_range ) * w
    ty = numpy.random.uniform( -shift_range, shift_range ) * h
    mat = cv2.getRotationMatrix2D( (w//2,h//2), rotation, scale )
    mat[:,2] += (tx,ty)
    result = cv2.warpAffine( image, mat, (w,h), borderMode=cv2.BORDER_REPLICATE )
    if numpy.random.random() < random_flip:
        result = result[:,::-1]
    return result

# get pair of random warped images from aligened face image
def random_warp( image ):
    assert image.shape == (256,256,3)
    #range_ = numpy.linspace( 128-80, 128+80, 5 )
    range_ = numpy.linspace( 128-110, 128+110, 5 )
    mapx = numpy.broadcast_to( range_, (5,5) )
    mapy = mapx.T

    mapx = mapx + numpy.random.normal( size=(5,5), scale=6 )
    mapy = mapy + numpy.random.normal( size=(5,5), scale=6 )

    interp_mapx = cv2.resize( mapx, (80,80) )[8:72,8:72].astype('float32')
    interp_mapy = cv2.resize( mapy, (80,80) )[8:72,8:72].astype('float32')

    warped_image = cv2.remap( image, interp_mapx, interp_mapy, cv2.INTER_LINEAR )

    src_points = numpy.stack( [ mapx.ravel(), mapy.ravel() ], axis=-1 )
    dst_points = numpy.mgrid[0:65:16,0:65:16].T.reshape(-1,2)
    mat = umeyama( src_points, dst_points, True )[0:2]

    target_image = cv2.warpAffine( image, mat, (64,64) )

    return warped_image, target_image

# get pair of random warped images from aligened face image
def random_warp128(image):
    assert image.shape == (256,256,3)
    range_ = numpy.linspace(128-110, 128+110, 5)
    mapx = numpy.broadcast_to(range_, (5,5))
    mapy = mapx.T

    mapx = mapx + numpy.random.normal(size=(5,5), scale=6)
    mapy = mapy + numpy.random.normal(size=(5,5), scale=6)

    interp_mapx = cv2.resize(mapx, (80*2,80*2))[8*2:72*2,8*2:72*2].astype('float32')
    interp_mapy = cv2.resize(mapy, (80*2,80*2))[8*2:72*2,8*2:72*2].astype('float32')

    warped_image = cv2.remap(image, interp_mapx, interp_mapy, cv2.INTER_LINEAR)

    src_points = numpy.stack([mapx.ravel(), mapy.ravel() ], axis=-1)
    dst_points = numpy.mgrid[0:65*2:16*2,0:65*2:16*2].T.reshape(-1,2)
    mat = umeyama(src_points, dst_points, True)[0:2]

    target_image = cv2.warpAffine(image, mat, (64*2,64*2))

    return warped_image, target_image

# get pair of random warped images from aligened face image
def random_warp224(image):
    assert image.shape == (256,256,3)
    range_ = numpy.linspace(128-110, 128+110, 5)
    mapx = numpy.broadcast_to(range_, (5,5))
    mapy = mapx.T

    mapx = mapx + numpy.random.normal(size=(5,5), scale=6)
    mapy = mapy + numpy.random.normal(size=(5,5), scale=6)

    interp_mapx = cv2.resize(mapx, (80*4,80*4))[8*4:72*4,8*4:72*4].astype('float32')
    interp_mapy = cv2.resize(mapy, (80*4,80*4))[8*4:72*4,8*4:72*4].astype('float32')

    warped_image = cv2.remap(image, interp_mapx, interp_mapy, cv2.INTER_LINEAR)

    src_points = numpy.stack([mapx.ravel(), mapy.ravel() ], axis=-1)
    dst_points = numpy.mgrid[0:65*4:16*4,0:65*4:16*4].T.reshape(-1,2)
    mat = umeyama(src_points, dst_points, True)[0:2]

    target_image = cv2.warpAffine(image, mat, (64*4,64*4))
    
    target_image = cv2.resize(target_image, (224,224))
    warped_image = cv2.resize(warped_image, (224,224))

    return warped_image, target_image