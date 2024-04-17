import socket
import json
import threading

# Criando uma trava para sincronizar o acesso à lista divided_intervals
lock = threading.Lock()

def handle_post_request(client_socket, data, divided_intervals):
    global lock

    with lock:  # Adquirindo a trava antes de acessar a lista
        if len(divided_intervals) == 0:
            response_data = json.dumps({'range': 'empty'})
        else:
            response_data = json.dumps({'range': divided_intervals.pop(0)})

    # Construir a resposta HTTP
    response = f"HTTP/1.1 200 OK\nContent-Type: application/json\nContent-Length: {len(response_data)}\n\n{response_data}"

    # Enviar a resposta ao cliente
    client_socket.sendall(response.encode())
    client_socket.close()

def handle_client(conn,divided_intervals):
    data = conn.recv(1024)
    if data:
        try:
            data_str = data.decode()  # Decodifica os bytes para string
            lines = data_str.split("\n")
            body_index = lines.index("\r") + 1
            body = "\n".join(lines[body_index:])
            json_data = json.loads(body)
            handle_post_request(conn, json_data, divided_intervals)
        except Exception as e:
            print("Erro ao processar requisição:", e)
    conn.close()

def main():
    HOST = 'localhost'
    PORT = 8080
    MAX_CONNECTIONS=12
    PI_INTERVAL=15

    divided_intervals = divide_interval(1, PI_INTERVAL, MAX_CONNECTIONS)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Servidor escutando em {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            print('Conectado por', addr)
            thread = threading.Thread(target=handle_client, args=(conn,divided_intervals,))
            thread.start()

def divide_interval(start, end, parts):
    interval_size = (end - start + 1) // parts
    remainder = (end - start + 1) % parts
    intervals = []
    current_start = start

    for i in range(parts):
        interval_end = current_start + interval_size - 1
        if remainder > 0:
            interval_end += 1
            remainder -= 1
        if current_start <= end:
            intervals.append((current_start, min(interval_end, end)))
        current_start = interval_end + 1

    return intervals


if __name__ == "__main__":
    main()