package com.tudominio.jadxmcp;

import jadx.api.plugins.JadxPlugin;
import jadx.api.plugins.JadxPluginContext;
import jadx.api.plugins.JadxPluginInfo;

public class NttJadxMcpPlugin implements JadxPlugin {

    private static final JadxPluginInfo INFO = new JadxPluginInfo(
        "ntt_jadx_mcp_plugin",
        "NTT JADX MCP Plugin",
        "Expone API REST para el MCP Server de análisis de vulnerabilidades - NTT"
    );

    private NttMcpServer mcpServer;

    @Override
    public JadxPluginInfo getPluginInfo() {
        return INFO;
    }

    @Override
    public void init(JadxPluginContext context) {
        System.out.println("[NTT MCP Plugin] Iniciando...");
        
        // Iniciar servidor HTTP en el puerto 8650 (compatible con jadx-mcp-server)
        mcpServer = new NttMcpServer(context, 8650);
        mcpServer.start();
    }
}
