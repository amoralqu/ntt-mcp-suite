plugins {
    id("java")
}

group = "com.ntt"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

repositories {
    mavenCentral()
    maven { url = uri("https://s01.oss.sonatype.org/content/repositories/snapshots/") }
}

dependencies {
    // JADX plugin API - ajusta la versión a la que tengas instalada
    compileOnly("io.github.skylot:jadx-core:1.5.0")

    // JSON
    implementation("com.google.code.gson:gson:2.10.1")
}

tasks.jar {
    manifest {
        attributes(
            "Plugin-Class" to "com.ntt.jadxmcp.NttJadxMcpPlugin",
            "Plugin-Id" to "ntt_jadx_mcp_plugin",
            "Plugin-Version" to "1.0.0"
        )
    }
    // Fat jar para incluir dependencias
    from(configurations.runtimeClasspath.get().map { if (it.isDirectory) it else zipTree(it) })
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
}
