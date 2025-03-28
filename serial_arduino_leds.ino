/*
  Código para receber comandos via Serial e ligar pinos específicos:
  - Envia 'Y' para ligar o pino 6.
  - Envia 'G' para ligar o pino 5.
  - Envia 'R' para ligar o pino 7.
  
  O código desliga todos os pinos antes de ligar o correspondente ao comando recebido.
*/

void setup() {
  // Inicializa a comunicação serial a 9600 bps
  Serial.begin(9600);
  
  // Configura os pinos 6, 5 e 7 como saída
  pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(7, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    // Lê o caractere enviado via Serial
    char command = Serial.read();

    // Desliga todos os pinos antes de ligar o desejado
    digitalWrite(6, LOW);
    digitalWrite(5, LOW);
    digitalWrite(7, LOW);

    // Verifica o comando recebido e liga o pino correspondente
    if (command == 'Y') {
      digitalWrite(6, HIGH);
    } else if (command == 'G') {
      digitalWrite(5, HIGH);
    } else if (command == 'R') {
      digitalWrite(7, HIGH);
    }
  }
}
