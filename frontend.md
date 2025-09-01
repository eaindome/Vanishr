<!-- frontend:
    build: ./frontend
    command: npm run dev -- --host 0.0.0.0
    volumes:
      - ./frontend:/frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend -->