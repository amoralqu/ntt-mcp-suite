package com.tudominio.jadxmcp;

import jadx.api.plugins.JadxPluginContext;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class NttMcpServer {

    private final JadxPluginContext context;
    private final int port;
    private ServerSocket serverSocket;
    private ExecutorService executor;
    private volatile boolean running = false;

    public NttMcpServer(JadxPluginContext context, int port) {
        this.context = context;
        this.port = port;
    }

    public void start() {
        try {
            serverSocket = new ServerSocket(port);
            executor = Executors.newCachedThreadPool();
            running = true;
            
            System.out.println("[NTT MCP Plugin] Escuchando en http://localhost:" + port);
            
            // Thread para aceptar conexiones
            Thread acceptThread = new Thread(() -> {
                while (running) {
                    try {
                        Socket clientSocket = serverSocket.accept();
                        executor.submit(() -> handleRequest(clientSocket));
                    } catch (IOException e) {
                        if (running) {
                            System.err.println("[NTT MCP Plugin] Error aceptando conexión: " + e.getMessage());
                        }
                    }
                }
            });
            acceptThread.setDaemon(true);
            acceptThread.start();
            
        } catch (IOException e) {
            System.err.println("[NTT MCP Plugin] Error al iniciar servidor: " + e.getMessage());
        }
    }

    private void handleRequest(Socket clientSocket) {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
             OutputStream out = clientSocket.getOutputStream()) {
            
            // Leer la línea de request
            String requestLine = in.readLine();
            if (requestLine == null) return;
            
            // Leer headers (ignoramos por ahora)
            String line;
            while ((line = in.readLine()) != null && !line.isEmpty()) {
                // Skip headers
            }
            
            // Parsear el request
            String[] parts = requestLine.split(" ");
            if (parts.length < 2) {
                sendResponse(out, 400, "Bad Request");
                return;
            }
            
            String method = parts[0];
            String path = parts[1];
            
            if (!method.equals("GET")) {
                sendResponse(out, 405, "Method Not Allowed");
                return;
            }
            
            // Parsear path y query string
            String endpoint;
            Map<String, String> params = new HashMap<>();
            
            int queryIndex = path.indexOf('?');
            if (queryIndex >= 0) {
                endpoint = path.substring(0, queryIndex);
                String queryString = path.substring(queryIndex + 1);
                parseQueryString(queryString, params);
            } else {
                endpoint = path;
            }
            
            // Procesar endpoint
            NttApiHandler handler = new NttApiHandler(context);
            String response;
            
            switch (endpoint) {
                // Health check
                case "/health":
                    sendJsonResponse(out, 200, "{\"status\":\"ok\",\"version\":\"1.0.0\"}");
                    return;
                    
                // Endpoints originales (compatibilidad)
                case "/list-classes":
                    response = handler.listClasses(params);
                    break;
                case "/get-class-code":
                    response = handler.getClassCode(params);
                    break;
                case "/get-current-class":
                    response = handler.getCurrentClass(params);
                    break;
                case "/get-method":
                    response = handler.getMethod(params);
                    break;
                case "/search":
                    response = handler.search(params);
                    break;
                    
                // Endpoints compatibles con jadx-mcp-server
                case "/current-class":
                    response = handler.getCurrentClass(params);
                    break;
                case "/selected-text":
                    response = handler.getSelectedText(params);
                    break;
                case "/method-by-name":
                    response = handler.getMethodByName(params);
                    break;
                case "/all-classes":
                    response = handler.getAllClasses(params);
                    break;
                case "/class-source":
                    response = handler.getClassSource(params);
                    break;
                case "/search-method":
                    response = handler.searchMethod(params);
                    break;
                case "/methods-of-class":
                    response = handler.getMethodsOfClass(params);
                    break;
                case "/search-classes-by-keyword":
                    response = handler.searchClassesByKeyword(params);
                    break;
                case "/fields-of-class":
                    response = handler.getFieldsOfClass(params);
                    break;
                case "/smali-of-class":
                    response = handler.getSmaliOfClass(params);
                    break;
                case "/manifest":
                    response = handler.getManifest(params);
                    break;
                case "/strings":
                    response = handler.getStrings(params);
                    break;
                case "/list-all-resource-files-names":
                    response = handler.getAllResourceFileNames(params);
                    break;
                case "/get-resource-file":
                    response = handler.getResourceFile(params);
                    break;
                case "/main-application-classes-names":
                    response = handler.getMainApplicationClassesNames(params);
                    break;
                case "/main-application-classes-code":
                    response = handler.getMainApplicationClassesCode(params);
                    break;
                case "/main-activity":
                    response = handler.getMainActivity(params);
                    break;
                    
                default:
                    sendResponse(out, 404, "{\"error\":\"Endpoint not found: " + endpoint + "\"}");
                    return;
            }
            
            sendJsonResponse(out, 200, response);
            
        } catch (IOException e) {
            System.err.println("[NTT MCP Plugin] Error manejando request: " + e.getMessage());
        } finally {
            try {
                clientSocket.close();
            } catch (IOException e) {
                // Ignore
            }
        }
    }
    
    private void parseQueryString(String queryString, Map<String, String> params) {
        String[] pairs = queryString.split("&");
        for (String pair : pairs) {
            int idx = pair.indexOf('=');
            if (idx > 0) {
                try {
                    String key = URLDecoder.decode(pair.substring(0, idx), StandardCharsets.UTF_8.name());
                    String value = URLDecoder.decode(pair.substring(idx + 1), StandardCharsets.UTF_8.name());
                    params.put(key, value);
                } catch (UnsupportedEncodingException e) {
                    // Ignore
                }
            }
        }
    }
    
    private void sendResponse(OutputStream out, int statusCode, String body) throws IOException {
        String statusText = getStatusText(statusCode);
        String response = "HTTP/1.1 " + statusCode + " " + statusText + "\r\n" +
                         "Content-Type: text/plain\r\n" +
                         "Content-Length: " + body.getBytes(StandardCharsets.UTF_8).length + "\r\n" +
                         "Connection: close\r\n" +
                         "\r\n" +
                         body;
        out.write(response.getBytes(StandardCharsets.UTF_8));
        out.flush();
    }
    
    private void sendJsonResponse(OutputStream out, int statusCode, String json) throws IOException {
        String statusText = getStatusText(statusCode);
        byte[] jsonBytes = json.getBytes(StandardCharsets.UTF_8);
        String response = "HTTP/1.1 " + statusCode + " " + statusText + "\r\n" +
                         "Content-Type: application/json\r\n" +
                         "Content-Length: " + jsonBytes.length + "\r\n" +
                         "Access-Control-Allow-Origin: *\r\n" +
                         "Connection: close\r\n" +
                         "\r\n";
        out.write(response.getBytes(StandardCharsets.UTF_8));
        out.write(jsonBytes);
        out.flush();
    }
    
    private String getStatusText(int code) {
        switch (code) {
            case 200: return "OK";
            case 400: return "Bad Request";
            case 404: return "Not Found";
            case 405: return "Method Not Allowed";
            case 500: return "Internal Server Error";
            default: return "Unknown";
        }
    }

    public void stop() {
        running = false;
        if (executor != null) {
            executor.shutdown();
        }
        if (serverSocket != null) {
            try {
                serverSocket.close();
                System.out.println("[NTT MCP Plugin] Servidor detenido");
            } catch (IOException e) {
                System.err.println("[NTT MCP Plugin] Error al detener servidor: " + e.getMessage());
            }
        }
    }
}
