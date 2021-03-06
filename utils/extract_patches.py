import numpy as np
np.random.seed(1337)
import ConfigParser

from help_functions import load_hdf5, visualize, group_images
from pre_processing import my_PreProc, my_PreProc_patches, my_PreProc_patches_ROC_testing, my_PreProc_ROC_testing

def get_data_val(DRIVE_train_imgs_original,
                      DRIVE_train_groudTruth,
                      patch_height,
                      patch_width,
                      N_subimgs,
                      inside_FOV,
                      path_experiment):
    train_imgs_original = load_hdf5(DRIVE_train_imgs_original)
    train_masks = load_hdf5(DRIVE_train_groudTruth) #masks always the same
    visualize(group_images(train_imgs_original[0:2,:,:,:],2),path_experiment +'imgs_validation')  #check original imgs train

    # TODO: preprocessing
    train_imgs = my_PreProc(train_imgs_original)
    train_masks = train_masks/255.

    train_imgs = train_imgs[:,:,9:574,:]  #cut bottom and top so now it is 565*565
    train_masks = train_masks[:,:,9:574,:]  #cut bottom and top so now it is 565*565
    data_consistency_check(train_imgs,train_masks)

    #check masks are within 0-1
    assert(np.min(train_masks)==0 and np.max(train_masks)==1)

    print "\ntrain images/masks shape:"
    print train_imgs.shape
    print "train images range (min-max): " +str(np.min(train_imgs)) +' - '+str(np.max(train_imgs))
    print "train masks are within 0-1\n"

    #extract the TRAINING patches from the full images
    patches_imgs_train, patches_masks_train = extract_random_val(train_imgs,train_masks,patch_height,patch_width,N_subimgs,inside_FOV)
    data_consistency_check_patches(patches_imgs_train, patches_masks_train)
    
    ##fourier transform of patches
    patches_imgs_train = my_PreProc_patches(patches_imgs_train)

    print "\ntrain PATCHES images/masks shape:"
    print patches_imgs_train.shape
    print "train PATCHES images range (min-max): " +str(np.min(patches_imgs_train)) +' - '+str(np.max(patches_imgs_train))

    return patches_imgs_train, patches_masks_train#, patches_imgs_test, patches_masks_test

def get_data_val_ROC_testing(DRIVE_train_imgs_original,
                             DRIVE_train_groudTruth,
                             patch_height,
                             patch_width,
                             N_subimgs,
                             inside_FOV,
                             path_experiment,
                             name_experiment):

    train_imgs_original = load_hdf5(DRIVE_train_imgs_original)
    train_masks = load_hdf5(DRIVE_train_groudTruth) #masks always the same
    visualize(group_images(train_imgs_original[0:2,:,:,:],2),path_experiment +'imgs_validation')  #check original imgs train

    # TODO: preprocessing
    train_imgs = my_PreProc_ROC_testing(train_imgs_original, name_experiment)
    train_masks = train_masks/255.

    train_imgs = train_imgs[:,:,9:574,:]  #cut bottom and top so now it is 565*565
    train_masks = train_masks[:,:,9:574,:]  #cut bottom and top so now it is 565*565
    data_consistency_check(train_imgs,train_masks)

    #check masks are within 0-1
    assert(np.min(train_masks)==0 and np.max(train_masks)==1)

    print "\ntrain images/masks shape:"
    print train_imgs.shape
    print "train images range (min-max): " +str(np.min(train_imgs)) +' - '+str(np.max(train_imgs))
    print "train masks are within 0-1\n"

    #extract the TRAINING patches from the full images
    patches_imgs_train, patches_masks_train = extract_random_val(train_imgs,train_masks,patch_height,patch_width,N_subimgs,inside_FOV)
    data_consistency_check_patches(patches_imgs_train, patches_masks_train)
    
    ##fourier transform of patches
    patches_imgs_train = my_PreProc_patches_ROC_testing(patches_imgs_train, name_experiment)

    print "\ntrain PATCHES images/masks shape:"
    print patches_imgs_train.shape
    print "train PATCHES images range (min-max): " +str(np.min(patches_imgs_train)) +' - '+str(np.max(patches_imgs_train))

    return patches_imgs_train, patches_masks_train#, patches_imgs_test, patches_masks_test    

def get_data_training(DRIVE_train_imgs_original,
                      DRIVE_train_groudTruth,
                      patch_height,
                      patch_width,
                      N_subimgs_positive,
                      N_subimgs_negative,
                      inside_FOV,
                      path_experiment):
    train_imgs_original = load_hdf5(DRIVE_train_imgs_original)
    train_masks = load_hdf5(DRIVE_train_groudTruth) #masks always the same
    
    visualize(group_images(train_imgs_original[0:18,:,:,:],6),path_experiment+'imgs_train')  #check original imgs train

    # TODO: preprocessing
    train_imgs = my_PreProc(train_imgs_original)
    train_masks = train_masks/255.

    train_imgs = train_imgs[:,:,9:574,:]  #cut bottom and top so now it is 565*565
    train_masks = train_masks[:,:,9:574,:]  #cut bottom and top so now it is 565*565
    data_consistency_check(train_imgs,train_masks)

    #check masks are within 0-1
    assert(np.min(train_masks)==0 and np.max(train_masks)==1)

    print "\ntrain images/masks shape:"
    print train_imgs.shape
    print "train images range (min-max): " +str(np.min(train_imgs)) +' - '+str(np.max(train_imgs))
    print "train masks are within 0-1\n"

    #extract the TRAINING patches from the full images
    patches_imgs_train, patches_masks_train = extract_random(train_imgs,train_masks,patch_height,patch_width,N_subimgs_positive,N_subimgs_negative,inside_FOV)
    data_consistency_check_patches(patches_imgs_train, patches_masks_train)
    ##Fourier transform of patches
    patches_imgs_train = my_PreProc_patches(patches_imgs_train)
    print "\ntrain PATCHES images/masks shape:"
    print patches_imgs_train.shape
    print "train PATCHES images range (min-max): " +str(np.min(patches_imgs_train)) +' - '+str(np.max(patches_imgs_train))

    return patches_imgs_train, patches_masks_train#, patches_imgs_test, patches_masks_test


# Load the original data and return the extracted patches for training/testing
def get_data_testing_single_image(DRIVE_test_imgs_original, 
                                  DRIVE_test_groudTruth, 
                                  patch_height, 
                                  patch_width,
                                  index):
    ### test
    test_imgs_original = load_hdf5(DRIVE_test_imgs_original)
    test_masks = load_hdf5(DRIVE_test_groudTruth)

    test_imgs = my_PreProc(test_imgs_original)
    test_masks = test_masks / 255.

    # extend both images and masks so they can be divided exactly by the patches dimensions
    test_imgs = test_imgs[index, :, :, :]
    test_masks = test_masks[index, :, :, :]
    # test_imgs = paint_border(test_imgs, patch_height, patch_width)
    # test_masks = paint_border(test_masks, patch_height, patch_width)

    # check masks are within 0-1
    assert (np.max(test_masks) == 1 and np.min(test_masks) == 0)

    print "\ntest images/masks shape:"
    print test_imgs.shape
    print "test images range (min-max): " + str(np.min(test_imgs)) + ' - ' + str(np.max(test_imgs))
    print "test masks are within 0-1\n"

    # extract the TEST patches from the full images
    patches_imgs_test = extract_ordered_single_image(test_imgs, patch_height, patch_width)
    patches_masks_test = extract_ordered_single_image(test_masks, patch_height, patch_width)
    
    patches_imgs_test = my_PreProc_patches(patches_imgs_test)

    data_consistency_check_patches(patches_imgs_test, patches_masks_test)

    print "\ntest PATCHES images/masks shape:"
    print patches_imgs_test.shape
    print "test PATCHES images range (min-max): " + str(np.min(patches_imgs_test)) + ' - ' + str(
        np.max(patches_imgs_test))

    return patches_imgs_test, patches_masks_test


#extract patches randomly in the full training images
#  -- Inside OR in full image
def extract_random(full_imgs,full_masks, patch_h,patch_w, N_patches_positive, N_patches_negative, inside=True):
    if (N_patches_positive%full_imgs.shape[0] != 0 and N_patches_negative%full_imgs.shape[0] != 0):
        print "N_patches: plase enter a multiple of ", full_imgs.shape[0]
        exit()
    N_patches = N_patches_positive + N_patches_negative
    assert (len(full_imgs.shape)==4 and len(full_masks.shape)==4)  #4D arrays

    # image.shape[1] >1 in using gabor wavelet,  so cannot have fixed number of channels

    #assert (full_imgs.shape[1]==1 or full_imgs.shape[1]==3)  #check the channel is 1 or 3

    assert (full_masks.shape[1]==1)   #masks only black and white
    assert (full_imgs.shape[2] == full_masks.shape[2] and full_imgs.shape[3] == full_masks.shape[3])
    patches = np.empty((N_patches,full_imgs.shape[1],patch_h,patch_w))
    patches_masks = np.empty(N_patches)
    img_h = full_imgs.shape[2]  #height of the full image
    img_w = full_imgs.shape[3] #width of the full image
    # (0,0) in the center of the image
    patch_per_img_positive = int(N_patches_positive/full_imgs.shape[0])  #N_patches equally divided in the full images
    patch_per_img_negative = int(N_patches_negative/full_imgs.shape[0])  #N_patches equally divided in the full images
    print "positive patches per full image: " +str(patch_per_img_positive)
    print "negative patches per full image: " +str(patch_per_img_negative)
    iter_tot = 0   #iter over the total numbe rof patches (N_patches)
    for i in range(full_imgs.shape[0]):  #loop over the full images
        k_p=0
        k_n=0
        while k_p <patch_per_img_positive or k_n <patch_per_img_negative:
            x_center = np.random.randint(low = 0+int(patch_w/2),high = img_w-int(patch_w/2))
            # print "x_center " +str(x_center)
            y_center = np.random.randint(low = 0+int(patch_h/2),high = img_h-int(patch_h/2))
            # print "y_center " +str(y_center)
            #check whether the patch is fully contained in the FOV
            if inside==True:
                if is_patch_inside_FOV(x_center,y_center,img_w,img_h,patch_h)==False:
                    continue
            if k_p < patch_per_img_positive and full_masks[i,0,y_center,x_center] == 1.:
                patch = full_imgs[i,:,y_center-int(patch_h/2):y_center+int(patch_h/2)+1,x_center-int(patch_w/2):x_center+int(patch_w/2)+1]
                patch_mask = full_masks[i,0,y_center,x_center]
                patches[iter_tot]=patch
                patches_masks[iter_tot]=patch_mask
                iter_tot +=1   #total
                k_p+=1  #per full_img
            elif k_n < patch_per_img_negative and full_masks[i,0,y_center,x_center] == 0.:
                patch = full_imgs[i,:,y_center-int(patch_h/2):y_center+int(patch_h/2)+1,x_center-int(patch_w/2):x_center+int(patch_w/2)+1]
                patch_mask = full_masks[i,0,y_center,x_center]
                patches[iter_tot]=patch
                patches_masks[iter_tot]=patch_mask
                iter_tot +=1   #total
                k_n+=1  #per full_img
    return patches, patches_masks

#extract patches randomly in the full validation images
#  -- Inside OR in full image
def extract_random_val(full_imgs,full_masks, patch_h,patch_w, N_patches, inside=True):
    if (N_patches%full_imgs.shape[0] != 0):
        print "N_patches: plase enter a multiple of ", full_imgs.shape[0]
        exit()
    assert (len(full_imgs.shape)==4 and len(full_masks.shape)==4)  #4D arrays

    # image.shape[1] >1 in using gabor wavelet,  so cannot have fixed number of channels
    #assert (full_imgs.shape[1]==1 or full_imgs.shape[1]==3)  #check the channel is 1 or 3

    assert (full_masks.shape[1]==1)   #masks only black and white
    assert (full_imgs.shape[2] == full_masks.shape[2] and full_imgs.shape[3] == full_masks.shape[3])
    patches = np.empty((N_patches,full_imgs.shape[1],patch_h,patch_w))
    patches_masks = np.empty(N_patches)
    img_h = full_imgs.shape[2]  #height of the full image
    img_w = full_imgs.shape[3] #width of the full image
    # (0,0) in the center of the image
    patch_per_img = int(N_patches/full_imgs.shape[0])  #N_patches equally divided in the full images
    print "patches per full image: " +str(patch_per_img)
    iter_tot = 0   #iter over the total numbe rof patches (N_patches)
    for i in range(full_imgs.shape[0]):  #loop over the full images
        k=0
        while k <patch_per_img:
            x_center = np.random.randint(low = 0+int(patch_w/2),high = img_w-int(patch_w/2))
            # print "x_center " +str(x_center)
            y_center = np.random.randint(low = 0+int(patch_h/2),high = img_h-int(patch_h/2))
            # print "y_center " +str(y_center)
            #check whether the patch is fully contained in the FOV
            if inside==True:
                if is_patch_inside_FOV(x_center,y_center,img_w,img_h,patch_h)==False:
                    continue
            patch = full_imgs[i,:,y_center-int(patch_h/2):y_center+int(patch_h/2)+1,x_center-int(patch_w/2):x_center+int(patch_w/2)+1]
            patch_mask = full_masks[i,0,y_center,x_center]
            patches[iter_tot]=patch
            patches_masks[iter_tot]=patch_mask
            iter_tot +=1   #total
            k+=1  #per full_img
        
    return patches, patches_masks

# Divide all the full_img in pacthes
def extract_ordered_single_image(full_img, patch_h, patch_w):
    assert (len(full_img.shape) == 3)  # 3D arrays
    assert (full_img.shape[0] == 1 or full_img.shape[0] == 3)  # check the channel is 1 or 3
    img_h = full_img.shape[1]  # height of the full image
    img_w = full_img.shape[2]  # width of the full image
    N_patches_h = img_h - (patch_h-1) 
    N_patches_w = img_w - (patch_w-1) 

    N_patches_tot = (N_patches_h * N_patches_w)

    patches = np.empty((N_patches_tot, full_img.shape[0], patch_h, patch_w))

    iter_tot = 0  # iter over the total number of patches (N_patches)
    for h in range(N_patches_h):
        for w in range(N_patches_w):
            patch = full_img[:, h:(h + patch_h), w:(w + patch_w)]
            patches[iter_tot] = patch
            iter_tot += 1  # total
    assert (iter_tot == N_patches_tot)
    return patches  # array with all the full_imgs divided in patches


def data_consistency_check(imgs,masks):
    assert(len(imgs.shape)==len(masks.shape))
    assert(imgs.shape[0]==masks.shape[0])
    assert(imgs.shape[2]==masks.shape[2])
    assert(imgs.shape[3]==masks.shape[3])
    assert(masks.shape[1]==1)

    
    # image.shape[1] >1 in using gabor wavelet,  so cannot have fixed number of channels
    #assert(imgs.shape[1]==1 or imgs.shape[1]==3)


def data_consistency_check_patches(imgs, masks):
    assert(len(imgs.shape)==4)
    assert(imgs.shape[0]==masks.shape[0])

    # image.shape[1] >1 in using gabor wavelet,  so cannot have fixed number of channels
    #assert(imgs.shape[1]==1 or imgs.shape[1]==3)


def is_patch_inside_FOV(x,y,img_w,img_h,patch_h):
    x_ = x - int(img_w/2) # origin (0,0) shifted to image center
    y_ = y - int(img_h/2)  # origin (0,0) shifted to image center
    R_inside = 270 - int(patch_h * np.sqrt(2.0) / 2.0) #radius is 270 (from DRIVE db docs), minus the patch diagonal (assumed it is a square #this is the limit to contain the full patch in the FOV
    radius = np.sqrt((x_*x_)+(y_*y_))
    if radius < R_inside:
        return True
    else:
        return False
