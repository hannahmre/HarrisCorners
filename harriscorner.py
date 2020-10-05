import math
import cv2
import numpy as np

def makeMatrix(sumxx, sumyy, sumxy):
    m1 = [sumxx, sumxy]
    m2 = [sumxy, sumyy]
    m = [m1, m2]

    return m




def cValues(ixx,iyy,ixy):
    cim = np.zeros((ixx.shape[0], ixx.shape[1], 3), np.float32)
    for i in range(1,ixx.shape[0]-1):
        for j in range(1,ixx.shape[1]-1):
            sumIxx = 0
            sumIyy = 0
            sumIxy = 0

            # Calculate sum for Ixx, Iyy and Ixy values
            for k in range(i-1,i+1):
                for l in range(j-1,j+1):
                    sumIxx += ixx[k][l][0]
                    sumIyy += iyy[k][l][0]
                    sumIxy += ixy[k][l][0]

            m = makeMatrix(sumIxx,sumIyy,sumIxy)  #Create 2x2 matrix with sums

            determinant = computeDeterminant(m)  #Compute the determinant
            trace = computeTrace(m)  #Compute the trace

            c = determinant - 0.05 * (trace ** 2)  #Formula for calculating c value

            cim[i][j][0] = c  #add calculated c values to empty image

    return cim




def computeDeterminant(m):
    return (m[0][0]*m[1][1]) - (m[0][1]*m[1][0])

def computeTrace(m):
    return m[0][0]+m[1][1]




def harrisCorners(im,im2,ix,iy,ixx,iyy,ixy):

    # Calculate Ixx, Iyy and Ixy
    for i in range(1,im.shape[0]-1):
        for j in range(1,im.shape[1]-1):
            ix[i][j] = int(float(im[i+1][j]) - float(im[i-1][j]))
            iy[i][j] = int(float(im[i][j+1]) - float(im[i][j-1]))
            ixx[i][j] = int((float(im[i + 1][j]) - float(im[i - 1][j]))**2)
            iyy[i][j] = int((float(im[i][j + 1]) - float(im[i][j - 1]))**2)
            ixy[i][j] = int((float(im[i+1][j]) - float(im[i-1][j]))*(float(im[i][j+1]) - float(im[i][j-1])))

    m = cValues(ixx,iyy,ixy) #Calling function to calculate c values. Returns image of c values

    # Call Method 1
    cornersMethod1(m,im2)

    # Call Method 2
    # cornersMethod2(m,im2,18,8,5)



#Finds largest c value
def findMax(m):
    maxval = 0
    for i in range(1,len(m)-1):
        for j in range(1,len(m[0])-1):
            if m[i][j][0] > maxval:
                maxval = m[i][j][0]
    return maxval




#Corner Ranking Technique 1
def cornersMethod1(m,img):
    maxval = findMax(m) #Gets largest c value
    for i in range(1,len(m)-1):
        for j in range(1,len(m[0])-1):
            if m[i][j][0] >= maxval*.05: #Finds c values that are greater than given percentage of largest c value
                cv2.circle(img,(j,i),1,(0,0,255),1)  #Adds a red circle to those c values
                # cv2.imwrite("img4.jpg", img)





#Corner Ranking Technique 2
def cornersMethod2(m,img,h,w,n):
    height = math.floor(img.shape[0]/h)
    width = math.floor(img.shape[1]/w)

    for i in range(h): #looping through h rows
        for j in range(w):  #looping through w cols
            nums = []

            # looking at c values in each section
            for ii in range(height*i,(height*i)+height):
                for jj in range(width*j,(width*j)+width):
                    if ii < img.shape[0] and jj < img.shape[1] and m[ii][jj][0] > 0: #keeps indexs in bound and makes sure c value is greater than 0
                        nums.append([m[ii][jj][0], (jj, ii)]) #creating a list to store each c value and its index

            sortednums = sorted(nums, key=lambda x:x[0],reverse=True) #sorts the list from greatest to least

            for value in sortednums[:n]: #grabs the firt n sorted values
                cv2.circle(img, value[1], 1, (0, 0, 255), 1) #adds a red circle to each value
                # cv2.imwrite("img1.jpg", img)





def main():
    im = cv2.imread('checkerboard.png', 0)
    im2 = cv2.imread('checkerboard.png')

    height = im.shape[0]
    width = im.shape[1]

    ix = np.zeros((height,width,3), np.float32)
    iy = np.zeros((height,width,3), np.float32)
    ixx = np.zeros((height, width, 3), np.float32)
    iyy = np.zeros((height, width, 3), np.float32)
    ixy = np.zeros((height, width, 3), np.float32)

    harrisCorners(im,im2,ix,iy,ixx,iyy,ixy)

    cv2.imshow('',im2/255.0)
    cv2.waitKey(0)




main()