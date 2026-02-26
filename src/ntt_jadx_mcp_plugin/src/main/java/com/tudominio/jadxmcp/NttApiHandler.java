package com.tudominio.jadxmcp;

import com.google.gson.Gson;
import jadx.api.JavaClass;
import jadx.api.JavaMethod;
import jadx.api.JavaField;
import jadx.api.plugins.JadxPluginContext;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class NttApiHandler {

    private final JadxPluginContext context;
    private final Gson gson = new Gson();

    public NttApiHandler(JadxPluginContext context) {
        this.context = context;
    }

    // ===== Métodos originales =====
    
    public String getCurrentClass(Map<String, String> params) {
        Map<String, Object> response = new HashMap<>();
        try {
            List<JavaClass> classes = context.getDecompiler().getClasses();
            if (!classes.isEmpty()) {
                JavaClass firstClass = classes.get(0);
                response.put("className", firstClass.getFullName());
                response.put("packageName", firstClass.getPackage());
                response.put("code", firstClass.getCode());
            } else {
                response.put("error", "No hay clases cargadas");
            }
        } catch (Exception e) {
            response.put("error", "getCurrentClass: " + e.getMessage());
        }
        return gson.toJson(response);
    }

    public String getClassCode(Map<String, String> params) {
        String className = params.getOrDefault("name", "");
        Map<String, Object> response = new HashMap<>();

        context.getDecompiler().getClasses().stream()
            .filter(c -> c.getFullName().equals(className))
            .findFirst()
            .ifPresentOrElse(
                cls -> {
                    response.put("className", cls.getFullName());
                    response.put("packageName", cls.getPackage());
                    response.put("code", cls.getCode());
                },
                () -> response.put("error", "Clase no encontrada: " + className)
            );

        return gson.toJson(response);
    }

    public String listClasses(Map<String, String> params) {
        List<String> classes = context.getDecompiler().getClasses()
            .stream()
            .map(JavaClass::getFullName)
            .collect(Collectors.toList());

        Map<String, Object> response = new HashMap<>();
        response.put("classes", classes);
        response.put("total", classes.size());
        return gson.toJson(response);
    }

    public String getMethod(Map<String, String> params) {
        String className = params.getOrDefault("class", "");
        String methodName = params.getOrDefault("method", "");
        Map<String, Object> response = new HashMap<>();

        context.getDecompiler().getClasses().stream()
            .filter(c -> c.getFullName().equals(className))
            .findFirst()
            .ifPresent(cls ->
                cls.getMethods().stream()
                    .filter(m -> m.getName().equals(methodName))
                    .findFirst()
                    .ifPresent(method -> {
                        response.put("class", cls.getFullName());
                        response.put("method", method.getName());
                        response.put("signature", method.getMethodNode().toString());
                        response.put("code", "Método encontrado");
                    })
            );

        if (response.isEmpty()) {
            response.put("error", "Método no encontrado: " + className + "#" + methodName);
        }
        return gson.toJson(response);
    }

    public String search(Map<String, String> params) {
        String term = params.getOrDefault("q", "");
        Map<String, Object> response = new HashMap<>();

        List<Map<String, String>> results = context.getDecompiler().getClasses()
            .stream()
            .filter(c -> c.getCode().contains(term) || c.getFullName().contains(term))
            .map(c -> {
                Map<String, String> r = new HashMap<>();
                r.put("class", c.getFullName());
                r.put("preview", extractPreview(c.getCode(), term));
                return r;
            })
            .limit(50)
            .collect(Collectors.toList());

        response.put("term", term);
        response.put("results", results);
        response.put("total", results.size());
        return gson.toJson(response);
    }

    // ===== Nuevos métodos para compatibilidad con jadx-mcp-server =====
    
    public String getSelectedText(Map<String, String> params) {
        Map<String, Object> response = new HashMap<>();
        response.put("selectedText", "");
        response.put("info", "JADX 1.5.0 no expone texto seleccionado via API");
        return gson.toJson(response);
    }

    public String getMethodByName(Map<String, String> params) {
        return getMethod(params);
    }

    public String getAllClasses(Map<String, String> params) {
        int offset = Integer.parseInt(params.getOrDefault("offset", "0"));
        int count = Integer.parseInt(params.getOrDefault("count", "100"));
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            // Verificar que el decompilador está disponible
            if (context.getDecompiler() == null) {
                response.put("classes", new String[]{});
                response.put("total", 0);
                response.put("offset", offset);
                response.put("count", 0);
                response.put("error", "Decompilador no disponible. ¿Hay un APK cargado?");
                return gson.toJson(response);
            }
            
            List<JavaClass> classes = context.getDecompiler().getClasses();
            if (classes == null || classes.isEmpty()) {
                response.put("classes", new String[]{});
                response.put("total", 0);
                response.put("offset", offset);
                response.put("count", 0);
                response.put("error", "JADX tiene APK cargado pero el plugin no puede verlo");
                response.put("solution", "REINICIA JADX: 1) Cierra JADX completamente, 2) Abre JADX, 3) Carga el APK, 4) Espera que termine de descompilar, 5) Prueba nuevamente");
                response.put("cause", "El JadxPluginContext se captura en init() antes de cargar el APK y nunca se actualiza en JADX 1.5.0");
                return gson.toJson(response);
            }
            
            List<String> allClasses = classes.stream()
                .map(JavaClass::getFullName)
                .collect(Collectors.toList());
            
            int total = allClasses.size();
            int endIndex = Math.min(offset + count, total);
            List<String> paginatedClasses = allClasses.subList(
                Math.min(offset, total), 
                endIndex
            );
            
            response.put("classes", paginatedClasses);
            response.put("total", total);
            response.put("offset", offset);
            response.put("count", paginatedClasses.size());
        } catch (Exception e) {
            response.put("classes", new String[]{});
            response.put("total", 0);
            response.put("offset", offset);
            response.put("count", 0);
            response.put("error", "Error al obtener clases: " + e.getMessage());
            e.printStackTrace();
        }
        
        return gson.toJson(response);
    }

    public String getClassSource(Map<String, String> params) {
        String className = params.getOrDefault("class", "");
        Map<String, Object> response = new HashMap<>();

        context.getDecompiler().getClasses().stream()
            .filter(c -> c.getFullName().equals(className))
            .findFirst()
            .ifPresentOrElse(
                cls -> {
                    response.put("className", cls.getFullName());
                    response.put("source", cls.getCode());
                },
                () -> response.put("error", "Clase no encontrada: " + className)
            );

        return gson.toJson(response);
    }

    public String searchMethod(Map<String, String> params) {
        String methodName = params.getOrDefault("method", "");
        
        List<Map<String, String>> results = context.getDecompiler().getClasses()
            .stream()
            .flatMap(cls -> cls.getMethods().stream()
                .filter(m -> m.getName().contains(methodName))
                .map(m -> {
                    Map<String, String> r = new HashMap<>();
                    r.put("class", cls.getFullName());
                    r.put("method", m.getName());
                    return r;
                }))
            .collect(Collectors.toList());

        Map<String, Object> response = new HashMap<>();
        response.put("results", results);
        response.put("total", results.size());
        return gson.toJson(response);
    }

    public String getMethodsOfClass(Map<String, String> params) {
        String className = params.getOrDefault("class_name", "");
        Map<String, Object> response = new HashMap<>();

        context.getDecompiler().getClasses().stream()
            .filter(c -> c.getFullName().equals(className))
            .findFirst()
            .ifPresentOrElse(
                cls -> {
                    List<String> methods = cls.getMethods().stream()
                        .map(JavaMethod::getName)
                        .collect(Collectors.toList());
                    response.put("methods", methods);
                    response.put("total", methods.size());
                },
                () -> response.put("error", "Clase no encontrada: " + className)
            );

        return gson.toJson(response);
    }

    public String searchClassesByKeyword(Map<String, String> params) {
        String searchTerm = params.getOrDefault("search_term", "");
        int offset = Integer.parseInt(params.getOrDefault("offset", "0"));
        int count = Integer.parseInt(params.getOrDefault("count", "20"));

        List<String> matchingClasses = context.getDecompiler().getClasses()
            .stream()
            .filter(c -> c.getCode().contains(searchTerm) || c.getFullName().contains(searchTerm))
            .map(JavaClass::getFullName)
            .collect(Collectors.toList());

        int total = matchingClasses.size();
        int endIndex = Math.min(offset + count, total);
        List<String> paginatedClasses = matchingClasses.subList(
            Math.min(offset, total),
            endIndex
        );

        Map<String, Object> response = new HashMap<>();
        response.put("classes", paginatedClasses);
        response.put("total", total);
        response.put("offset", offset);
        response.put("count", paginatedClasses.size());
        return gson.toJson(response);
    }

    public String getFieldsOfClass(Map<String, String> params) {
        String className = params.getOrDefault("class_name", "");
        Map<String, Object> response = new HashMap<>();

        context.getDecompiler().getClasses().stream()
            .filter(c -> c.getFullName().equals(className))
            .findFirst()
            .ifPresentOrElse(
                cls -> {
                    List<String> fields = cls.getFields().stream()
                        .map(JavaField::getName)
                        .collect(Collectors.toList());
                    response.put("fields", fields);
                    response.put("total", fields.size());
                },
                () -> response.put("error", "Clase no encontrada: " + className)
            );

        return gson.toJson(response);
    }

    public String getSmaliOfClass(Map<String, String> params) {
        String className = params.getOrDefault("class", "");
        Map<String, Object> response = new HashMap<>();
        response.put("error", "Smali no disponible en JADX 1.5.0 API");
        response.put("className", className);
        return gson.toJson(response);
    }

    public String getManifest(Map<String, String> params) {
        Map<String, Object> response = new HashMap<>();
        response.put("error", "AndroidManifest.xml no disponible directamente en JADX 1.5.0 API");
        response.put("info", "Use getResourceFile con nombre 'AndroidManifest.xml'");
        return gson.toJson(response);
    }

    public String getStrings(Map<String, String> params) {
        Map<String, Object> response = new HashMap<>();
        response.put("strings", new String[]{});
        response.put("total", 0);
        response.put("info", "Strings.xml no disponible directamente en JADX 1.5.0 API");
        return gson.toJson(response);
    }

    public String getAllResourceFileNames(Map<String, String> params) {
        Map<String, Object> response = new HashMap<>();
        response.put("files", new String[]{});
        response.put("total", 0);
        response.put("info", "Lista de recursos no disponible en JADX 1.5.0 API");
        return gson.toJson(response);
    }

    public String getResourceFile(Map<String, String> params) {
        String resourceName = params.getOrDefault("name", "");
        Map<String, Object> response = new HashMap<>();
        response.put("error", "Acceso a recursos no disponible en JADX 1.5.0 API");
        response.put("resourceName", resourceName);
        return gson.toJson(response);
    }

    public String getMainApplicationClassesNames(Map<String, String> params) {
        List<String> classes = context.getDecompiler().getClasses()
            .stream()
            .filter(c -> !c.getFullName().startsWith("android.") && 
                        !c.getFullName().startsWith("androidx.") &&
                        !c.getFullName().startsWith("java.") &&
                        !c.getFullName().startsWith("kotlin."))
            .map(JavaClass::getFullName)
            .collect(Collectors.toList());

        Map<String, Object> response = new HashMap<>();
        response.put("classes", classes);
        response.put("total", classes.size());
        return gson.toJson(response);
    }

    public String getMainApplicationClassesCode(Map<String, String> params) {
        int offset = Integer.parseInt(params.getOrDefault("offset", "0"));
        int count = Integer.parseInt(params.getOrDefault("count", "10"));

        List<Map<String, String>> classes = context.getDecompiler().getClasses()
            .stream()
            .filter(c -> !c.getFullName().startsWith("android.") && 
                        !c.getFullName().startsWith("androidx.") &&
                        !c.getFullName().startsWith("java.") &&
                        !c.getFullName().startsWith("kotlin."))
            .skip(offset)
            .limit(count)
            .map(c -> {
                Map<String, String> classData = new HashMap<>();
                classData.put("className", c.getFullName());
                classData.put("code", c.getCode());
                return classData;
            })
            .collect(Collectors.toList());

        Map<String, Object> response = new HashMap<>();
        response.put("classes", classes);
        response.put("total", classes.size());
        response.put("offset", offset);
        return gson.toJson(response);
    }

    public String getMainActivity(Map<String, String> params) {
        Map<String, Object> response = new HashMap<>();
        response.put("error", "MainActivity no detectada automáticamente en JADX 1.5.0 API");
        response.put("info", "Busque clases que extiendan Activity");
        return gson.toJson(response);
    }

    // ===== Utilidades =====

    private String extractPreview(String code, String term) {
        int idx = code.indexOf(term);
        if (idx == -1) return "";
        int start = Math.max(0, idx - 80);
        int end = Math.min(code.length(), idx + term.length() + 80);
        return code.substring(start, end).replaceAll("\\s+", " ").trim();
    }
}
