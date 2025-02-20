# Usar uma imagem base com Python
FROM python:3.9-slim

# Configurar diretório de trabalho
WORKDIR /app

# Copiar o arquivo requirements para o contêiner
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código para o contêiner
COPY . .

# Expor a porta do Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "src/app.py"]
