from pathlib import Path, WindowsPath
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

import torch
import cv2
import numpy as np
import os

class FoodDetector:
    def __init__(self):
        try:
            # Model yolu
            model_path = str(Path(os.path.abspath('best.pt')))
            print(f"Model yolu: {model_path}")

            # Model yükleme
            self.model = torch.hub.load('ultralytics/yolov5', 
                                      'custom', 
                                      path=model_path,
                                      force_reload=True, 
                                      trust_repo=True)
            
            # Model ayarları
            self.model.conf = 0.07
            self.model.iou = 0.3    
            self.model.classes = None  
            self.model.max_det = 100  
            
            # Model sınıflarını görüntüle
            print("\nModel sınıfları:")
            print(self.model.names)
            print("\nModel başarıyla yüklendi!")

        except Exception as e:
            print(f"Hata: {str(e)}")
            raise

    def detect(self, image_path):
        try:
            # Görüntüyü yükle
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Görüntü yüklenemedi: {image_path}")

            # Görüntü ön işleme
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Tahmin yap
            results = self.model(img_rgb, size=500)

            # Sonuçları işle
            detections = results.pandas().xyxy[0]
            
            # Görüntü üzerine tespitleri çiz
            result_img = img.copy()
            if len(detections) > 0:
                print("\nTespitler:")
                for idx, detection in detections.iterrows():
                    # Koordinatları al
                    x1, y1 = int(detection['xmin']), int(detection['ymin'])
                    x2, y2 = int(detection['xmax']), int(detection['ymax'])
                    label = f"{detection['name']} {detection['confidence']:.2f}"
                    
                    # Kutu çiz
                    cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Etiket yaz
                    cv2.putText(result_img, label, (x1, y1-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    print(f"Tespit {idx+1}:")
                    print(f"  Sınıf: {detection['name']}")
                    print(f"  Güven: {detection['confidence']:.2f}")
                    print(f"  Koordinatlar: [{x1}, {y1}, {x2}, {y2}]")
            else:
                print("Tespit yapılamadı!")

            return result_img

        except Exception as e:
            print(f"Tespit hatası: {str(e)}")
            return None

def main():
    try:
        # Detector oluştur
        detector = FoodDetector()

        # Test görüntüleri
        test_images = [
            '261040_jpg.rf.1dfe697f87b5bd6fd4713d958af85e6a.jpg'
        ]

        # Her görüntüyü test et
        for img_path in test_images:
            if os.path.exists(img_path):
                print(f"\nİşleniyor: {img_path}")
                
                # Tespit yap
                result = detector.detect(img_path)
                
                if result is not None:
                    # Sonuç görüntüsünü kaydet
                    output_path = f"result_{os.path.basename(img_path)}"
                    cv2.imwrite(output_path, result)
                    print(f"Sonuç kaydedildi: {output_path}")
                    
                    # Görüntüle
                    cv2.imshow('Food Detection', result)
                    key = cv2.waitKey(0)
                    if key == 27:  # ESC
                        break
            else:
                print(f"Dosya bulunamadı: {img_path}")

        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Program hatası: {str(e)}")

if __name__ == "__main__":
    main()