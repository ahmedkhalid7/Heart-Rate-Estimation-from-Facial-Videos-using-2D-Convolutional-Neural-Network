import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChangeDetectorRef, ElementRef } from '@angular/core';
import { HomePageComponent } from './home-page.component';

describe('HomePageComponent', () => {
  let component: HomePageComponent;
  let fixture: ComponentFixture<HomePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HomePageComponent],
      providers: [ChangeDetectorRef]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should start heart rate measurement and update properties', async () => {
    spyOn(component, 'askForCameraAccess').and.returnValue(Promise.resolve(true));
    spyOn(component, 'startVideoStream');
    spyOn(component, 'startImageCaptureAndPrediction');
    
    const detectChangesSpy = spyOn(component.changeDetectorRef, 'detectChanges');
  
    await component.startHeartRateMeasurement();
  
    expect(component.askForCameraAccess).toHaveBeenCalled();
    expect(component.showWebcam).toBe(true);
    expect(detectChangesSpy).toHaveBeenCalled();
    expect(component.startVideoStream).toHaveBeenCalled();
    expect(component.startImageCaptureAndPrediction).toHaveBeenCalled();
  });

  it('should ask for camera access and resolve with true', async () => {
    spyOn(navigator.mediaDevices, 'getUserMedia').and.returnValue(Promise.resolve(new MediaStream()));

    const hasCameraAccess = await component.askForCameraAccess();

    expect(navigator.mediaDevices.getUserMedia).toHaveBeenCalledWith({ video: { facingMode: 'user' } });
    expect(hasCameraAccess).toBe(true);
  });

  it('should ask for camera access and resolve with false', async () => {
    spyOn(navigator.mediaDevices, 'getUserMedia').and.returnValue(Promise.reject());

    const hasCameraAccess = await component.askForCameraAccess();

    expect(navigator.mediaDevices.getUserMedia).toHaveBeenCalledWith({ video: { facingMode: 'user' } });
    expect(hasCameraAccess).toBe(false);
  });

  it('should start video stream and update video element properties', async () => {
    const videoElement = { nativeElement: { srcObject: null, style: { display: '' } } };
    component.videoElement = videoElement as ElementRef;
  
    const mediaStream = new MediaStream();
    spyOn(navigator.mediaDevices, 'getUserMedia').and.returnValue(Promise.resolve(mediaStream));
  
    await component.startVideoStream();
  
    expect(navigator.mediaDevices.getUserMedia).toHaveBeenCalledWith({ video: { facingMode: 'user' } });
    expect(videoElement.nativeElement.srcObject).toBeTruthy();
    expect(videoElement.nativeElement.style.display).toEqual('block');
  });
});
