# Endpoint Availability Monitor

## Installation
1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py config.yaml
```

## Configuration
The YAML configuration file should contain a list of endpoints with the following format:
```yaml
- name: Endpoint Name
  url: https://example.com
  method: GET  # Optional, defaults to GET
  headers:     # Optional
    Content-Type: application/json
  body: '{}'   # Optional, must be valid JSON string
```

## Issues Identified and Fixes
1. **Missing Response Time Check**
   - Added response time measurement
   - Endpoints must respond within 500ms to be considered available

2. **Domain Parsing**
   - Fixed domain parsing to properly handle ports using urlparse
   - Now correctly ignores port numbers when determining domain

3. **Request Timeout**
   - Added 550ms timeout to prevent hanging requests
   - Ensures timely responses for accurate availability tracking

4. **Logging**
   - Replaced print statements with proper logging
   - Added file logging to monitor.log
   - Includes detailed status and timing information

5. **Input Validation**
   - Added validation for YAML structure
   - Ensures required fields are present and properly formatted

6. **Error Handling**
   - Improved error handling throughout the application
   - Added proper error messages and exit codes

## Example Output
```
2025-04-14 14:23:45,123 - INFO - Endpoint https://example.com is UP (Status: 200, Time: 123.45ms)
example.com has 100% availability percentage
---
2025-04-14 14:24:00,456 - WARNING - Endpoint https://example.com is DOWN (Status: 500, Time: 567.89ms)
example.com has 50% availability percentage
