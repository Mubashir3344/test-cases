FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl fonts-liberation \
    libasound2t64 \
    libatk-bridge2.0-0t64 libatk1.0-0t64 libcairo2 libcups2t64 libdbus-1-3 \
    libdrm2 libgbm1 libglib2.0-0t64 libgtk-3-0t64 libnspr4 libnss3 \
    libpango-1.0-0 libxcomposite1 libxdamage1 libxfixes3 \
    libxkbcommon0 libxrandr2 xdg-utils --no-install-recommends \
    && install -d /etc/apt/keyrings \
    && wget -q -O /etc/apt/keyrings/google-chrome.asc \
       https://dl-ssl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.asc] \
       http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/test-results

CMD ["pytest", "tests/", "-v", \
     "--junit-xml=/app/test-results/results.xml", \
     "--html=/app/test-results/report.html", \
     "--self-contained-html"]
