package com.metasploit.stage;

import java.net.URLConnection;
import java.util.LinkedList;
import java.util.List;
/* loaded from: classes.dex */
public final class a {
    public int a;
    public long b;
    public String c;
    public List d = new LinkedList();

    public static void a(URLConnection uRLConnection, String str, String str2) {
        String[] split;
        if (!a(str2)) {
            uRLConnection.addRequestProperty("User-Agent", str2);
        }
        for (String str3 : str.split("\r\n")) {
            if (!a(str3)) {
                String[] split2 = str3.split(": ", 2);
                if (split2.length == 2 && !a(split2[0]) && !a(split2[1])) {
                    uRLConnection.addRequestProperty(split2[0], split2[1]);
                }
            }
        }
    }

    private static boolean a(String str) {
        return str == null || "".equals(str);
    }
}
