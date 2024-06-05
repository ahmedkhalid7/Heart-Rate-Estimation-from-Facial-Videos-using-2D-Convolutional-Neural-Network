import { ChangeDetectorRef, Component, ElementRef, ViewChild } from '@angular/core';


@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})


export class HomePageComponent {
  @ViewChild('video', { static: false }) videoElement!: ElementRef;
  showWebcam = false;
  predictedHeartRate: number | null = null;
  errorMessage: string | null = null;

  constructor(private changeDetectorRef: ChangeDetectorRef) {}
  
  startHeartRateMeasurement(): void {
    this.askForCameraAccess()
      .then((hasCameraAccess) => {
          if (hasCameraAccess) {
            this.showWebcam = true;
            this.changeDetectorRef.detectChanges();
            this.startVideoStream();
            this.startImageCaptureAndPrediction();
          }
      });
  }

  askForCameraAccess(): Promise<boolean> {
    return new Promise<boolean>((resolve, reject) => {
      navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
        .then(() => {
          resolve(true);
        })
        .catch((error) => {
          resolve(false);
        });
    }); 
  }

  startVideoStream(): void {
    const videoElement: HTMLVideoElement = this.videoElement.nativeElement;
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
      .then((stream) => {
        videoElement.srcObject = stream;
        videoElement.style.display = 'block'; 
      })
  }

  startImageCaptureAndPrediction(): void {
    const videoElement: HTMLVideoElement = this.videoElement.nativeElement;
  
    const captureFrame = () => {
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      const context = canvas.getContext('2d');
  
      if (context) {
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        const image = canvas.toDataURL('image/png');

        this.predictHeartRate(image)
          .then((response) => {
            if (typeof response === 'number') {
              this.predictedHeartRate = response;
              this.errorMessage = '';
            } else if (typeof response === 'string') {
              this.errorMessage = response;
              this.predictedHeartRate = null;
            } else this.predictedHeartRate = null; // 204 no change
          })
          .catch((error) => {
            this.errorMessage = error;
          });
      }
      setTimeout(captureFrame, 2000); 
    };
    setTimeout(captureFrame, 2000); 
  }
  
  predictHeartRate(image: string): Promise<number | string> {
    
    const formData = new FormData();
  
    const byteCharacters = atob(image.split(',')[1]); // extracts first 6 bits from each character

    console.log(byteCharacters);
    console.log(image);

    const byteArrays = [];
    for (let i = 0; i < byteCharacters.length; i++) {
      byteArrays.push(byteCharacters.charCodeAt(i));
    }
    console.log(byteArrays);

    const blob = new Blob([new Uint8Array(byteArrays)], { type: 'image/png' });
    console.log(blob);

    console.log("base64 encoded image size ", image.length);
    console.log("blob size ", blob.size);
    formData.append('image', blob);
  
    return fetch('https://serverside-tu64dty6ea-ww.a.run.app/predict', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        if (data.hasOwnProperty('heart_rate')) {
          return data.heart_rate;
        } else if (data.hasOwnProperty('error')) {
          return data.error;
        }
      })
      .catch(error => {
        return error;
      });
  }
}
