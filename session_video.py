import sys
import os

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import copy
import cv2
import time


os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
def predict(image_data):

    predictions = sess.run(softmax_tensor, \
            {'DecodeJpeg/contents:0': image_data})


    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

    max_score = 0.0
    res = ''
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        if score > max_score:
            max_score = score
            res = human_string
    return res, max_score


label_lines = [line.rstrip() for line
                in tf.io.gfile.GFile("logs/output_labels.txt")]


with tf.compat.v1.gfile.FastGFile("logs/output_graph.pb", 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.compat.v1.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    while True:
        if os.path.isfile('input.mp4'):
            time.sleep(10)
            try:
                c = 0

                cap = cv2.VideoCapture('input.mp4')
                res, score = '', 0.0
                i = 0
                mem = ''
                consecutive = 0
                sequence = ''
                cv2.waitKey(30)
                while (True):
                    
                    ret, img = cap.read()
                    #img = cv2.flip(img, 1)
                    
                    if ret:
                        x1, y1, x2, y2 = 100, 100, 300, 300
                        img_cropped = img[y1:y2, x1:x2]

                        c += 1
                        image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()
                        cv2.imwrite( "imagini/imagine.jpg", img_cropped)
                        a = cv2.waitKey(1) 
                        
                        if i == 50:
                            res_tmp, score = predict(image_data)
                            res = res_tmp
                            i = 0
                            #print(sequence[:-1] +  "ultima litera")
                            if res !='nimic':
                                if len(sequence) == 0:
                                    sequence += res
                                    print(sequence)
                                else:
                                    if sequence[-1] != res:
                                        sequence += res
                                        print(sequence)
                            else:
                                print("nimic")

                        i += 1
                            

                        cv2.putText(img, '%s' % (res.upper()), (100,400), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
                        cv2.putText(img, '(score = %.5f)' % (float(score)), (100,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))

                        cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
                        cv2.imshow("img", img)
                        #img_sequence = np.zeros((200,1200,3), np.uint8)
                        #cv2.putText(img_sequence, '%s' % (sequence.upper()), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                        #cv2.imshow('sequence', img_sequence)
                        
                        if a == 27: 
                            break
                    else:
                        break
                import corector
                corector.corrector(sequence)
            # Following line should... <-- This should work fine now
                cap.release()
                cv2.destroyAllWindows()
                os.remove('input.mp4')
                time.sleep(3)
            except cv2.error as e:
                print("waiting file")
        if os.path.isfile('test.jpg'):
            time.sleep(5)
            image_data = tf.compat.v1.gfile.FastGFile('test.jpg', 'rb').read()
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor, \
                    {'DecodeJpeg/contents:0': image_data})


            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            
            printed = False
            for node_id in top_k:
                if not printed:
                    print(label_lines[node_id] + " print ")
                    with open('output.txt', 'w') as file:
                        file.write(label_lines[node_id])
                    printed = True
            os.remove('test.jpg')
            time.sleep(3)


