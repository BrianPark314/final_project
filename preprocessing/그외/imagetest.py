def test(img): ## 이미지 넣기
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(gray, (5, 5),0)
    ret, otsu = cv2.threshold(blurred_img,-1,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU) 
    contours , hierarchy = cv2.findContours(otsu,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour) # 딱 맞는 사각형 좌표 
        bounding_rects.append((x/1280, y/976, (x + w)/1280, (y + h)/976)) # 사각형 그릴떄 쓰는 좌표 
    
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,200,0),2) # 사각형 그림 
    cv2.drawContours(image,contours,-1,(0,200,0))
    cv2.imshow('contour',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()