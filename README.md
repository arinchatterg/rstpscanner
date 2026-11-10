# Single IP RTSP Stream Scanner

A lightweight utility to brute-force common RTSP paths on a single IP address and identify live, unauthenticated video streams. Designed for authorized security assessments and infrastructure auditing.

## Purpose

This tool tests a target IP against a comprehensive list of known RTSP URL patterns used by major camera manufacturers (Hikvision, Dahua, Axis, Ubiquiti) and generic devices. It validates stream availability by attempting to read a single frame via OpenCV/FFmpeg without saving or storing any video data.

## Requirements

-   Python 3.8+
-   `opencv-python-headless`
-   FFmpeg (must be in system PATH; OpenCV uses it as the backend for RTSP handling)

Install dependencies:

```bash
pip install opencv-python-headless
```

## Usage

```bash
python single_ip_scanner.py <TARGET_IP>
```

Example:

```bash
python single_ip_scanner.py 192.168.1.50
```

The script will test up to 150+ common RTSP paths and stop after finding 3 valid streams. Each confirmed stream outputs a direct `rtsp://` URL that can be copied into VLC or other media players. Proof-of-concept screenshots are saved locally as `proof_<IP>_<path>.jpg`.

## Important Notes

-   This tool is intended solely for authorized security research, penetration testing with explicit written permission, or auditing your own infrastructure.
-   Unauthorized access to networked cameras may violate computer fraud laws and organizational policies. Always obtain proper authorization before scanning.
-   The scanner sends connection requests to port 554 and attempts to open RTSP streams. This generates visible network traffic and log entries on the target device.
-   No credentials are tested beyond empty/default URL parameters already embedded in the path list. This is not a password cracker.
-   Results should be validated manually. False positives can occur due to honeypots, misconfigured services, or transient network conditions.

## Path Coverage

The included path list covers:

-   Generic RTSP endpoints (`/live.sdp`, `/stream1`, `/h264`, etc.)
-   Hikvision Streaming Channels and AV stream paths
-   Dahua realmonitor and CGI endpoints
-   Axis media amp and MJPEG paths
-   Ubiquiti UniFi live channels
-   Bosch, Hanwha, Uniview, Vivotek, Foscam vendor-specific paths
-   ONVIF media service endpoints
-   Common default credential URL patterns
-   Snapshot and CGI fallback endpoints

## Disclaimer

This software is provided for educational and authorized security assessment purposes only. The authors assume no liability for misuse. Users are responsible for ensuring compliance with applicable laws, regulations, and organizational policies.
