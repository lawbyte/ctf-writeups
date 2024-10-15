package com.lbyte.pwd2;

import dalvik.system.PathClassLoader;

/* loaded from: classes3.dex */
public class CustomClassLoader extends PathClassLoader {
    public CustomClassLoader(String dexPath) {
        super(dexPath, PathClassLoader.getSystemClassLoader());
    }
}