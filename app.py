import cv2
import mediapipe as mp
import serial
import time

# Inicia a conexão com o Arduino (ajuste a porta se necessário)
arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)  # Aguarda o Arduino iniciar

# Inicializa o detector de malha facial do MediaPipe
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(max_num_faces=1)
mp_draw = mp.solutions.drawing_utils

# Inicia a captura de vídeo a partir do arquivo "video.mp4"
cap = cv2.VideoCapture('video.mp4')
if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# Define um limiar para detectar a variação do nariz em relação ao centro dos olhos
THRESHOLD = 0.03  # Valor em coordenadas normalizadas (0 a 1)

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Fim do vídeo

    # (Opcional) Espelha o frame para uma visualização mais natural
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        # Verifica se os landmarks necessários estão presentes (índices 1, 33 e 263)
        if len(landmarks) < 264:
            cv2.putText(frame, "Landmarks incompletos", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            # Obtemos os landmarks:
            left_eye = landmarks[33]
            right_eye = landmarks[263]
            nose = landmarks[1]

            # Calcula o centro horizontal entre os olhos
            center_eye_x = (left_eye.x + right_eye.x) / 2.0

            # Diferença entre a posição do nariz e o centro dos olhos
            diff = nose.x - center_eye_x

            # Define a direção e o comando baseado no valor de diff
            if diff < -THRESHOLD:
                direcao = "Looking Left"
                comando = b'G'  # Liga pino 5
            elif diff > THRESHOLD:
                direcao = "Looking Right"
                comando = b'R'  # Liga pino 7
            else:
                direcao = "Looking Forward"
                comando = b'Y'  # Liga pino 6

            # Envia o comando via serial para o Arduino
            arduino.write(comando)

            # Desenha a malha facial para visualização
            mp_draw.draw_landmarks(
                frame,
                results.multi_face_landmarks[0],
                mp_face.FACEMESH_TESSELATION,
                landmark_drawing_spec=mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1)
            )

            # Exibe informações na tela (opcional para debug)
            cv2.putText(frame, f"Nose: {nose.x:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.putText(frame, f"Center Eyes: {center_eye_x:.2f}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.putText(frame, f"Diff: {diff:.3f}", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.putText(frame, direcao, (10, 130),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Exibe o vídeo
    cv2.imshow("Head Pose Estimation", frame)

    # Encerra o loop ao pressionar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos e fecha as conexões
cap.release()
arduino.close()
cv2.destroyAllWindows()
