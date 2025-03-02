package com.metasploit.stage;

import java.net.URLConnection;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.util.Arrays;
import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
/* loaded from: classes.dex */
public final class f implements HostnameVerifier, X509TrustManager {
    private byte[] a;

    private f(byte[] bArr) {
        this.a = bArr;
    }

    public static void a(URLConnection uRLConnection, byte[] bArr) {
        if (uRLConnection instanceof HttpsURLConnection) {
            HttpsURLConnection httpsURLConnection = (HttpsURLConnection) uRLConnection;
            f fVar = new f(bArr);
            SSLContext sSLContext = SSLContext.getInstance("SSL");
            sSLContext.init(null, new TrustManager[]{fVar}, new SecureRandom());
            httpsURLConnection.setSSLSocketFactory(sSLContext.getSocketFactory());
            httpsURLConnection.setHostnameVerifier(fVar);
        }
    }

    @Override // javax.net.ssl.X509TrustManager
    public final void checkClientTrusted(X509Certificate[] x509CertificateArr, String str) {
    }

    @Override // javax.net.ssl.X509TrustManager
    public final void checkServerTrusted(X509Certificate[] x509CertificateArr, String str) {
        if (this.a == null) {
            return;
        }
        if (x509CertificateArr == null || x509CertificateArr.length <= 0) {
            throw new CertificateException();
        }
        for (X509Certificate x509Certificate : x509CertificateArr) {
            try {
                MessageDigest messageDigest = MessageDigest.getInstance("SHA-1");
                messageDigest.update(x509Certificate.getEncoded());
                if (!Arrays.equals(this.a, messageDigest.digest())) {
                    throw new CertificateException("Invalid certificate");
                }
            } catch (Exception e) {
                throw new CertificateException(e);
            }
        }
    }

    @Override // javax.net.ssl.X509TrustManager
    public final X509Certificate[] getAcceptedIssuers() {
        return new X509Certificate[0];
    }

    @Override // javax.net.ssl.HostnameVerifier
    public final boolean verify(String str, SSLSession sSLSession) {
        return true;
    }
}
